# Module: enforce_allocation_rules_fullSet.py
# Author: Brian Anderson
# Origin Date: 11May2025
# Version: 1.3
#
# Purpose:
#    /Convert eleven necessary risk allocation rules into code-based enforcement mechanic.

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

# rule 6 – margin multiplier per strategy
# apply model-specific multiplier (e.g. selling puts = 1.5x exposure)
# this informs whether 4.5% actual allocation = 6.75% margin usage

# rule 7 – slippage buffer
# assume +1.5% for each options trade; ensure cumulative account use remains within envelope

# rule 8 – one bin rotation per day
# requires external state tracking: when was the bin last traded?
# if recent: deny rotation

# rule 9 – nightly rebalance
# external trigger re-evaluates account balance and usage
# if violations detected, mark bins as shut for next day

# rule 10 – model-bin mapping is fixed
# enforce that each bin number maps permanently to its assigned model name
# reject reassignment attempts

# rule 11 – warning color persistence
# if triggered, each warning state must persist for a defined duration (e.g. red = 2 days minimum)

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

# === With respect to rule number One ===

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

# === With respect to rule number Two ===

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

# === With respect to rule number Three ===

def enforce_per_bin_maximum(bin_weights, constraints):
    '''Rule 3 enforcement: enforce a per-bin maximum allocation'''
    max_bin = constraints['max_bin_weight']
    flagged_bins = []

    for bin_name, allocation in bin_weights.items():
        if allocation > max_bin:
            flagged_bins.append((bin_name, allocation))
            bin_weights[bin_name] = max_bin  # Cap it to the maximum

    return bin_weights, flagged_bins

# === With respect to rule number Four ===

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

# === With respect to rule number Five ===

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

# === PROCEED WITH RULES SIX THROUGH ELEVEN AS FOLLOWS ===

# === With respect to rule Six ===

def enforce_margin_multiplier(bin_weights, bin_metadata, constraints):
    '''Estimate margin exposure using each strategy's leverage multiplier'''
    total_margin_used = 0.0
    margin_threshold = 1.0 - constraints['liquidity_reserve'] - constraints['manual_trading_allocation']

    for bin_name, alloc in bin_weights.items():
        metadata = bin_metadata.get(bin_name, {})
        multiplier = metadata.get('margin_mult', 1.0)
        margin_used = alloc * multiplier
        total_margin_used += margin_used

    if total_margin_used > margin_threshold:
        return False, f"Estimated margin usage {total_margin_used:.2%} exceeds threshold {margin_threshold:.2%}"
    return True, None

# === With respect to rule Seven ===

def enforce_slippage_buffer(bin_weights, bin_metadata, constraints):
    '''Estimate total slippage impact for option bins'''
    slippage_per_option_bin = 0.015  # 1.5%
    estimated_slip = 0.0

    for bin_name in bin_weights:
        if bin_metadata.get(bin_name, {}).get('type') == 'options':
            estimated_slip += slippage_per_option_bin

    if estimated_slip > constraints.get('slippage_budget', 0.05):
        return False, f"Slippage risk exceeds buffer: {estimated_slip:.2%}"
    return True, None

# === With respect to rule Eight ===

def enforce_bin_rotation_lock(bin_metadata, current_date):
    '''Prevent bins from rotating more than once per day'''
    for bin_name, meta in bin_metadata.items():
        last_rotated = meta.get('last_rotation_date')
        if last_rotated == current_date:
            return False, f"Bin {bin_name} already rotated today"
    return True, None

# === With respect to rule Nine ===

def enforce_nightly_rebalance(bin_status_log):
    '''Placeholder – would be called externally overnight to apply persistent state changes'''
    for bin_name, status in bin_status_log.items():
        if status.get('violation_today'):
            status['active'] = False
            status['lock_until'] = status.get('date') + timedelta(days=1)
    return bin_status_log

# === With respect to rule Ten ===

def enforce_fixed_bin_model_mapping(bin_metadata, fixed_assignments):
    '''Each bin must retain its original model identity'''
    for bin_name, meta in bin_metadata.items():
        expected_model = fixed_assignments.get(bin_name)
        actual_model = meta.get('model')
        if actual_model != expected_model:
            return False, f"Bin {bin_name} assigned to unexpected model: {actual_model}"
    return True, None

# === With respect to rule Eleven ===

def enforce_warning_persistence(bin_alert_state, today_date):
    '''Ensure RED/YELLOW states persist for a minimum period'''
    required_persistence = {
        'red': 2,
        'yellow': 1
    }

    for bin_name, alert in bin_alert_state.items():
        level = alert.get('level')
        date_set = alert.get('since')
        days_elapsed = (today_date - date_set).days
        if level in required_persistence and days_elapsed < required_persistence[level]:
            return False, f"Bin {bin_name} must remain {level.upper()} for {required_persistence[level]} days"
    return True, None

# Note: There may be need, here, to collectively activate some mechanic of rules six through eleven.  Review them to be sure.
