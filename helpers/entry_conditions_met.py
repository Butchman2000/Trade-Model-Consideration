# Program: entry_conditions_met.py
# Author: Brian Anderson
# Origin Date: 11May2025
# Version: 1.3
#
# Purpose:
#   /Evaluate composite entry readiness based on multiple market signals.
#   /Requires EMA trend confirmation, VWAP proximity support, healthy volume,
#    and favorable sentiment alignment.
#   /Designed to be modular and reusable across different trading models.

# NOTES:
# - Can be used as a precondition filter in tactical or strategic systems.
# - Modularity supports pluggable signals and unit testability.
# - Optional logging shows which condition failed, for debugging or tuning.
# - Now includes metadata feedback for logging and analytics.
# - Extendable: can later accept threshold overrides or model-specific logic injections.

import numpy as np


def entry_conditions_met(current_date, data, sentiment_score=None,
                         ema_short='EMA_9', ema_long='EMA_20',
                         vwap_col='VWAP', vol_col='Volume',
                         vwap_proximity_threshold=0.01,
                         min_volume_percentile=0.8,
                         sentiment_ok_values=None,
                         logger=None,
                         return_metadata=False):
    """
    Evaluate whether entry conditions are met on the given day.

    Parameters:
    - current_date: datetime
    - data: pd.DataFrame with columns for EMA_9, EMA_20, VWAP, Volume, etc.
    - sentiment_score: float or str (optional sentiment rating)
    - ema_short / ema_long: column names for fast/slow EMAs
    - vwap_col: name of VWAP column
    - vol_col: name of volume column
    - vwap_proximity_threshold: max % distance allowed from VWAP to consider as 'support'
    - min_volume_percentile: min volume level as % of rolling mean (e.g., 0.8 = 80%)
    - sentiment_ok_values: list of allowed sentiment states (e.g., ['neutral', 'greed'])
    - logger: optional logging object
    - return_metadata: if True, returns (decision, metadata) tuple

    Returns:
    - decision: bool – True if all filters pass, else False
    - metadata: dict – Optional, includes status of each filter (if return_metadata=True)
    """
    metadata = {
        'ema_condition': False,
        'vwap_condition': False,
        'volume_condition': False,
        'sentiment_condition': False,
        'date_valid': current_date in data.index,
        'final_decision': False
    }

    def log(reason):
        if logger:
            logger.info(f"{current_date.date()} – entry failed: {reason}")

    if not metadata['date_valid']:
        log("date not in index")
        if return_metadata:
            return False, metadata
        return False

    row = data.loc[current_date]

    # EMA condition
    if row[ema_short] > row[ema_long]:
        metadata['ema_condition'] = True
    else:
        log(f"EMA condition failed: {ema_short}={row[ema_short]} <= {ema_long}={row[ema_long]}")
        if return_metadata:
            return False, metadata
        return False

    # VWAP proximity
    close_price = row['Close']
    vwap = row[vwap_col]
    vwap_distance = abs(close_price - vwap) / close_price
    if vwap_distance <= vwap_proximity_threshold:
        metadata['vwap_condition'] = True
    else:
        log(f"VWAP support failed: distance={vwap_distance:.4f} > threshold={vwap_proximity_threshold}")
        if return_metadata:
            return False, metadata
        return False

    # Volume check
    recent_volume = data[vol_col].rolling(20).mean()
    min_vol = recent_volume.loc[current_date] * min_volume_percentile
    green_candle = row['Close'] > row.get('Open', row['Close'])  # fallback if Open missing
    candle_body_pct = abs(row['Close'] - row.get('Open', row['Close'])) / row['Close']

    if row[vol_col] >= min_vol:
        metadata['volume_condition'] = True
    elif green_candle and candle_body_pct >= 0.01 and row[vol_col] >= 1_000_000:
        # Override for fast green squeeze candle with good volume baseline
        metadata['volume_condition'] = True
        log(f"Volume override: green candle with body {candle_body_pct:.2%} and volume {row[vol_col]:,.0f}")
    else:
        log(f"Volume too low: {row[vol_col]} < {min_vol:.0f}")
        if return_metadata:
            return False, metadata
        return False

    # Sentiment check
    if sentiment_score is not None and sentiment_ok_values:
        if sentiment_score in sentiment_ok_values:
            metadata['sentiment_condition'] = True
        else:
            log(f"Sentiment mismatch: score={sentiment_score} not in {sentiment_ok_values}")
            if return_metadata:
                return False, metadata
            return False
    else:
        # No sentiment filter applied
        metadata['sentiment_condition'] = True

    metadata['final_decision'] = True
    if logger:
        logger.info(f"{current_date.date()} – entry PASSED")

    if return_metadata:
        return True, metadata
    return True
