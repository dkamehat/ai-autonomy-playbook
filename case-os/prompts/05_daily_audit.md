# Case OS Daily Exception Audit

Audit active Full/Dedicated cases.

Notify only when at least one condition exists:

- overdue
- P0 due <= 3 days
- Critical Path WAITING >= 2 business days
- P0 BLOCKED
- due <= 7 days with missing owner/dependency
- Gate readiness regressed
- Critical/High RAID
- Decision/Approval blocking progress
- Required document missing/expired near gate
- event CONFLICT / pipeline failure

For each exception return:
- Case
- severity
- item
- deadline/follow-up
- owner/counterparty
- required action
- evidence/state reference

If no meaningful exception exists, produce no notification.
