# Program: email_config.py
# Author: Brian Anderson
# Origin Date: 01May2025
# Version: 1.0
#
# Purpose:
#   /Centralized configuration for SMTP email alerts that is used by audit tools.

# TODO: Add my password.  Add this to .gitignore if necessary.

EMAIL_SETTINGS = {
    "recipient": "their-email@provider.com",
    "sender": "Bdander2000@outlook.com",
    "smtp_host": "smtp.office365.com",
    "smtp_port": 587
}

# These should be set in your environment for security, not hardcoded:
# - SMTP_SENDER_EMAIL
# - SMTP_SENDER_PASSWORD

# Example:
# In my shell or virtual environment:
# export SMTP_SENDER_EMAIL="Bdander2000@outlook.com"
# export SMTP_SENDER_PASSWORD="my-secure-password"
