::Confidential -- For Jade Harbor Finance Only

All material belongs to the author, and is not to be copied, altered, or used without express permission.
The intellectual property involved in this repository belongs solely to the author, or assigns.

This README is unfinished, and is evolving as it moves forward in development.




# --- Trade-Model-Consideration ---
Collection of several trading models, constraints, code, and backtesting results.

The trading activity within each model, is limited to AVOID the dates and times of the exclusion parameters.
The exception is the SPX VIX model, which may benefit from index/volatility disconnection; flagging is used instead.


# --- Unfinished Material ---
Collection of some additional models and alternative ideas, in need of further consideration, adaptation, or removal.

They are not to be involved in any other part of the repository, and are solely for exploratory purposes.



# --- Audit and Compliance Tools ---

This project includes a self-contained audit framework designed to meet high-integrity logging, traceability, and external validation requirements. It supports oversight from limited partners, auditors, or quality control personnel.

Features:

Structured JSON logging of all monitored events, including timestamps and context

Environment variable validation for secure credential handling

External approval gating using file-based control flags

Modular design that isolates audit logic from trading logic

Audit Tests

Test functionality is provided in tests/test_audit_tools.py to validate the audit logging and approval system.

To run:

python -m tests.test_audit_tools

External Approval Flag Format

Some logic may pause until an external reviewer approves a file. The flag must follow this structure:

{
  "approved": true,
  "approved_by": "example@domain.com",
  "timestamp": "2025-05-01T14:33:00"
}

This is intended to simulate a change control step prior to the continuation of risk-sensitive operations.


# Third-Party Software Attribution

This project may incorporate components from the open-source project TradingGym, available at https://github.com/Yvictor/TradingGym, which is licensed under the MIT License.
All modifications and proprietary models developed on top of this framework are original works and remain the intellectual property of Brian Anderson, or Jade Harbor, possibly dba Jade Harbor Finance, or assigns.
Backtesting may be done with TradingGym components, yet that remains to be seen.


