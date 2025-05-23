Program: date_time_ops_commander.py
Author: Brian Anderson
Origin Date: 10May2025
Version: 1.1
#
# Purpose:
#    /Establish and elucidate rules and action enabling/disabling, for different days and specific times.
#    /E.g, at 4:15 am on a Tuesday, pre-market: no trading of stocks, no options,
#    /but asian-open mode for futures which is open for trading at that point.
#    /This checks against the exclusion list for the year in which the program checks.

# NOTE: There is extensive idea development at the bottom, in the form of TODO.

from date_time import datetime
from exclusions.exclusions_2025 import (    #change the year as needed
    is_valid_trading_day,
    exit_time_on_fomc_day,
    exit_time_on_half_day,
    powell_speech_blackout,
    quad_witching_exit_time,
    nfp_trading_restrictions,
    election_day_halt
    )
    # may need a line for when any of these dont exist; e.g. there is no election in 2025


def stock_price_division(stuff here…):
  Stock_Price_Small = [ 
    “Small Penny”, 0.40, 1.95;
    “Medium Penny”, 1.96, 4.95;
    “Large Penny”, 96, 17.95]
  Stock_Price_Medium = [
    “Smaller Medium”, 17.96, 37.95;
    “Larger Medium”, 37.96, 72.49]
  Stock_Price_Large = [
	  “Large, 1of4”, 72.50, 149.95;
    “Large, 2of4”, 149.96, 299.95;
    “Large, 3of4”, 299.96, 499.95;
    “Large, 4of4”, 499.96, 799.95]
  Stock_Price_Huge = [
    “Smaller Huge”, 799.96, 1499.95;
    “Larger Huge:, 1499.96, 9995.00]


def division_of_time_based_operation (put stuff here...) :
  # assign the defaults:
  stock_trading_timeperiod = str()
  stock_trading_algo_main = (stock_trading_turned_off,0)
  options_trading_algo = (options_trading_turned_off,0)
  futures_trading_algo = (futures_trading_turned_off,0)
  # I might need to tuple everything below as well, depending on what we need to do

  current_time = datetime(now)
  # convert to EST if needed
  Wait(60)
  While(current_time ~= previous_time) :    return current_time… advance the time

  if date_today is not in (Monday, Tuesday, Wednesday, Thursday, Friday) :
	  stock_trading_timeperiod = “Stock market asleep for the weekend… zzz...”
    if date_today is (Sunday) and current_time > 18:00:00 :
		  stock_trading_timeperiod() = “Market is asleep, futures awake.”
		  stock_trading_algo_main_status() = stock_trading_turned_off
		  options_trading_algo_status() = options_trading_turned_off
		  futures_trading_algo_status() = futures_trading_preMonday_mode
      return (all the above stuff)
	
    # Else… (if Saturday or Sunday, before 6pm on Sunday)
	  stock_trading_timeperiod() = “Everything is asleep for now.  Chill out.”
	  stock_trading_algo_main_status() = stock_trading_turned_off
	  options_trading_algo_status() = options_trading_turned_off
	  futures_trading_algo_status() = futures_trading_turned_off
    return (all the above stuff)

  #if date_today is in (Monday(),Tuesday(),Wednesday(),Thursday(),Friday())
	if date_today is not in (excluded_dates({current_year}) :
		if date_today is not in (excluded_times({current_year}) :
			weekday_market_machine()
			is_weekday_and_not_excluded_date_or_time = True
		return is_weekday_and_not_excluded_date_or_time
  return None

# NOTE: may be able to bypass this with:
‘’’
from exclusions.exclusions_2024 import (    #change the year as needed
    is_valid_trading_day,
    exit_time_on_fomc_day,
    exit_time_on_half_day,
    powell_speech_blackout,
    quad_witching_exit_time,
    nfp_trading_restrictions,
    election_day_halt
‘’’


def weekday_market_machine(current_time, previous_time, date_today) :
	# just to triple check:
	While (is_weekday_and_not_excluded_date_and_time == True) :
	#indent all the rest below:
  if current_time >= 00:00:00 and current_time < 02:00:00 :
		market_trading_timeperiod = “Market is asleep, slow futures… zzz …”
		stock_trading_algo_main = stock_trading_turned_off
		options_trading_algo = options_trading_turned_off
		futures_trading_algo = futures_trading_afterhours_gentle_mode
	# in futures program, give ourselves some room to breathe 2 min before and after Asian futures sleepy time
    return (all the above stuff)

  if (current_time >= 02:00:00 and current_time < 04:00:00)
		market_trading_timeperiod = “Market is asleep, Asia futures is asleep”
		stock_trading_algo_main = stock_trading_turned_off
		options_trading_algo = options_trading_turned_off
		futures_trading_algo = futures_trading_afterhours_AsiaOff_mode
    return (all the above stuff)

  if 04:00:00 <= current_time < 07:00:00 :
	  stock_trading_timeperiod = “Pre-Market, early morning, be patient!”
	  print(f”Market Status:  Early Market Hours, no trading available”)
	  stock_trading_algo_main = stock_trading_turned_off
	  options_trading_algo = options_trading_turned_off
	  futures_trading_algo = futures_trading_premarket_mode  
    return (all the above stuff)

  if 07:00:00 <= current_time < 09:00:00 :
	  stock_trading_timeperiod = “Pre-Market activity open, get ready…!”
	  print(f”Market Status:  Early Market Hours trading is currently open”)
	  stock_trading_algo_main = stock_trading_premarket_mode
	  options_trading_algo = options_trading_turned_off
	  futures_trading_algo = futures_trading_premarket_mode
    return (all the above stuff)

  if 09:00:00 <= current_time < 09:30:00 :
	  stock_trading_timeperiod = “30 minutes left until the bell, get set…!”
	  print(f”Market Status:  Early Market Hours + early options is open”)
	  stock_trading_algo_main = stock_trading_premarket_mode()
	  options_trading_algo = options_trading_premarket_mode()
	  futures_trading_algo = futures_trading_turned_on()
    return (all the above stuff)
  
  if 09:30:00 <= current_time < 16:00:00 :
	  stock_trading_timeperiod = “Market Open! GO GO GO!!!”
	  print(f”Market Status:  Market Open”)
	  stock_trading_algo_main = stock_trading_market_mode
	  options_trading_algo = options_trading_market_mode
	  futures_trading_algo = futures_trading_turned_on
    return (all the above stuff)

  if 16:00:00 <= current_time < 16:15:00 :
	  stock_trading_timeperiod = “Post Market Hours, Limited options window”
	  print(f”Market Status:  Afterhours… options afterhours”)
	  stock_trading_algo_main = stock_trading_afterhours_mode
	  options_trading_algo = options_trading_afterhours_mode
	  futures_trading_algo = futures_trading_turned_on
    return (all the above stuff)

  if 17:00:00 <= current_time < 18:00:00 :
	  stock_trading_timeperiod = “Post Market Hours, Options post market window”
	  print(f”Market Status:  Afterhours, American futures market closed”)
	  stock_trading_algo_main = stock_trading_afterhours
	  options_trading_algo = options_trading_turned_afterhours
	  futures_trading_algo = futures_trading_closed
    return (all the above stuff)

 
# Sunday 6pm to Friday 5pm, futures is open,
# with the exception from 5 pm to 6 pm (EST), wherein my access to the futures market closes 
  if 17:00:00 <= current_time < 18:00:00 :  # give futures a 2 minute window for safety
	  stock_trading_timeperiod = “Post Market Hours, Options post market window”
	  print(f”Market Status:  Afterhours… options afterhours”)
	  stock_trading_algo_main = stock_trading_turned_afterhours
	  options_trading_algo = options_trading_turned_afterhours
	  futures_trading_algo = futures_trading_turned_on
    return (all the above stuff)
  
  if 16:15:00 <= current_time < 20:00:00 :
		stock_trading_timeperiod = “Post Market Hours, options closed”
		print(f”Market Status:  Afterhour trading, options closed”)
		stock_trading_algo_main = stock_trading_afterhours
		options_trading_algo = options_trading_turned_off
		futures_trading_algo = futures_trading_turned_on
    return (all the above stuff)

	if 00:00:00 <= current_time < 04:00:00 or
    (current_time >20:00:00) :
		market_trading_timeperiod = “Market is asleep, slow futures… zzz …”
		stock_trading_algo_main = stock_trading_turned_off
		options_trading_algo = options_trading_turned_off
		futures_trading_algo = futures_trading_afterhours_gentle_mode


'''
Considerations:
Continuance? News? Pre-market anomalous?
Volume, IV(?), jumps, patterns?
Trend following from day(s) before?
what could come if catches up with trend from before?
Volume multiple day(s) before? (other than continuance)
So multi day computation is needed
RSI? Change in it?
Futures equivalence?
Move pre-market: pk to peak 2x of that value from previous days
Move pre-mark >5% for (bid-ask close stocks, only)
Open >12% in some fashion
Open >15% from market open within 1 hour window moving forward
Or >8% after >5% previous hour,
Or >22% anytime after open
Predicated on acceptable open price (avg bid-ask) and reasonable spread
For price>0.40,
Any>30% from market open
For price>12, any >15%,
For price>25, any > 8%,
For price>55, any >5.5%

 
TO DO:
Anything other than pk to pk noise? Like usp noise?

 
Maybe consider this as deviation from the others in its sector or something
Need length of time to measure over, conditions for self picking of range of time to choose (possible deconvolution from volume), and threshold value to report
 
May have to consider peak detection methodology lie empower does, via their traditional or auto-thing mode.
Calculation of first derivative of price action, of action difference from volume-weighted segment, of delta-volume dependent action, and of delta-volume dependent action difference from (regular or delta-weighted) volume weighted segment.
Calc of second derivative (convoluted from the first derivative considerations) x the additional 5.  Is this 2^5? or 5x5?  I think this is 5x5.
Need methodology for empower like processing, for liftoff and touchdown maybe, and inibit and draw baseline and the rest.  Need mechanism for tuning it as well.
Todo at later time: an analogous peak purity equivalent calculation: autothreshold, solvent, noise, noise+solvent (see waters webpage)

For first derivative of points:
 Use numpy.gradient (best option)
Most people want this. This is now the Numpy provided finite difference aproach (2nd-order accurate.) Same shape-size as input array.
Uses second order accurate central differences in the interior points and either first or second order accurate one-sides (forward or backwards) differences at the boundaries. The returned gradient hence has the same shape as the input array.
2. Use numpy.diff (you probably don't want this)
If you really want something ~twice worse this is just 1st-order accurate and also doesn't have same shape as input. But it's faster than above (some little tests I did).
For constant space between x sampless
import numpy as np 
dx = 0.1; y = [1, 2, 3, 4, 4, 5, 6] # dx constant
np.gradient(y, dx) # dy/dx 2nd order accurate
array([10., 10., 10.,  5.,  5., 10., 10.])
For irregular space between x samples
import numpy as np
x = [.1, .2, .5, .6, .7, .8, .9] # dx varies
y = [1, 2, 3, 4, 4, 5, 6]
np.gradient(y, x) # dy/dx 2nd order accurate
array([10., 8.333..,  8.333.., 5.,  5., 10., 10.])
What are you trying to achieve?
The numpy.gradient offers a 2nd-order and numpy.diff is a 1st-order approximation schema of finite differences for a non-uniform grid/array. But if you are trying to make a numerical differentiation, a specific finite differences formulation for your case might help you better. You can achieve much higher accuracy like 8th-order (if you need) much superior to numpy.gradient.
 
https://github.com/chemplexity/chromatography/blob/master/Methods/Integration/PeakDetection.m 
https://github.com/chemplexity/chromatography/blob/master
https://fityk.nieto.pl/fityk-manual.html
https://github.com/niuchuangnn/noise2sim/blob/master/README.md

what if a github as facebook copyright?

Extended rBergomi smile/skew separation:
https://github.com/freephys/extended_rbergomi/blob/master/README.md
https://github.com/alichopping/Heston-Model/blob/main/Smiles.png
(calc smile and skew graph stuffs;  really good iv model. May want to see deviations of actual options surface against this simulation/actual model)
https://hal.science/hal-02118508/file/ProceduralPhasorNoise.pdf

'''
