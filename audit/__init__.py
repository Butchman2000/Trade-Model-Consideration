# Program: __init__
# Author: Brian Anderson
# Origin Date: 01May2025
# Version: 1.0
#
# Purpose:
#    /Makes core audit components available directly via `from audit import ...`
#    / It is used to initialize the audit namespace, enforce structure, and simplify imports.

from .audit_tools import ComplianceLogger, wait_for_external_approval
from .email_config import EMAIL_SETTINGS
from .env_check import check_env_vars

__all__ = [
    "ComplianceLogger",
    "wait_for_external_approval",
    "EMAIL_SETTINGS",
    "check_env_vars"
]
