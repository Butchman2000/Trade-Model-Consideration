# Program: audit_tools.py
# Author: Brian Anderson
# Origin Date: 01May2025
# Version: 1.0
#
# Purpose:
#    Shared module to ensure all stock monitoring and analysis tools log auditable,
#    timestamped, and structured events in compliance with traceability requirements
#    analogous to installation/operational/performance qualification in cGMP environments.
#
#    Use this module to log structured events across all trading, alerting, or signal
#    detection scripts for centralized tracking, review, and post-mortem audit.

# Note: In order to benefit from these controls, in each module, add:
# from audit.audit_tools import ComplianceLogger, wait_for_external_approval

'''
# --- Compliance Notes for Repository Setup ---

# To enforce change control and LP protection, set up the following:
#
# 1. GitHub Branch Protection Rules:
#    - Require pull request reviews before merging to `main`
#    - Include administrators (to prevent self-bypass)
#    - Enable status checks if using CI/CD
#
# 2. Set `audit_tools.py` in a monitored folder (e.g., /compliance or /core)
#
# 3. Use GitHub CODEOWNERS to enforce that any change to this file must be approved:
#    Example .github/CODEOWNERS file:
#      /compliance/audit_tools.py  @BrianAnderson @YourApproverHandle
#
# 4. Use commit signatures (GPG) to validate that all commits are authentic.
#
# 5. Optional: deploy read-only permission to this file via file system lock:
#    chmod 444 audit_tools.py
#
# These steps ensure traceability, separation of duties, and change tracking aligned
# with GxP and institutional capital handling standards.

# --- Instructions for Use ---

# External Approval (Phase 2 concept)
# -----------------------------------
# Some conditions may require external confirmation before continuing.
# To enforce that, define an approval flag file (e.g., 'biotech_approval_flag.json') like so:
# {
#     "approved": true,
#     "approved_by": "user@example.com",
#     "timestamp": "2025-05-01T14:33:00"
# }
# 
# The system will pause until this file exists and is marked approved.
# Notification is sent to the designated authority (see APPROVAL_CONTACT_EMAIL).
# This allows for basic 2-person review prior to advancing critical logic.

# Example hook in a module:
# from audit_tools import wait_for_external_approval
# wait_for_external_approval('biotech_approval_flag.json')


In all stock modules, put the following code in:

from audit_tools import ComplianceLogger

log = ComplianceLogger("biotech_event_log_20250501.json")

# Inside your logic
if drop >= 0.3:
    log.log_event(ticker="ACME", event_type="BIOTECH_DROP", value=drop, notes="Phase 2 failed")
'''

import json
from datetime import datetime
import time
import os
import sys

# Global: Approval authority email placeholder (may become part of access control or LDAP system)
APPROVAL_CONTACT_EMAIL = "lp_approver@example.com"

# Utility function: wait_for_external_approval
# ------------------------------------------------
# This function halts execution until a specific JSON file confirms
# that an external party has reviewed and approved a sensitive event.
# Intended for manual checkpoints, audit pauses, or double-confirmation protocols.
def wait_for_external_approval(flag_filepath, check_interval=60):
    print(f"[WAIT] Awaiting external approval via: {flag_filepath}")
    while True:
        if os.path.exists(flag_filepath):
            try:
                with open(flag_filepath, 'r') as f:
                    data = json.load(f)
                    if data.get("approved") is True:
                        approved_by = data.get("approved_by", "UNKNOWN")
                        approved_when = data.get("timestamp", datetime.now().isoformat())
                        print(f"[APPROVED] Proceeding — approved by {approved_by} at {approved_when}")
                        return
            except Exception as e:
                print(f"WARNING: Could not read approval file {flag_filepath}: {e}")
        else:
            print(f"[WAIT] No approval file found yet: {flag_filepath}")

        time.sleep(check_interval)


class ComplianceLogger:
    def __init__(self, log_file_path):
        # Path to the file where JSON-formatted logs will be saved
        self.log_file_path = log_file_path
        self.log_records = []  # also keep logs in memory (useful for in-process reviews)

    def log_event(self, ticker, event_type, value, notes=None):
        # Create and store a structured event log with timestamp
        record = {
            "timestamp": datetime.now().isoformat(),
            "ticker": ticker,
            "event_type": event_type,
            "value": round(value, 4),
            "notes": notes or ""
        }
        self.log_records.append(record)

        # Append to disk immediately to preserve in case of crash
        try:
            with open(self.log_file_path, 'a') as f:
                json.dump(record, f)
                f.write('\n')
        except Exception as e:
            print(f"DANGER: Failed to write to log file {self.log_file_path}: {e}")

        return record

    def notify(self, message):
        # Primary notification system: print + optional email alert
        print(f"[NOTIFY] {message}")

        # Email alert logic — only if SMTP settings are configured
        import smtplib
        from email.mime.text import MIMEText

        recipient = "Bdander2000@msn.com"
        subject = "Compliance Alert from Trading System"
        body = f"Alert generated at {datetime.now().isoformat()}:

{message}"

        # Customize this to match your actual email provider (Gmail, Outlook, etc.)
        smtp_host = "smtp.office365.com"
        smtp_port = 587
        import os
        sender_email = os.getenv("SMTP_SENDER_EMAIL")  # set in environment
        sender_password = os.getenv("SMTP_SENDER_PASSWORD")  # set in environment

        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)

        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send alert email: {e}")
