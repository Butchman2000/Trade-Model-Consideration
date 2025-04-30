# Module Program: universe_filtering.py
# Author: Brian Anderson
# Origin Date: 30April2025
# Version: 1.0
#
# Purpose:
#    /Dynamically build a filtered list of tradable stock tickers, based on liquidity, price, market cap, and other rules.
#    /Median assignment of average price during noisy sessions, or extreme quoted price deviations are handled.

import yfinance as yf
import pandas as pd


def get_filtered_universe(as_of_date, min_dollar_vol=18_000_000, min_price=9.50, min_cap=700_000_000,
                          min_days_since_ipo=252, min_std=0.01, max_std=0.08,
                          min_valid_price=1.00, max_valid_price=2000.00):
    """
    Generate a filtered list of tickers based on trading, liquidity, volatility, and listing constraints.

    Parameters:
    - as_of_date: datetime
    - min_dollar_vol: minimum average daily dollar volume in past month
    - min_price: minimum closing price (for trade eligibility)
    - min_cap: minimum market cap (placeholder; real implementation would need fundamentals data)
    - min_days_since_ipo: IPO must be older than this many trading days
    - min_std, max_std: filter on 30-day return std dev for volatility window
    - min_valid_price, max_valid_price: hard price cutoff to eliminate price spikes, glitches, or reverse splits

    Returns:
    - List of tickers passing all filters
    """
  
    # Placeholder universe for testing; in production, replace with something like S&P1500 or full NASDAQ
    universe = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "JPM", "CVNA", "PLTR"]

    end = as_of_date.strftime("%Y-%m-%d")
    start = (as_of_date - pd.Timedelta(days=40)).strftime("%Y-%m-%d")

    data = yf.download(universe, start=start, end=end, interval='1d', auto_adjust=True)['Adj Close']
    volume = yf.download(universe, start=start, end=end, interval='1d')['Volume']

    filtered = []
    for ticker in universe:
        try:
            # Drop NAs
            px = data[ticker].dropna()
            vol = volume[ticker].dropna()
            if len(px) < min_days_since_ipo:
                continue

            # Check for abnormal price behavior (glitches or splits)
            if px.max() > max_valid_price or px.min() < min_valid_price:
                print(f"[NOISE] {ticker} skipped due to extreme price values:")
                print(f"[NOISE] {ticker} min={px.min():.2f}, max={px.max():.2f}")
                continue

            # Average daily dollar volume = price * volume
            avg_dollar_vol = (px * vol).mean()
            if avg_dollar_vol < min_dollar_vol:
                continue

            # Last closing price check
            last_price = px.iloc[-1]  # iloc[-1] gets the most recent (last) entry in the series
            if last_price < min_price:
                continue

            # 30-day volatility filter (standard deviation of daily returns)
            daily_returns = px.pct_change().dropna()
            std_30 = daily_returns[-30:].std()
            # Note: [-30:] slices the last 30 rows (the most recent 30 days)
            if not (min_std <= std_30 <= max_std):
                continue

            # Additional spike filter using Z-score of daily returns
            mean_ret = daily_returns.mean()
            std_ret = daily_returns.std()
            z_scores = (daily_returns - mean_ret) / std_ret # a factor of deviation
            max_z = z_scores.abs().max()
            if max_z > 5:  # consider 5+ std devs from mean as likely abnormal
                print(f"[Z-FLAG] {ticker} max z-score = {max_z:.2f}, flagged as abnormal")
                continue

            # If we had fundamentals, (or when we get there), we would/will also check:
            # contition: is_optionable (requires external data)
            # condition: not OTC (check exchange symbol)
            # condition: market cap > threshold (requires a fundamentals API)
            # I am separately working on an API, but will need much more time to finish.

            filtered.append(ticker)

        except Exception as e:
            print(f"[WARN] Skipped {ticker}: {e}")
            continue

    return filtered
