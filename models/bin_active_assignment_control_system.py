# Program: bin_active_assignment_control_system.py
# Author: Brian Anderson
# Origin Date: 10May2025
# Version: 1.0
#
# Purpose:
#    /Establish the mechanics on the apportionment of the trading account, by permissible patterns of segmentations,
#    /permissible amounts allocated per segmentation, segment margin spending limits, and responses when violated.

from date_time import datetime

from models import (golden_crossover_strategy_model(),
  iv_rank_options_trades_model(),
  options_expiry_pinning_model(),
  post_earnings_drift_model(),
  rsi_reversion_strategy_model(),
  skew_drift_signal_model(),
  spx_vix_divergence_model(),
  turn_of_month_effect_model(),
  twelve_one_momentum_model(),
  volatility_mean_reversion_model(),
  “…()”,
  “…()”,
  “…()”,
  “…()”,
  “…()”,
  “…()”,
  “…()”,
  “…()”,
  “…()”,
  “…()” ]

# from To_The_Moon.scanners import (cup and handle, pmcc, other...)


bin_apportionment_model_identity = [ “one”,”two”,”three”,”four”,”five”,”six”,”seven”,”eight”,”nine”,”ten”,
  ”eleven”,”twelve”,”thirteen”,”fourteen”,”fifteen”,”sixteen”,”seventeen”,”eighteen”,”nineteen”,”twenty”]

one = golden_crossover_strategy_model()
two = iv_rank_options_trades_model()
three = options_expiry_pinning_model()
four = post_earnings_drift_model()
five = rsi_reversion_strategy_model()
six = skew_drift_signal_model()
seven = spx_vix_divergence_model()
eight = turn_of_month_effect_model()
nine = twelve_one_momentum_model()
ten = volatility_mean_reversion_model()
eleven = “…()”
twelve = “…()”
thirteen = “…()”
fourteen = “…()”
fifteen = “…()”
sixteen = “…()”
seventeen = “…()”
eighteen = “…()”
nineteen = “…()”
twenty = “…()”


total_number_bins = len(bin_apportionment_model_identity)

'''

# rule 1 – 10% of account is to always be in liquid capital (cash, money market,…)

# rule 2 - 10% will be preserved for manual activation of selections, using an intuited approach to instrument choice.
# rule 2.a - In any one day, the active portion of manual choices should not be above 7.5% of the account.
# rule 2.b - In specific circumstances, the total non-margined value of manual actions should be no more than 10%.
#            This is delimited by the current open bin distributions for the day that are already open.

# rule 3 - The maximum percentage of any bin to be no more than 6%:
# rule 3.b – no bin, despite having 6% allocation, should be filled with more than 4.5% of the account equivalent
# of that bin assignment; e.g. for a $100,000 account, the maximum amount for one bin is $6000, but the maximum
# safe permitted utilization is $4500 for that bin.
# which is (80 to 82.5%, divided by 6%) = 13 bins maximum
# rule 3.c - The elements contributing to that 4.5%, for example, are to be weighted based on the expected margin that
# is typically required by the broker.  For example, for selling puts, the margin is 1.5x of the credit value.
# rule 3.d - The minimum percentage of any bin should be around 2.5% (with 1.75% max margin usage)
# which would permit 30 bins to be used--this offers a buffer of protection in times of illiquidity or shifted market dynamics.

# rule 4 - There are to be no more than 25 bins utilized in any single day period.
# rule 4.b - This is reduced to a maximum of 20 bins, if any bins have activity involving the same underlying equity.

# rule 5 - Futures involvement shall never breech 5% of the account at any time. Any combination of futures and
# future-like derivatives is not to have margin equivalent larger than 3.75% of the account, regardless of which
# bins they are in, or separately.

# rule 6 – Each option combination will have a margin multiplier that gives way for the same expected range of margin
# required by ikbr in order to support the options choice

# rule 7 – All options choices are to be logged in the bins in such as fashion, so that there is an assumed 1.5% slippage
# in each direction—accounting for worst case situations or drastic rebalancing actions.

# rule 8 – Rotation of bins shall not happen more than once every 24 hours, in a fashion identical to daytrading a cash
# account.  One round trip.  If there was none in the bin, and something was opened, then closed (whether partial or
# fully), then ...

# rule 9 – At midnight of the weekday trading day, the end-of-day account balance, and the bin PnL’s, will be used in reevaluating 
# the risk profile, and the next day’s permitted apportionments will be calculated.  Breaches of those new limits will cause
# the bin to close for the next day until the breach can be sealed—that is, actions are taken to lower the margin usage of the bin. 

# rule 10 – in order to maintain program integrity, bin assignments are permanent, in terms of bin numbers aligning with specific
# trading models.  E.g. an ‘iron cross’ will always stay as bin 12.  There is no limit on new models that can be added, nor number
# of bin assignments.

# rule 11 - The standard warning notification classification schemes, warning color expressions, and any interrelated logic, is to
remain persistent for a period of time proportionate to the rules for those color assignments.  When yellow, orange, red, shutout
tiered responses are to occur, with the requisite consequences if manipulated, overridden, or violated.

def evaluate_bin_safety(bin assignments, bin percentages, bin ...)

equity under consideration: {ticker}
ticker_list = ()
Equity_Overlap_between_Bins = ()
for i in bin_list() :
  for j in bin_list(bin(i)) :
    if {ticker}=(bin_list(bin(ticker))
      append.Equity_Overlap_between_Bins()
      overlapping_tickers =+ 1
      for k in Equity_Overlap_between_Bins()
        if {ticker} == Equity_Overlap_between_Bins(k)
          # overlapping_tickers... I'm lost here...  what do i do if in more than one bin, or more than two bins?
          return overlapping_tickers
        return Equity_Overlap_between_Bins()
      append.ticker_list = ({ticker)(i))}
      return Equity_Overlap_between_Bins()
    return overlapping_tickers
  return None
return None


def bin_apportionment_amount (...)
  max_permitted_per_bin = (0.06, 0.055, 0.05, 0.045, 0.04, 0.035, 0.03, 0.025) #eight scale downs available
  account_percentage_cum_total = sum (bin_1 + ... bin_n)
  if account_cum_total > 0.80 :
    max_permitted_pct_per_bin =- 1
    return None
  # something here
  # I am lost.  Should I adjust the whole assembly by crushing them all proportionately?
  # Should I check what can be squished first?
  # Should it be weighted by a normalization of (risk and volatility sensitivity)?
  # When should a new bin be permitted in? When opportunity is fiduciarily irresponsible not to take hold?
  # This needs significant work...

  
    
