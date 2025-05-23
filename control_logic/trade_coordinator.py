# Program: trade_coordinator.py
# Author: Brian Anderson
# Origin Date:
# Version 2.0
#
# Purpose:
#    /Coordinates the following:
#    /Signal isolation system (SIS); file name: signal_isolation_system.py
#    /Risk execution protocol (REP); file name: risk_execution_protocol.py
#    /Tax filter (TAX); file name: to be determined, incorporated elsewhere
#
#    /This is a portable, semi-autonomous strategy governance layer. 
#    /Logs, validates, and structures trade decision data
#
# Includes: margin, corporate actions, and secure preprocessing safeguards
# Includes: basic margin risk awareness for trade style + permission mismatch
# Includes: symbol normalization, split/spinoff tracking, and passive metadata flags
# NOTE: Be sure to apply split-adjusted criteria to noise and time evaluation logic elsewhere.
#
# NOTE: Cash accounts are subject to T+1 use delays and T+2 withdrawal times.
#       Futures accounts have MTM capital rules and T+1 withdrawal timing.

'''
 A disciplined execution system, wherein:
-Knows when not to act
-Understands risk scaling per signal type
-Filters noise and data deception
-Avoids margin or tax landmines
-Documents every judgment for future clarity

 This System Was Meant To:
-Restore Trust in My Own Judgment
-Move You Toward Institutional Readiness
-Protect You from Invisible Traps (unseen and structural)
-Work towards Delegation of Execution
'''

import time
# from collections import deque  # Correct this when proper pathway is discovered

# The RateLimiter class controls the number of incoming signals per second, to prevent overload.

class RateLimiter: 
    def __init__(self, max_packets_per_sec=5, burst_limit=10):  # Initializes rate limits
        self.timestamps = deque()
        self.max_packets_per_sec = max_packets_per_sec
        self.burst_limit = burst_limit

    def allow(self):  # Checks if current rate of signal intake is within limits
        now = time.time()
        self.timestamps.append(now)
        while self.timestamps and now - self.timestamps[0] > 1:
            self.timestamps.popleft()
        return len(self.timestamps) <= self.burst_limit

class PacketSanitizer:  # Ensures incoming signal packets are safe, valid, and clean
    def __init__(self, max_length=4096):  # Sets maximum acceptable field length
        self.max_length = max_length

    def validate_timestamp(self, timestamp_str):  # Ensures timestamp is ISO, not future, and within 5 minutes
        from datetime import datetime, timedelta
        try:
            packet_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            raise ValueError("Invalid timestamp format. Expected ISO format (e.g., 2025-04-09T14:33:00Z)")

        now = datetime.utcnow()
        if packet_time > now:
            raise ValueError("Timestamp is in the future")
        if now - packet_time > timedelta(minutes=5):
            raise ValueError("Timestamp is older than 5 minutes")
            self.validate_timestamp(packet.get('timestamp', ''))
        return True

    def sanitize(self, packet):  # Checks structure and field size of incoming signal packet
        if not isinstance(packet, dict):
            raise ValueError("Malformed packet: not a dictionary")
        if any(len(str(v)) > self.max_length for v in packet.values()):
            raise ValueError("Suspiciously large field in packet")
        return True

class TradeCoordinator:  # Central brain for coordinating SIS, REP, TaxFilter, and security logic
    # Includes anomaly throttling to prevent execution under synthetic or distorted input conditions
    def __init__(self, sis, rep, tax_filter):  # Initializes coordinator with subsystems and logs
        self.sis = sis
        self.rep = rep
        self.tax_filter = tax_filter
        self.decision_log = []
        self.symbol_registry = {}
        self.split_log = []
        self.spinoff_log = []
        self.ratelimiter = RateLimiter()
        self.sanitizer = PacketSanitizer()
        self.anomaly_cooldown = 90.41  # seconds between trades during integrity faults
        self.last_safe_trade_time = 0

    def register_symbol_change(self, old_symbol, new_symbol):  # Tracks symbol renames (e.g., FB -> META)
        self.symbol_registry[old_symbol] = new_symbol

    def register_split(self, symbol, date_str, factor):  # Logs share splits for historical normalization
        self.split_log.append({ 'symbol': symbol, 'date': date_str, 'factor': factor })

    def register_spinoff(self, parent_symbol, child_symbol, date_str):  # Logs asset spin-offs
        self.spinoff_log.append({ 'parent': parent_symbol, 'child': child_symbol, 'date': date_str })

    def get_split_factor(self, symbol, date_str):  # Retrieves the applicable split ratio for a date
        for entry in self.split_log:
            if entry['symbol'] == symbol and entry['date'] <= date_str:
                return entry['factor']
        return 1.0

    def get_current_symbol(self, input_symbol):  # Resolves renamed symbols via registry
        return self.symbol_registry.get(input_symbol, input_symbol)

    def list_spinoffs_for(self, symbol):  # Returns a list of known spin-off assets
        return [s['child'] for s in self.spinoff_log if s['parent'] == symbol]

    def process_signal(self, signal_packet):  # Core decision pipeline: SIS + REP + Tax + Security + Anomaly Check
        import time
        now = time.time()

        if now - self.last_safe_trade_time < self.anomaly_cooldown:
            return {'error': f'Anomaly throttle active. Must wait {round(self.anomaly_cooldown - (now - self.last_safe_trade_time), 2)} seconds.'}

        if not self.ratelimiter.allow():
            return {'error': 'Rate limit exceeded. Try again later.'}

        try:
            self.sanitizer.sanitize(signal_packet)
        except ValueError as e:
            return {'error': f'Packet rejected: {str(e)}'}

        decision = {
            'signal_id': signal_packet['id'],
            'timestamp': signal_packet['timestamp'],
            'inputs': signal_packet['inputs'],
            'confidence_tag': signal_packet.get('confidence_tag', 'unclassified'),
            'risk_pct': signal_packet.get('risk_pct', 0.01),
            'suitable': False,
            'permitted': False,
            'tax_notes': [],
            'margin_risk': '',
            'split_adjusted': signal_packet.get('split_adjusted', False),
            'spinoff_event': signal_packet.get('spinoff_event', False),
            'final_decision': 'REJECTED',
            'reason': ''
        }

        allowed_by_sis = self.sis.allow_trade(signal_packet)
        decision['suitable'] = allowed_by_sis

        if not allowed_by_sis:
            decision['reason'] = 'SIS filter rejected signal'
                    self.last_safe_trade_time = now
        self.decision_log.append(decision)
            return decision

        rep_ok, reason = self.rep.validate_trade_request(
            classification=decision['confidence_tag'],
            position_size_pct=decision['risk_pct']
        )
        decision['permitted'] = rep_ok
        decision['reason'] = reason

        symbol = signal_packet.get('symbol', 'UNKNOWN')
        current_symbol = self.get_current_symbol(symbol)
        trade_date_str = decision['timestamp'].split('T')[0]
        holding_days = signal_packet.get('holding_days', 0)
        realized = signal_packet.get('realized', False)
        decision['tax_notes'] = self.tax_filter.evaluate_trade_tax_notes(
            current_symbol, trade_date_str, holding_days, realized)

        margin_enabled = signal_packet.get('margin_enabled', False)
        involves_short_option = signal_packet.get('involves_short_option', False)

        if margin_enabled and not involves_short_option:
            decision['margin_risk'] = 'Low (cash equity margin)'
        elif margin_enabled and involves_short_option:
            decision['margin_risk'] = 'Moderate to High (requires margin coverage on short leg)'
        elif not margin_enabled and involves_short_option:
            decision['margin_risk'] = 'Ineligible: naked short option in cash-only account'
        else:
            decision['margin_risk'] = 'Low'

        if allowed_by_sis and rep_ok:
            decision['final_decision'] = 'APPROVED'

        self.decision_log.append(decision)
        return decision

    def recent_decisions(self, n=5):  # Returns the last n trade evaluations
        return self.decision_log[-n:]

    def get_decision_by_id(self, signal_id):  # Looks up a specific signal's decision
        for entry in reversed(self.decision_log):
            if entry['signal_id'] == signal_id:
                return entry
        return None
