# Program: exclusions_2021.py
# Author: Brian Anderson
# Origin Date: 30April2025
# Version: 1.0
# 
# Purpose:
#    /Backtest exclusion criterion for the year of 2021
#    /Assemble market dates for critical days that most strongly affect market activity.
#    /Specifies spans of time for which alteration of trading activity should be considered.

from datetime import datetime, time

# CPI release dates for 2021
Date_CPI_Releases_2021 = [
    datetime(2021, 1, 13), datetime(2021, 2, 10), datetime(2021, 3, 10), datetime(2021, 4, 13),
    datetime(2021, 5, 12), datetime(2021, 6, 10), datetime(2021, 7, 13), datetime(2021, 8, 11),
    datetime(2021, 9, 14), datetime(2021, 10, 13), datetime(2021, 11, 10), datetime(2021, 12, 10)
]

# FOMC announcement dates for 2021
Date_FOMC_Announcements_2021 = [
    datetime(2021, 1, 27), datetime(2021, 3, 17), datetime(2021, 4, 28), datetime(2021, 6, 16),
    datetime(2021, 7, 28), datetime(2021, 9, 22), datetime(2021, 11, 3), datetime(2021, 12, 15)
]

# Powell speeches in 2021 (partial list)
Date_Powell_Speeches_2021 = [
    datetime(2021, 2, 23), datetime(2021, 3, 4), datetime(2021, 8, 27), datetime(2021, 9, 22),
    datetime(2021, 11, 30)
]

# Market half-days in 2021
Date_Market_HalfDays_2021 = [
    datetime(2021, 7, 2), datetime(2021, 11, 26), datetime(2021, 12, 24)
]

# Last trading day of each month in 2021
Date_Last_Trading_Days_2021 = [
    datetime(2021, 1, 29), datetime(2021, 2, 26), datetime(2021, 3, 31), datetime(2021, 4, 30),
    datetime(2021, 5, 28), datetime(2021, 6, 30), datetime(2021, 7, 30), datetime(2021, 8, 31),
    datetime(2021, 9, 30), datetime(2021, 10, 29), datetime(2021, 11, 30), datetime(2021, 12, 31)
]

# Quad Witching Dates 2021
Date_Quad_Witching_2021 = [
    datetime(2021, 3, 19), datetime(2021, 6, 18), datetime(2021, 9, 17), datetime(2021, 12, 17)
]

# NFP Fridays 2021 (1st Friday each month approx.)
Date_NFP_2021 = [
    datetime(2021, 1, 8), datetime(2021, 2, 5), datetime(2021, 3, 5), datetime(2021, 4, 2),
    datetime(2021, 5, 7), datetime(2021, 6, 4), datetime(2021, 7, 2), datetime(2021, 8, 6),
    datetime(2021, 9, 3), datetime(2021, 10, 8), datetime(2021, 11, 5), datetime(2021, 12, 3)
]

# Election Day (not applicable in 2021)
Date_Election_2021 = None

# Jackson Hole 2021 note (no action taken)
# Jackson Hole 2021 occurred around August 26–28

# Combine all exclusion dates into a set for faster lookup
exclusion_dates = set(
    Date_CPI_Releases_2021 +
    Date_FOMC_Announcements_2021 +
    Date_Powell_Speeches_2021 +
    Date_Market_HalfDays_2021 +
    Date_Last_Trading_Days_2021
)

# Function to filter out exclusion dates
def is_valid_trading_day(date):
    return date not in exclusion_dates

# Function to determine if trades should be exited early on FOMC days
def exit_time_on_fomc_day(date):
    fomc_dates_only = {d.date() for d in Date_FOMC_Announcements_2021}
    if date.date() in fomc_dates_only:
        return (time(13, 45), time(18, 0))
    return None

# Function to determine if it's a market half-day and when trades should be exited
def exit_time_on_half_day(date):
    half_day_dates_only = {d.date() for d in Date_Market_HalfDays_2021}
    if date.date() in half_day_dates_only:
        return (time(11, 45), datetime(date.year, date.month, date.day + 1, 7, 0))
    return None

# Function for Powell speech day trade halt
def powell_speech_blackout(date):
    powell_dates_only = {d.date() for d in Date_Powell_Speeches_2021}
    if date.date() in powell_dates_only:
        return (time(14, 15), time(18, 0))
    return None

# Function for quad witching day early exit
def quad_witching_exit_time(date):
    quad_dates_only = {d.date() for d in Date_Quad_Witching_2021}
    if date.date() in quad_dates_only:
        return (time(13, 0), datetime(date.year, date.month, date.day + 1, 7, 0))
    return None

# Function for NFP timing restrictions
def nfp_trading_restrictions(date):
    nfp_dates_only = {d.date() for d in Date_NFP_2021}
    if date.date() in nfp_dates_only:
        return (None, time(10, 30))
    elif any((date - d).days == -1 for d in Date_NFP_2021):
        return (time(15, 15), None)
    return None

# Function for election day full halt
def election_day_halt(date):
    if Date_Election_2021 and date.date() == Date_Election_2021.date():
        return (None, datetime(date.year, date.month, date.day + 1, 7, 0))
    return None
