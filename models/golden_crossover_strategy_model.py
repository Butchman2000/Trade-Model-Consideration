# Program: golden_cross_strategy_model.py
# Author: Brian Anderson
# Origin Date: 01May2025
# Version: 1.4
#
# Purpose:
#   - Evaluate a classic moving average crossover strategy (Golden Cross)
#   - Apply VIX-based whipsaw filtering to avoid entering trades during high-volatility regimes
#   - Introduce dynamic position sizing based on macro (Golden Cross) vs. tactical entry filters
#   - Ensure signal compliance and system auditability

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Custom module for exclusion logic
from utils.exclusion_tools import should_trade_on
# Import externalized whipsaw filter
from helpers.volatility_filters import vix_whipsaw_filter
# Import tactical entry filter
from helpers.entry_conditions_helper import entry_conditions_met

'''
INSTRUCTIONS:
To make vix_whipsaw_filter work as a reusable helper, ensure the following inside utils/volatility_filters.py:

1. The function definition remains exactly as:
   def vix_whipsaw_filter(current_date, vix_data, state):

2. It must not rely on external script-level state. Everything passed explicitly.

3. Required dependencies in that module:
   import pandas as pd
   from datetime import timedelta

4. If used for logging or diagnostics, consider injecting a logging interface optionally
   (not required for this version).

5. Optional: Add unit tests to tests/test_volatility_filters.py to ensure regressions don’t
   break core functionality.
'''

# === Download SPY and VIX Data ===
ticker = 'SPY'
vix_ticker = '^VIX'

spy_data = yf.download(ticker, start='2000-01-01', end='2025-05-01')
vix_data = yf.download(vix_ticker, start='2000-01-01', end='2025-05-01')

spy_data = spy_data['Close'].copy()
vix_data = vix_data['Close'].copy()

# === Compute Moving Averages ===
data = pd.DataFrame(index=spy_data.index)
data['Close'] = spy_data
data['SMA_50'] = spy_data.rolling(50).mean()
data['SMA_200'] = spy_data.rolling(200).mean()
data['EMA_9'] = spy_data.ewm(span=9).mean()
data['EMA_20'] = spy_data.ewm(span=20).mean()
data['VWAP'] = spy_data.rolling(5).mean()  # Placeholder for real VWAP logic
data['Volume'] = 1000000  # Placeholder: inject real volume if available
data.dropna(inplace=True)

# === Initialize State and Generate Signals ===
data['Position'] = 0
position = 0
state = {}  # VIX regime state holder

for current_date in data.index:
    if not should_trade_on(current_date):
        continue

    # Evaluate volatility regime
    regime, state = vix_whipsaw_filter(current_date, vix_data, state)
    if regime != 'normal':
        continue  # Skip trading during yellow/red light regimes

    short_ma = data.loc[current_date, 'SMA_50']
    long_ma = data.loc[current_date, 'SMA_200']
    golden_cross_active = short_ma > long_ma

    # Tactical filter (entry gating based on VWAP, EMA(9/20), etc.)
    sentiment_today = 'neutral'  # Placeholder: integrate actual sentiment source
    if not entry_conditions_met(current_date, data, sentiment_score=sentiment_today):
        continue  # Skip if tactical entry gates not satisfied

    # Entry signal: Golden Cross (macro trend confirmation)
    if short_ma > long_ma and position == 0:
        position = 1  # Full/ramped position
        data.at[current_date, 'Position'] = position

    # Tactical entry without Golden Cross (macro trend not confirmed)
    elif short_ma <= long_ma and position == 0:
        position = 0.5  # Smaller tactical position
        data.at[current_date, 'Position'] = position

    # Exit signal: Death Cross
    elif short_ma < long_ma and position > 0:
        position = 0
        data.at[current_date, 'Position'] = position

    # Hold current position if no new signal
    else:
        data.at[current_date, 'Position'] = position

# === Final Output Preview ===
print(data.tail())
