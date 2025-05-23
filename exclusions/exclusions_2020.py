# Program: exclusions_2020.py
# Author: Brian Anderson
# Origin Date: 30April2025
# Version: 1.0
# 
# Purpose:
#    /Backtest exclusion criterion for the year of 2020
#   /Assemble market dates for critical days that most strongly affect market activity.
#   /Specifies spans of time for which alteration of trading activity should be considered.

from datetime import datetime, time

# CPI release dates for 2020
Date_CPI_Releases_2020 = [
    datetime(2020, 1, 14), datetime(2020, 2, 13), datetime(2020, 3, 11), datetime(2020, 4, 10),
    datetime(2020, 5, 12), datetime(2020, 6, 10), datetime(2020, 7, 14), datetime(2020, 8, 12),
    datetime(2020, 9, 11), datetime(2020, 10, 13), datetime(2020, 11, 12), datetime(2020, 12, 10)
]

# FOMC announcement dates for 2020
Date_FOMC_Announcements_2020 = [
    datetime(2020, 1, 29), datetime(2020, 3, 15), datetime(2020, 4, 29), datetime(2020, 6, 10),
    datetime(2020, 7, 29), datetime(2020, 9, 16), datetime(2020, 11, 5), datetime(2020, 12, 16)
]

# Powell speeches in 2020 (partial list)
Date_Powell_Speeches_2020 = [
    datetime(2020, 3, 3), datetime(2020, 3, 26), datetime(2020, 5, 13), datetime(2020, 8, 27),
    datetime(2020, 10, 6), datetime(2020, 11, 17)
]

# Market half-days in 2020
Date_Market_HalfDays_2020 = [
    datetime(2020, 7, 3), datetime(2020, 11, 27), datetime(2020, 12, 24)
]

# Last trading day of each month in 2020
Date_Last_Trading_Days_2020 = [
    datetime(2020, 1, 31), datetime(2020, 2, 28), datetime(2020, 3, 31), datetime(2020, 4, 30),
    datetime(2020, 5, 29), datetime(2020, 6, 30), datetime(2020, 7, 31), datetime(2020, 8, 31),
    datetime(2020, 9, 30), datetime(2020, 10, 30), datetime(2020, 11, 30), datetime(2020, 12, 31)
]

# Quad Witching Dates 2020
Date_Quad_Witching_2020 = [
    datetime(2020, 3, 20), datetime(2020, 6, 19), datetime(2020, 9, 18), datetime(2020, 12, 18)
]

# NFP Fridays 2020 (1st Friday each month approx.)
Date_NFP_2020 = [
    datetime(2020, 1, 10), datetime(2020, 2, 7), datetime(2020, 3, 6), datetime(2020, 4, 3),
    datetime(2020, 5, 8), datetime(2020, 6, 5), datetime(2020, 7, 2), datetime(2020, 8, 7),
    datetime(2020, 9, 4), datetime(2020, 10, 2), datetime(2020, 11, 6), datetime(2020, 12, 4)
]

# Election Day 2020
Date_Election_2020 = datetime(2020, 11, 3)

# Jackson Hole 2020 note (no action taken)
# Jackson Hole 2020 occurred around August 27–29

# Combine all exclusion dates into a set for faster lookup
exclusion_dates = set(
    Date_CPI_Releases_2020 +
    Date_FOMC_Announcements_2020 +
    Date_Powell_Speeches_2020 +
    Date_Market_HalfDays_2020 +
    Date_Last_Trading_Days_2020
)

# Function to filter out exclusion dates
def is_valid_trading_day(date):
    return date not in exclusion_dates

# Function to determine if trades should be exited early on FOMC days
def exit_time_on_fomc_day(date):
    fomc_dates_only = {d.date() for d in Date_FOMC_Announcements_2020}
    if date.date() in fomc_dates_only:
        return (time(13, 45), time(18, 0))
    return None

# Function to determine if it's a market half-day and when trades should be exited
def exit_time_on_half_day(date):
    half_day_dates_only = {d.date() for d in Date_Market_HalfDays_2020}
    if date.date() in half_day_dates_only:
        return (time(11, 45), datetime(date.year, date.month, date.day + 1, 7, 0))
    return None

# Function for Powell speech day trade halt
def powell_speech_blackout(date):
    powell_dates_only = {d.date() for d in Date_Powell_Speeches_2020}
    if date.date() in powell_dates_only:
        return (time(14, 15), time(18, 0))
    return None

# Function for quad witching day early exit
def quad_witching_exit_time(date):
    quad_dates_only = {d.date() for d in Date_Quad_Witching_2020}
    if date.date() in quad_dates_only:
        return (time(13, 0), datetime(date.year, date.month, date.day + 1, 7, 0))
    return None

# Function for NFP timing restrictions
def nfp_trading_restrictions(date):
    nfp_dates_only = {d.date() for d in Date_NFP_2020}
    if date.date() in nfp_dates_only:
        return (None, time(10, 30))
    elif any((date - d).days == -1 for d in Date_NFP_2020):
        return (time(15, 15), None)
    return None

# Function for election day full halt
def election_day_halt(date):
    if date.date() == Date_Election_2020.date():
        return (None, datetime(date.year, date.month, date.day + 1, 7, 0))
    return None
