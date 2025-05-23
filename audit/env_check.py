# Program: env_check.py
# Author: Brian Anderson
# Origin Date: 01May2025
# Version: 1.0
#
# Purpose:
#    /Validate required environment variables are set for audit email and sensitive ops

import os

REQUIRED_VARS = ["SMTP_SENDER_EMAIL", "SMTP_SENDER_PASSWORD"]

def check_env_vars():
    missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
    if missing:
        print("DANGER: Missing required environment variables:")
        for var in missing:
            print(f"  - {var}")
        return False
    print("NOTICE: All required environment variables are set.")
    return True

# Example usage in a script:
# from env_check import check_env_vars
# if not check_env_vars():
#     exit(1)
