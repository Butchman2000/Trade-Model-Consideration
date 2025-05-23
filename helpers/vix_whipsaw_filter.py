# Program: vix_whipsaw_filter.py
# Author: Brian Anderson
# Origin Date: 30April2025
# Version: 1.1
#
# Purpose:
#   /An advanced, state-aware volatility filter that uses tiered logic.
#   /It monitors for large drops and subsequent rebounds in VIX.
#   /Manages yellow-light and red-light regimes with cooldown enforcement.
#   /Used across multiple trading modules; externalized for reuse and auditability.

# NOTES:
# - This helper is used across multiple modules. Avoid coupling to any one strategy logic.
# - Default thresholds are safe but configurable per strategy instance.
# - Logger integration is optional; used for audit trails or runtime diagnostics.
# - All state is passed in explicitly to ensure isolation and reusability.
# - Returns 'normal' if data is missing or no triggers fire — this acts as a fail-safe.
# - Red-light regime takes full precedence over yellow/cooldown logic.
# - Extendable: can later support weighted VIX composites, intraday resolution, etc.
# - Ideal for test scaffolds: use synthetic VIX data for deterministic validation.
# - When testing, ensure each trigger path (yellow, red, revert, cooldown) is hit at least once.

import pandas as pd
from datetime import timedelta

def vix_whipsaw_filter(current_date, vix_data, state):
    """
    Evaluates whether VIX behavior triggers yellow or red regime changes.

    Parameters:
    - current_date: datetime
    - vix_data: pd.Series (daily VIX close values)
    - state: dict tracking:
        - cooldown_until
        - observation_day
        - red_light_until
        - red_count
        - volatility_floor

    Returns:
    - decision: str
        One of the following regime indicators:
        - 'normal' – No filter triggered; system may trade.
        - 'cooling_triggered' – Yellow light anomaly detected; pending rebound test.
        - 'cooldown_active' – Rebound confirmed; trades suppressed during cool-off.
        - 'red_watch_triggered' – Large VIX drop observed; watching for dangerous rebound.
        - 'red_light_active' – Confirmed volatility spike; trading halted for multiple days.
        - 'revert_to_strict' – Rebound after yellow anomaly confirmed; enter cooldown.
    - updated state: dict
        The internal filter state after applying current date logic.
    """

    # Safety check: skip if data is missing for current date
    if current_date not in vix_data.index:
        return 'normal', state

    # === Red light logic overrides everything ===
    if state.get('red_light_until') and current_date <= state['red_light_until']:
        current_vix = vix_data.loc[current_date]

        # Define recent 3-week window for volatility floor check
        recent_window = vix_data[current_date - timedelta(days=21):current_date]
        three_week_low = recent_window.min() if not recent_window.empty else current_vix
        volatility_floor = min(three_week_low, 38)  # Additional hard threshold floor

        if current_vix < volatility_floor:
            # Exit red regime if volatility recovers
            state.pop('red_light_until', None)
            state.pop('volatility_floor', None)
            return 'normal', state
        else:
            # Continue red regime and update stored floor
            state['volatility_floor'] = volatility_floor
            return 'red_light_active', state

    # === Yellow light cooldown logic ===
    if state.get('cooldown_until') and current_date <= state['cooldown_until']:
        return 'cooldown_active', state

    # === Get today and yesterday's VIX for comparison ===
    today_vix = vix_data.loc[current_date]
    idx = vix_data.index.get_loc(current_date)
    if idx == 0:
        return 'normal', state  # No previous day to compare against

    prev_date = vix_data.index[idx - 1]
    prev_vix = vix_data.loc[prev_date]

    # === Yellow light trigger (8% drop, VIX > 30) ===
    drop_pct = (prev_vix - today_vix) / prev_vix
    if prev_vix > 30 and drop_pct > 0.08:
        state['observation_day'] = current_date + timedelta(days=1)
        state['last_trigger_day'] = current_date
        return 'cooling_triggered', state

    # === Red light trigger (any 7% drop followed by 4% rebound) ===
    if drop_pct > 0.07:
        state['observe_red_on'] = current_date + timedelta(days=1)
        state['red_watch'] = True
        return 'red_watch_triggered', state

    # === Handle yellow observation logic ===
    if state.get('observation_day') == current_date:
        rebound_pct = (today_vix - prev_vix) / prev_vix
        if rebound_pct >= 0.045:
            # Confirmed rebound, activate cooldown
            state['cooldown_until'] = current_date + timedelta(hours=72)
            state.pop('observation_day', None)
            return 'revert_to_strict', state
        else:
            # Observation failed, return to normal
            state.pop('observation_day', None)
            return 'normal', state

    # === Handle red observation logic ===
    if state.get('observe_red_on') == current_date and state.get('red_watch'):
        rebound_pct = (today_vix - prev_vix) / prev_vix
        if rebound_pct >= 0.04:
            # Escalate to red if rebound occurs after drop
            state['red_count'] = state.get('red_count', 0) + 1
            cooldown_hours = 72 if state['red_count'] == 1 else 144
            state['red_light_until'] = current_date + timedelta(hours=cooldown_hours)
            state['red_watch'] = False
            state.pop('observe_red_on', None)
            return 'red_light_active', state
        else:
            # No escalation, dismiss red watch
            state['red_watch'] = False
            state.pop('observe_red_on', None)
            return 'normal', state

    # === Default regime ===
    return 'normal', state
