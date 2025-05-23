# Program: ikbr_secure_config.py
# Author: Brian Anderson
# Origin Date: 06May2025
# Version: 1.4
#
# Purpose:
#    /Connect to Interactive Brokers (IBKR) via ib_insync
#    /Toggle between paper and real trading environments
#    /Set up base structure for future trading model integration
#    /Include time-based checks for market hours


# Constraints:
#- Paper vs Real is controlled by environment config via ibkr_secure_config
#- Does not send any orders by default
#- Logs connection and readiness

# Explore

ORDER_COUNT = 0

# Max trades per session:
MAX_TRADES_PER_SESSION = 100
TRADE_COUNT = 0


#- Config validation and fallback logging toggles:

# Toggle these explicitly (Y,N)
ENABLE_TIME_WAIT = 'Y'
ENABLE_ORDER_EXECUTION = 'N'
ENABLE_CONFIG_VALIDATION = 'Y'
ENABLE_CONFIG_LOGGING = 'Y'
ENABLE_LOG_DEDUP = 'Y'

# Explain time definitions
# Beware of permitting orders to be released at exact times below,
# as market flow becomes unstable near closures and openings.
# Ideally, +/- one minute avoidance of the time changes, is a safer approach,
# except for options after hours between 4pm and 4:15pm.

# === MARKET TIME DELINEATION ===

# It is no ideal to be holding a heavy futures position during 2 to 4 am.
MORNING_FUTURES_EURO_CLOSE = dtime(2,0)  
MORNING_FUTURES_EURO_OPEN = dtime(4,0)

This is the point when most brokerages permit retail purchase activity.
PREMARKET_OPEN = dtime(7,0)
MARKET_OPEN = dtime(9,30)

# Brokerages close options activity for most equities.
MARKET_CLOSE = dtime(16,0)
POSTMARKET_OPEN = dtime(16,0)

# Most brokerages shut down the trading period of special options at this point.
POSTMARKET_OPTIONS_CLOSE = dtime(16,15)  

# American futures market closes for maintenance from 5 to 6 pm.
FUTURES_AMERICAN_CLOSE = dtime(17,0)  
FUTURES_AMERICAN_OPEN = dtime(18,0)

# No further trading of equities.
AFTERMARKET_CLOSE = dtime(20,0)  

# === END OF MARKET TIME DELINEATION ===


# Global error cache for deduplication
_last_error_message = None
_last_error_time = 0

import json
import logging
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from ib_insync import IB, util
from datetime import datetime, time as dtime
import pytz
from ibkr_secure_config import get_ibkr_config
import os
import logging
import time

# If choosing to send data to OneDrive...
# replace 'with open(... , with the following:
# onedrive_path = Path("C:/Users/Butchman2000/OneDrive/IBKR/positions.json")
# with open(onedrive_path, "w") as f:
#
# do the same for the csv path
# add a note to .gitignore for safety

# Setup logging
LOG_PATH = Path("ibkr_secure_config.log")
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load .env file if it exists
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    logging.info(".env file loaded successfully.")
else:
    logging.warning(".env file not found. Using system environment variables.")


def place_order():
    # Do nothing for now, but add what is needed, later on.
    if TRADE_COUNT >= MAX_TRADES_PER_SESSION:
        raise RuntimeError("Trade count limit exceeded.")


def get_ibkr_config():
    """
    Retrieves and validates IBKR connection settings.
    Returns a dictionary with config data.
    Logs warnings or errors for any missing or invalid entries.
    """
    def _get_env(name, default=None, cast=str):
        val = os.getenv(name, default)
        if val is None:
            logging.error(f"Missing required config: {name}")
            raise ValueError(f"Missing required config: {name}")
        try:
            return cast(val)
        except Exception:
            logging.error(f"Invalid format for {name}: expected {cast.__name__}")
            raise

    config = {
        "USE_PAPER": _get_env("USE_PAPER", "True", lambda x: x.lower() == "true"),  # TODO: ensure my use of lambda is correct
        "IB_GATEWAY_HOST": _get_env("IB_GATEWAY_HOST", "127.0.0.1"),
        "IB_GATEWAY_PORT_PAPER": _get_env("IB_GATEWAY_PORT_PAPER", 7497, int),
        "IB_GATEWAY_PORT_LIVE": _get_env("IB_GATEWAY_PORT_LIVE", 7496, int),
        "IB_CLIENT_ID": _get_env("IB_CLIENT_ID", 1, int)
    }

    logging.info("IBKR config loaded and validated.")
    return config
  
'''
# Optional logging setup
if ENABLE_CONFIG_LOGGING == 'Y':
    logging.basicConfig(
        filename='ibkr_secure_config.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.info("Logging initialized.")
    '''


def log_error_once(message):
    global _last_error_message, _last_error_time
    now = time.time()
    if ENABLE_LOG_DEDUP == 'Y':
        if message == _last_error_message and (now - _last_error_time) <= 5:
            logging.error(f"DOUBLE: {message}")
            return
        _last_error_message = message
        _last_error_time = now
    logging.error(message)


# Config validation (additional layer)
def validate_config(cfg):
    required_keys = [
        "USE_PAPER", "IB_GATEWAY_HOST",
        "IB_GATEWAY_PORT_PAPER", "IB_GATEWAY_PORT_LIVE",
        "IB_CLIENT_ID"
    ]
    for key in required_keys:
        if key not in cfg:
            msg = f"Missing required config key: {key}"
            if ENABLE_CONFIG_LOGGING == 'Y':
                log_error_once(msg)
            raise KeyError(msg)
    if ENABLE_CONFIG_LOGGING == 'Y':
        logging.info("Config validation passed.")


# Load and optionally validate config
config = get_ibkr_config()
if ENABLE_CONFIG_VALIDATION == 'Y':
    validate_config(config)

USE_PAPER = config["USE_PAPER"]
IB_GATEWAY_HOST = config["IB_GATEWAY_HOST"]

# -----/// DO NOT ALTER UNDER ANY CONDITIONS ///-----

if USE_PAPER == True:
    IB_GATEWAY_PORT = config["IB_GATEWAY_PORT_PAPER"] 
else
    IB_GATEWAY_PORT = config["IB_GATEWAY_PORT_LIVE"]

# -----/// DO NOT ALTER UNDER ANY CONDITIONS ///-----

IB_CLIENT_ID = config["IB_CLIENT_ID"]

# Time window example (US Eastern time)
MARKET_OPEN = dtime(9, 30)
MARKET_CLOSE = dtime(16, 0)
EASTERN = pytz.timezone('US/Eastern')


def is_market_open():
    now_est = datetime.now(EASTERN).time()
    return MARKET_OPEN <= now_est <= MARKET_CLOSE


def connect_ibkr():
    ib = IB()
    try:
        ib.connect(IB_GATEWAY_HOST, IB_GATEWAY_PORT, clientId=IB_CLIENT_ID)
        if USE_PAPER == True:
            print(f"Connected to IBKR ({'Paper'})
        else:
            print(f"Connected to IBKR ({'Live'}))

        if ENABLE_CONFIG_LOGGING == 'Y':
            logging.info("IBKR connection successful.")
    except Exception as e:
        print("Failed to connect to IBKR:", e)
        if ENABLE_CONFIG_LOGGING == 'Y':
            log_error_once(f"Connection failed: {e}")
        return None
    return ib


def export_positions(ib):
    positions = ib.positions()
    for acct, contract, position in positions:
        print(f"{contract.symbol} | {position} shares/contracts in {acct}")

    position_data = [{
        "account": acct,
        "symbol": contract.symbol,
        "secType": contract.secType,
        "expiry": contract.lastTradeDateOrContractMonth,
        "strike": contract.strike,
        "right": contract.right,
        "multiplier": contract.multiplier,
        "exchange": contract.exchange,
        "currency": contract.currency,
        "position": position
    } for acct, contract, position in positions]

    with open("positions.json", "w") as f:
        json.dump(position_data, f, indent=2)

    df = pd.DataFrame(position_data)
    df.to_csv("positions.csv", index=False)


def main():

    if ENABLE_TIME_WAIT == 'Y':
        PREMARKET_OPEN = dtime(7, 0)
        while datetime.now(EASTERN).time() < PREMARKET_OPEN:
            print("Market off limit right now: holding...")
            time.sleep(30)

        while datetime.now(EASTERN).time() < MARKET_OPEN:
            print("Pre-market: holding...")
            time.sleep(30)

        while not is_market_open():
            print("Waiting for market to open...")
            time.sleep(60)

    if not is_market_open():
        print("Market is closed. Exiting.")
        return

    ib = connect_ibkr()
    if ib is None:
        return

    print("Ready to run trading model...")

    # Optional: check account summary
    account = ib.reqAccountSummary()
    print("Account summary:")
    print(account)

    # Export positions to JSON and CSV
    export_positions(ib)

    ib.disconnect()


if __name__ == "__main__":
    main()
    print("=== IBKR Session Started ===")

  # === AUDIT SYSTEM EXTENSION ===

# Example model audit specification
audit_specs = {
    "model_A": {
        "requires_position_check": True,
        "max_order_size": 100,
        "requires_spread_pair": True,
        "permitted_instruments": ["OPT", "STK"]
    },
    "model_B": {
        "requires_position_check": False,
        "permitted_instruments": ["STK"]
    }
    # Add additional models as needed
}

# Example audit execution

def run_model_audit(model_name, positions):
    spec = audit_specs.get(model_name)
    if not spec:
        print(f"[AUDIT] No audit spec found for model: {model_name}")
        return

    print(f"[AUDIT] Running audit for model: {model_name}")
    failures = []

    for acct, contract, position in positions:
        if spec.get("requires_position_check") and position == 0:
            failures.append(f"No position held in {contract.symbol} for audit-required model.")

        if spec.get("max_order_size") and abs(position) > spec["max_order_size"]:
            failures.append(f"Position size {position} in {contract.symbol} exceeds allowed max of {spec['max_order_size']}")

        if "permitted_instruments" in spec and contract.secType not in spec["permitted_instruments"]:
            failures.append(f"Instrument {contract.secType} not permitted in model {model_name}")

    if failures:
        print(f"[AUDIT] Issues found for {model_name}:")
        for issue in failures:
            print(f"  - {issue}")
    else:
        print(f"[AUDIT] All checks passed for {model_name}.")


# Example usage
# ib = connect_ibkr()
# positions = ib.positions()
# run_model_audit("model_A", positions)

