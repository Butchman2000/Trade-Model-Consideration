# --- Trade-Model-Consideration ---
Collection of several trading models, constraints, code, and backtesting results.




# --- Audit and Compliance Tools ---

This project includes a self-contained audit framework designed to meet high-integrity logging, traceability, and external validation requirements. It supports oversight from limited partners, auditors, or quality control personnel.

Features

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


This is intended to simulate a change control step prior to the continuation of risk-sensitive operations.

