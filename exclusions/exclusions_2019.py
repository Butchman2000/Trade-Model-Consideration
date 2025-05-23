# Program: exlusions_2019.py
# Author: Brian Anderson
# Origin Date: 30April2025
# Version: 1.0
# 
# Purpose:
#    /Backtest exclusion criterion for the year of 2019
#    /Assemble market dates for critical days that most strongly affect market activity.
#    /Specifies spans of time for which alteration of trading activity should be considered.

from datetime import datetime, time

# CPI release dates for 2019
Date_CPI_Releases_2019 = [
    datetime(2019, 1, 11), datetime(2019, 2, 13), datetime(2019, 3, 12), datetime(2019, 4, 10),
    datetime(2019, 5, 10), datetime(2019, 6, 12), datetime(2019, 7, 11), datetime(2019, 8, 13),
    datetime(2019, 9, 12), datetime(2019, 10, 10), datetime(2019, 11, 13), datetime(2019, 12, 11)
]

# FOMC announcement dates for 2019
Date_FOMC_Announcements_2019 = [
    datetime(2019, 1, 30), datetime(2019, 3, 20), datetime(2019, 5, 1), datetime(2019, 6, 19),
    datetime(2019, 7, 31), datetime(2019, 9, 18), datetime(2019, 10, 30), datetime(2019, 12, 11)
]

# Powell speeches in 2019 (partial list)
Date_Powell_Speeches_2019 = [
    datetime(2019, 1, 4), datetime(2019, 2, 26), datetime(2019, 6, 25), datetime(2019, 8, 23),
    datetime(2019, 10, 8), datetime(2019, 11, 13)
]

# Market half-days in 2019
Date_Market_HalfDays_2019 = [
    datetime(2019, 7, 3), datetime(2019, 11, 29), datetime(2019, 12, 24)
]

# Last trading day of each month in 2019
Date_Last_Trading_Days_2019 = [
    datetime(2019, 1, 31), datetime(2019, 2, 28), datetime(2019, 3, 29), datetime(2019, 4, 30),
    datetime(2019, 5, 31), datetime(2019, 6, 28), datetime(2019, 7, 31), datetime(2019, 8, 30),
    datetime(2019, 9, 30), datetime(2019, 10, 31), datetime(2019, 11, 29), datetime(2019, 12, 31)
]

# Quad Witching Dates 2019
Date_Quad_Witching_2019 = [
    datetime(2019, 3, 15), datetime(2019, 6, 21), datetime(2019, 9, 20), datetime(2019, 12, 20)
]

# NFP Fridays 2019 (1st Friday each month approx.)
Date_NFP_2019 = [
    datetime(2019, 1, 4), datetime(2019, 2, 1), datetime(2019, 3, 8), datetime(2019, 4, 5),
    datetime(2019, 5, 3), datetime(2019, 6, 7), datetime(2019, 7, 5), datetime(2019, 8, 2),
    datetime(2019, 9, 6), datetime(2019, 10, 4), datetime(2019, 11, 1), datetime(2019, 12, 6)
]

# Election Day (not applicable in 2019)
Date_Election_2019 = None

# Jackson Hole 2019 note (no action taken)
# Jackson Hole 2019 occurred around August 22–24

# Combine all exclusion dates into a set for faster lookup
exclusion_dates = set(
    Date_CPI_Releases_2019 +
    Date_FOMC_Announcements_2019 +
    Date_Powell_Speeches_2019 +
    Date_Market_HalfDays_2019 +
    Date_Last_Trading_Days_2019
)

# Function to filter out exclusion dates
def is_valid_trading_day(date):
    return date not in exclusion_dates

# Function to determine if trades should be exited early on FOMC days
def exit_time_on_fomc_day(date):
    fomc_dates_only = {d.date() for d in Date_FOMC_Announcements_2019}
    if date.date() in fomc_dates_only:
        return (time(13, 45), time(18, 0))
    return None

# Function to determine if it's a market half-day and when trades should be exited
def exit_time_on_half_day(date):
    half_day_dates_only = {d.date() for d in Date_Market_HalfDays_2019}
    if date.date() in half_day_dates_only:
        return (time(11, 45), datetime(date.year, date.month, date.day + 1, 7, 0))
    return None

# Function for Powell speech day trade halt
def powell_speech_blackout(date):
    powell_dates_only = {d.date() for d in Date_Powell_Speeches_2019}
    if date.date() in powell_dates_only:
        return (time(14, 15), time(18, 0))
    return None

# Function for quad witching day early exit
def quad_witching_exit_time(date):
    quad_dates_only = {d.date() for d in Date_Quad_Witching_2019}
    if date.date() in quad_dates_only:
        return (time(13, 0), datetime(date.year, date.month, date.day + 1, 7, 0))
    return None

# Function for NFP timing restrictions
def nfp_trading_restrictions(date):
    nfp_dates_only = {d.date() for d in Date_NFP_2019}
    if date.date() in nfp_dates_only:
        return (None, time(10, 30))
    elif any((date - d).days == -1 for d in Date_NFP_2019):
        return (time(15, 15), None)
    return None

# Function for election day full halt
def election_day_halt(date):
    if Date_Election_2019 and date.date() == Date_Election_2019.date():
        return (None, datetime(date.year, date.month, date.day + 1, 7, 0))
    return None
