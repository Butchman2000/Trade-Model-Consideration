# Program: ml_oversold_workflow.py
# Author: Brian Anderson
# Origin Date: 11May2025
# Version: 1.2
#
# Purpose:
#    /Dynamically assign trade module weights based on market conditions including technical, sentiment, and fundamental oversold definitions.
#    /Example Workflow with Machine Learning and Oversold Condition Handling

# NOTE: This script currently ends with allocation output only.
# An executor is the next logical component; it would take these bin_weights
# and translate them into actual trades, simulations, or order instructions.

# (goto Label A)  which is at the very bottom
# === Optional: Later replace this with AuditLogger.log(...) ===
# from audit_logger import AuditLogger
# logger = AuditLogger()
# logger.log(MODE, condition_type, bin_weights, recent_row.to_dict())

# === TODO Next Steps ===
# - Feed bin_weights into portfolio executor
# - Track performance per bin per regime
# - Continuously refine model thresholds and logic

import numpy as np
import pandas as pd
import json

from datetime import datetime

from config_loader_module import ConfigLoader
cfg = ConfigLoader()

from sklearn.ensemble import RandomForestClassifier

# === GLOBAL CONSTRAINTS AND SETTINGS ===

MODE = "Manual"  # options: "Manual", "ML enabled", "ML off"

constraints = cfg.get_constraints()
MAX_BIN_WEIGHT = constraints["max_bin_weight"]  # Max % per module (6%)
MIN_BIN_WEIGHT = constraints["min_bin_weight"]  # Min % per module (2.5%)  
# This may not be necessary, unless there is later competition for bin space from other models that want action.

total_alloc = constraints["total_portfolio_allocation"]
# This was originally hard set to 80% (maximum) of account in automated bins

reserve = constraints["liquidity_reserve"]
# This was originally hard set to 10% reserved for liquidity

INNER_BIN_BUFFER = 0.95            # 5% internal buffer: e.g., only 4.75% used if 5% is allocated
MANUAL_TRADING_ALLOCATION = 0.10   # Max 10% for manual trades

# === Load and preprocess data ===

market_data = pd.read_csv('market_conditions.csv')  # Data includes SPY, VIX, PE, RSI, etc.
features = market_data[['spy_rsi', 'vix', 'atm_iv', 'pe_ratio', 'fear_greed', 'spx_slope', 'vol_of_vol']]
target = market_data['market_label']  # Labels: 1 = Oversold, 0 = Neutral, -1 = Overbought

# === Train machine learning model (Random Forest Classifier) ===

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(features, target)

# === Manual override logic: define oversold condition categories ===

from bin_logic_shared import categorize_oversold

# === Evaluate current market state ===

recent_row = market_data.iloc[-1]
# Provide the correct order, and correct names for prediction
# The reshape command turns the output into a 2D row for the model
model_input = recent_row[features.columns].values.reshape(1, -1)

# Now we extract the single prediction value ( [0] )
model_prediction = model.predict(model_input)[0]

# Choose whether to manually assume oversold conditions,
# to enable machine learning to test on its own,
# or to turn off the oversold analysis completely.

if MODE == "Manual":
    condition_type = categorize_oversold(recent_row)
elif MODE == "ML enabled":
    if model_prediction == 1:
        condition_type = "oversold and undervalued"
    elif model_prediction == -1:
        condition_type = "technically oversold but overvalued"
    else:
        condition_type = "not_oversold"
elif MODE == "ML off":
    condition_type = "not_oversold"

# === Define bin allocation strategies based on oversold type ===

from bin_logic_shared import assign_bin_weights

# Now use the function
bin_weights = assign_bin_weights(condition_type)

# === Final risk normalization (preserve 80% allocation cap) ===

total_alloc = sum(bin_weights.values())
scaling_factor = constraints["total_portfolio_allocation"] / total_alloc

for k in bin_weights:
    bin_weights[k] *= scaling_factor

# === Output results ===

print(f"Current market condition: {condition_type}")
print("Proposed bin weight allocation:")
for bin_name, weight in bin_weights.items():
    print(f" - {bin_name}: {weight*100:.2f}%")

# === Lightweight JSON audit log ===

log_entry = {
    "timestamp": datetime.utcnow().isoformat(),
    "mode": MODE,
    "condition": condition_type,
    "bin_count": len(bin_weights),
    "bin_weights": bin_weights,
    "constraints": {
        "max_bin_weight": MAX_BIN_WEIGHT,
        "min_bin_weight": MIN_BIN_WEIGHT,
        "total_portfolio_allocation": constraints["total_portfolio_allocation"],
        "liquidity_reserve": constraints["liquidity_reserve"]
    }
}

with open("allocation_log.jsonl", "a") as f:
    f.write(json.dumps(log_entry) + "\n")

# (Label A)
