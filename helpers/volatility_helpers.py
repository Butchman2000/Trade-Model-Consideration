# Program: volatility_helpers.py
# Author: Brian Anderson
# Origin Date: 01May2025
# Version: 1.0
#
# Purpose:
#    /Establish supporting functions for advanced VIX/SPY filtering in divergence or
#    /volatility-aware strategies.

import pandas as pd

def add_multiday_confirmation(data, vix_days=3, vix_threshold=0.10):
    """
    Adds a column to confirm VIX rising across a short time window.

    Parameters:
        data: DataFrame with 'VIX_Change' column.
        vix_days: number of rolling days to check for net VIX increase.
        vix_threshold: minimum net increase to confirm volatility stress.

    Returns:
        DataFrame with new column 'VIX_Confirm'.
    """
    data['VIX_Confirm'] = data['VIX_Change'].rolling(vix_days).sum() > vix_threshold
    return data


def add_vix_term_structure(data, vix_front, vix_3m):
    """
    Adds a column to flag VIX term structure inversion (short-term > long-term).

    Parameters:
        data: main DataFrame with dates.
        vix_front: Series of VIX index (e.g., ^VIX).
        vix_3m: Series of 3-month VIX index (e.g., ^VIX3M).

    Returns:
        DataFrame with new column 'Term_Inversion'.
    """
    combined = pd.DataFrame({
        'VIX_Front': vix_front,
        'VIX_3M': vix_3m
    }).dropna()

    combined['Term_Inversion'] = combined['VIX_Front'] > combined['VIX_3M']

    data = data.join(combined['Term_Inversion'], how='left')
    data['Term_Inversion'].fillna(False, inplace=True)
    return data


def add_stress_regime_flag(data, vix_series, threshold=60, min_duration=3):
    """
    Flags periods of extreme stress where VIX exceeds a threshold for multiple days.

    Parameters:
        data: DataFrame to annotate.
        vix_series: Series of VIX values.
        threshold: stress threshold level for VIX.
        min_duration: consecutive days above threshold to qualify.

    Returns:
        DataFrame with new column 'Stress_Regime'.
    """
    # Identify stress days (True if VIX > threshold)
    is_stressed = vix_series > threshold

    # Convert boolean to integer (True = 1, False = 0)
    stressed_int = is_stressed.astype(int)

    # Identify groupings of consecutive True values using cumsum on ~is_stressed
    group_id = (~is_stressed).cumsum()

    # Within each group, count consecutive days of stress using cumsum again
    stress_streak = stressed_int.groupby(group_id).cumsum()

    # Then, flag regimes where the count exceeds minimum duration
    data['Stress_Regime'] = stress_streak >= min_duration
    return data
