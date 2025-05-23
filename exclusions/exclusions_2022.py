# Program: exclusions_2022.py
# Author: Brian Anderson
# Origin Date: 30April2025
# Version: 1.0
# 
# Purpose:
#    /Backtest exclusion criterion for the year of 2022
#    /Assemble market dates for critical days that most strongly affect market activity.
#    /Specifies spans of time for which alteration of trading activity should be considered.
#    /For example, since FOMC meetings are released around 2:30 pm, we make choices at 1:45 pm,
#    /as to whether to withdraw trades, or make other actions (todo).

from datetime import datetime, time

# CPI release dates for 2022
Date_CPI_Releases_2022 = [
    datetime(2022, 1, 12), datetime(2022, 2, 10), datetime(2022, 3, 10), datetime(2022, 4, 12),
    datetime(2022, 5, 11), datetime(2022, 6, 10), datetime(2022, 7, 13), datetime(2022, 8, 10),
    datetime(2022, 9, 13), datetime(2022, 10, 13), datetime(2022, 11, 10), datetime(2022, 12, 13)
]

# FOMC announcement dates for 2022
Date_FOMC_Announcements_2022 = [
    datetime(2022, 1, 26), datetime(2022, 3, 16), datetime(2022, 5, 4), datetime(2022, 6, 15),
    datetime(2022, 7, 27), datetime(2022, 9, 21), datetime(2022, 11, 2), datetime(2022, 12, 14)
]

# Powell speeches in 2022 (partial list)
Date_Powell_Speeches_2022 = [
    datetime(2022, 1, 11), datetime(2022, 3, 2), datetime(2022, 6, 23), datetime(2022, 8, 26),
    datetime(2022, 9, 8), datetime(2022, 11, 30)
]

# Market half-days in 2022
Date_Market_HalfDays_2022 = [
    datetime(2022, 7, 1), datetime(2022, 11, 25), datetime(2022, 12, 23)
]

# Last trading day of each month in 2022
Date_Last_Trading_Days_2022 = [
    datetime(2022, 1, 31), datetime(2022, 2, 28), datetime(2022, 3, 31), datetime(2022, 4, 29),
    datetime(2022, 5, 31), datetime(2022, 6, 30), datetime(2022, 7, 29), datetime(2022, 8, 31),
    datetime(2022, 9, 30), datetime(2022, 10, 31), datetime(2022, 11, 30), datetime(2022, 12, 30)
]

# Quad Witching Dates 2022
Date_Quad_Witching_2022 = [
    datetime(2022, 3, 18), datetime(2022, 6, 17), datetime(2022, 9, 16), datetime(2022, 12, 16)
]

# NFP Fridays 2022 (1st Friday each month approx.)
Date_NFP_2022 = [
    datetime(2022, 1, 7), datetime(2022, 2, 4), datetime(2022, 3, 4), datetime(2022, 4, 1),
    datetime(2022, 5, 6), datetime(2022, 6, 3), datetime(2022, 7, 8), datetime(2022, 8, 5),
    datetime(2022, 9, 2), datetime(2022, 10, 7), datetime(2022, 11, 4), datetime(2022, 12, 2)
]

# Election Day 2022
Date_Election_2022 = datetime(2022, 11, 8)

# Jackson Hole 2022 note (no action taken)
# Jackson Hole 2022 occurred around August 25–27

# Combine all exclusion dates into a set for faster lookup
exclusion_dates = set(
    Date_CPI_Releases_2022 +
    Date_FOMC_Announcements_2022 +
    Date_Powell_Speeches_2022 +
    Date_Market_HalfDays_2022 +
    Date_Last_Trading_Days_2022
)

# Function to filter out exclusion dates
def is_valid_trading_day(date):
    return date not in exclusion_dates

# Function to determine if trades should be exited early on FOMC days
def exit_time_on_fomc_day(date):
    fomc_dates_only = {d.date() for d in Date_FOMC_Announcements_2022}
    if date.date() in fomc_dates_only:
        return (time(13, 45), time(18, 0))
    return None

# Function to determine if it's a market half-day and when trades should be exited
def exit_time_on_half_day(date):
    half_day_dates_only = {d.date() for d in Date_Market_HalfDays_2022}
    if date.date() in half_day_dates_only:
        return (time(11, 45), datetime(date.year, date.month, date.day + 1, 7, 0))
    return None

# Function for Powell speech day trade halt
def powell_speech_blackout(date):
    powell_dates_only = {d.date() for d in Date_Powell_Speeches_2022}
    if date.date() in powell_dates_only:
        return (time(14, 15), time(18, 0))
    return None

# Function for quad witching day early exit
def quad_witching_exit_time(date):
    quad_dates_only = {d.date() for d in Date_Quad_Witching_2022}
    if date.date() in quad_dates_only:
        return (time(13, 0), datetime(date.year, date.month, date.day + 1, 7, 0))
    return None

# Function for NFP timing restrictions
def nfp_trading_restrictions(date):
    nfp_dates_only = {d.date() for d in Date_NFP_2022}
    if date.date() in nfp_dates_only:
        return (None, time(10, 30))
    elif any((date - d).days == -1 for d in Date_NFP_2022):
        return (time(15, 15), None)
    return None

# Function for election day full halt
def election_day_halt(date):
    if date.date() == Date_Election_2022.date():
        return (None, datetime(date.year, date.month, date.day + 1, 7, 0))
    return None
