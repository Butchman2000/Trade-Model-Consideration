# Module: enforce_allocation_rules_oneTOfive.py
# Author: Brian Anderson
# Origin Date: 11May2025
# Version: 1.1
#
# Purpose:
#    /Begin converting risk allocation rules into code-based enforcement.

'''
========== RULE BASED FRAMEWORK ==========

# rule 1 – enforce 10% liquidity reserve
# ensure total bin allocation does not exceed (1.0 - liquidity_reserve)
# if exceeded, scale down proportionally or raise exception

# rule 2 – preserve 10% for manual trading
# enforce that bin_weights + manual_trading_alloc <= 0.90

# rule 3 – no bin exceeds 6% total allocation
# optionally: apply "safe utilization" rule (4.5%)
# optionally: flag if any single bin is above 0.06 even after scaling

# rule 4 – max number of bins: 25; if overlapping underlyings: max = 20
# input must include bin metadata: which equity is used in each bin
# count overlap; reduce cap if needed

# rule 5 – futures max 5% allocation, 3.75% margin exposure
# detect any bin involving futures models; sum their allocation; flag if above limit

(continued in 'enforce_allocation_rules_sixTOeleven')

========== END OF RULE LIST ==========
'''

# === CONSTRAINTS (sample values for development) ===
# These would typically come from config_loader or external config file.
# Used here as reference for collaborators and context for enforcement logic.

# Example constraint values:
# max_bin_weight: 0.06 (6%)
# min_bin_weight: 0.025 (2.5%)
# liquidity_reserve: 0.10 (10%) of account held in cash or low-vol reserves
# manual_trading_allocation: 0.10 (10%) reserved for discretionary/manual orders

# note: several inputs assumed but not yet available
# - bin_weights: dict of {bin_name: float} after scaling
# - constraints: dict containing liquidity_reserve, max_bin_weight, etc.
# - bin_metadata: dict of {bin_name: {...}} including strategy type, underlying, last_rotation, margin_mult

# all outputs are assumed to return adjusted bin_weights or flag warnings


def enforce_liquidity_reserve_only(bin_weights, constraints):
    '''Rule 1 only: enforce 10% liquidity reserve'''
    liquidity_reserve = constraints['liquidity_reserve']
    max_total_allowed = 1.0 - liquidity_reserve
    current_total = sum(bin_weights.values())

    if current_total > max_total_allowed:
        scaling_factor = max_total_allowed / current_total
        for bin_name in bin_weights:
            bin_weights[bin_name] *= scaling_factor

    return bin_weights


def enforce_manual_reserve_only(bin_weights, constraints):
    '''Rule 2 only: reserve space for manual trading (typically 10%)'''
    manual_reserve = constraints['manual_trading_allocation']
    max_auto_alloc = 1.0 - manual_reserve
    current_total = sum(bin_weights.values())

    if current_total > max_auto_alloc:
        scaling_factor = max_auto_alloc / current_total
        for bin_name in bin_weights:
            bin_weights[bin_name] *= scaling_factor

    return bin_weights


def enforce_per_bin_maximum(bin_weights, constraints):
    '''Rule 3 enforcement: enforce a per-bin maximum allocation'''
    max_bin = constraints['max_bin_weight']
    flagged_bins = []

    for bin_name, allocation in bin_weights.items():
        if allocation > max_bin:
            flagged_bins.append((bin_name, allocation))
            bin_weights[bin_name] = max_bin  # Cap it to the maximum

    return bin_weights, flagged_bins


def enforce_bin_count_and_overlap(bin_weights, bin_metadata):
    '''Rule 4: cap number of bins and enforce unique underlying spread'''
    max_bins_allowed = 25
    overlap_threshold = 20  # Penalty if overlap detected above this

    active_bins = list(bin_weights.keys())
    underlyings = []
    for bin_name in active_bins:
        if 'underlying' in bin_metadata.get(bin_name, {}):
            underlyings.append(bin_metadata[bin_name]['underlying'])

    unique_underlyings = set(underlyings)

    if len(active_bins) > max_bins_allowed:
        return False, 'too many bins active'
    if len(unique_underlyings) < len(active_bins) and len(active_bins) > overlap_threshold:
        return False, 'bin overlap exceeds threshold'

    return True, None


def enforce_futures_allocation(bin_weights, bin_metadata):
    '''Rule 5: limit total exposure to futures strategies'''
    max_futures_alloc = 0.05
    max_margin_used = 0.0375
    total_futures_alloc = 0.0

    for bin_name, allocation in bin_weights.items():
        bin_type = bin_metadata.get(bin_name, {}).get('type', None)
        if bin_type == 'futures':
            total_futures_alloc += allocation

    if total_futures_alloc > max_futures_alloc:
        return False, 'futures allocation exceeds maximum permitted exposure'

    return True, None


# Enforcement driver function (placeholder)
# Calls individual rule enforcement in sequence

def enforce_allocation_rules(bin_weights, constraints, bin_metadata):
    bin_weights = enforce_liquidity_reserve_only(bin_weights, constraints)
    bin_weights = enforce_manual_reserve_only(bin_weights, constraints)
    bin_weights, over_caps = enforce_per_bin_maximum(bin_weights, constraints)

    ok, reason = enforce_bin_count_and_overlap(bin_weights, bin_metadata)
    if not ok:
        raise ValueError(f"Bin overlap violation: {reason}")

    ok, reason = enforce_futures_allocation(bin_weights, bin_metadata)
    if not ok:
        raise ValueError(f"Futures exposure violation: {reason}")

    return bin_weights  # final output with all limits applied

