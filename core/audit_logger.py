# Program: audit_logger.py
# Author: Brian Anderson
# Origin Date: 11May2025
# Version: 1.0
#
# Purpose:
#    /This is an audit logger utility program

import json
import hashlib
from datetime import datetime

class AuditLogger:
    def __init__(self, filepath="decision_log.jsonl"):
        self.filepath = filepath

    def log(self, mode, condition_type, bin_weights, features):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "mode": mode,
            "market_condition": condition_type,
            "features": features,
            "bin_weights": bin_weights
        }
        log_json = json.dumps(log_entry, sort_keys=True)
        checksum = hashlib.sha256(log_json.encode()).hexdigest()
        with open(self.filepath, "a") as f:
            f.write(log_json + f" // sha256: {checksum}\n")

    def log_error(self, exception, features):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(exception),
            "features": features
        }
        log_json = json.dumps(log_entry, sort_keys=True)
        checksum = hashlib.sha256(log_json.encode()).hexdigest()
        with open(self.filepath, "a") as f:
            f.write(log_json + f" // sha256: {checksum}\n")
