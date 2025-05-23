# Program: risk_execution_protocol.py
# Architect: Brian Anderson
# Date: 09April2025
# Version: 1.0
#
# Purpose:
#    /This module defines the risk boundaries, failure thresholds,
#    /and emergency logic governing trade execution and capital exposure.

# Safety mechanisms include:
# Throttling - reduced risk sizing is activated after drawdowns exceed a soft warning level.
# Position Size Cap - No single trade may exceed capital-based maximum thresholds.
# Trade Frequency Lock - Auto-freeze if more than N entry operations occur within an hour.
# Trade classification allows adaptive flexibility for exits and leg adjustments.
# Capital-based scaling tiers: low (<$2k), retail ($2k–$25k), pro ($25k+)
# Confidence-based risk modulation using classification strings
# Note A: Classification strings may include source metadata (e.g. signal family, IV level, float flag)

import datetime

class RiskExecutionProtocol:
    def __init__(self, account_equity):
        self.account_equity = account_equity
        self.tier = self._define_tier()

        # Capital scaling rules
        if self.tier == "low":
            self.max_position_size_pct = 0.15
            self.max_trades_per_hour = 8
        elif self.tier == "retail":
            self.max_position_size_pct = 0.20
            self.max_trades_per_hour = 6
        else:
            self.max_position_size_pct = 0.25
            self.max_trades_per_hour = 4

        self.max_daily_drawdown_pct = 0.04
        self.max_trade_drawdown_pct = 0.015
        self.daily_loss_total = 0.0
        self.trade_history = []
        self.last_trade_time = None

        self.execution_frozen = False
        self.throttle_mode = False
        self.throttle_trigger_pct = 0.025
        self.throttle_scaling = 0.5

        self.locked_due_to_freq = False
        self.trade_timestamps = []

    def _define_tier(self):
        if self.account_equity < 2000:
            return "low"
        elif self.account_equity < 25000:
            return "retail"
        else:
            return "pro"

    def _risk_scaling_from_confidence(self, classification):
        """
        Scale risk dynamically based on signal confidence.
        Accepts confidence tags like 'A_2_X', 'HiRSI.LowFloat.x,y,z'
        """
        tag = classification.lower()
        if "a_" in tag or "high" in tag:
            return 1.0  # full position size
        elif "b_" in tag or "med" in tag:
            return 0.65
        elif "c_" in tag or "low" in tag:
            return 0.4  #See Note A above
        else:
            return 0.25  # unknown or unclassified => small

    def validate_trade_request(self, classification, position_size_pct):
        """
        Used by SIS to validate trade viability pre-execution.
        Returns (bool: is_allowed, str: message)
        """
        if self.execution_frozen:
            return False, "Execution frozen. Trade denied."

        scale_factor = self._risk_scaling_from_confidence(classification)
        scaled_limit = self.max_position_size_pct * scale_factor

        if position_size_pct > scaled_limit:
            return False, f"Position exceeds scaled limit for class '{classification}'."

        return True, "Trade permitted."

    def record_trade(self, pnl_pct, position_size_pct, trade_type="entry", operation_type="primary", classification=""):
        if self.execution_frozen and trade_type == "entry" and operation_type == "primary":
            return "Execution frozen. No further primary entries allowed."

        now = datetime.datetime.utcnow()
        if trade_type == "entry" and operation_type == "primary":
            self.trade_timestamps.append(now)
            self.trade_timestamps = [t for t in self.trade_timestamps if (now - t).seconds < 3600]

            if len(self.trade_timestamps) > self.max_trades_per_hour:
                self.execution_frozen = True
                self.locked_due_to_freq = True
                return "Entry frequency exceeded. New primary entries blocked."

            scale_factor = self._risk_scaling_from_confidence(classification)
            scaled_limit = self.max_position_size_pct * scale_factor

            if position_size_pct > scaled_limit:
                self.execution_frozen = True
                return f"Trade size too large ({position_size_pct:.2%}) for confidence class '{classification}'. Execution frozen."

        self.trade_history.append(pnl_pct)
        self.daily_loss_total += pnl_pct if pnl_pct < 0 else 0
        self.last_trade_time = now

        if pnl_pct < -self.max_trade_drawdown_pct:
            self.execution_frozen = True
            return f"Trade loss exceeded limit ({pnl_pct:.2%}). Execution frozen."

        if abs(self.daily_loss_total) > self.max_daily_drawdown_pct:
            self.execution_frozen = True
            return f"Daily loss limit exceeded ({self.daily_loss_total:.2%}). Execution frozen."

        if abs(self.daily_loss_total) > self.throttle_trigger_pct:
            self.throttle_mode = True

        return "Trade recorded."

    def should_throttle(self):
        return self.throttle_mode and not self.execution_frozen

    def reset_daily_risk(self):
        self.daily_loss_total = 0.0
        self.trade_history.clear()
        self.trade_timestamps.clear()
        self.execution_frozen = False
        self.throttle_mode = False
        self.locked_due_to_freq = False
        return "Risk counters reset. Execution re-enabled."

    def get_status(self):
        return {
            'account_equity': self.account_equity,
            'capital_tier': self.tier,
            'daily_loss_total': self.daily_loss_total,
            'trades_today': len(self.trade_history),
            'execution_frozen': self.execution_frozen,
            'throttle_mode': self.throttle_mode,
            'locked_due_to_freq': self.locked_due_to_freq,
            'trades_last_hour': len(self.trade_timestamps)
        }
