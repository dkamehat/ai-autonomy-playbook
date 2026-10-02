# Case Intake / Factory

You are starting or reviewing a project/case.

Collect or infer from supplied context:

- case name
- mission / desired outcome
- current state
- hard dates
- counterparties / authorities
- required documents
- financial/legal/tax/medical/contractual impact
- irreversible decisions/events
- waiting/follow-up needs
- source systems
- sensitivity

## Classify PMO Mode

Full Case OS if at least two:
- hard deadline
- 2+ external counterparties
- 5+ documents
- irreversible decision/event
- material financial impact
- high-stakes domain
- waiting/follow-up tracking
- multi-thread/multi-agent execution

Otherwise use Simple mode.

Use Dedicated Legacy only when a mature existing PMO already exists.

## If Full

Return:

```
[CASE BOOTSTRAP]
Name:
Case ID candidate:
Case Type:
PMO Mode:
Sensitivity:
Mission:
Current State:
Primary SoT:
Hard Dates:
Next Irreversible Event:
Initial Gate:
Critical Path candidates:
Required Documents:
Initial RAID:
Stakeholders:
Open Decisions:
Automation candidates:
Missing evidence:
Next 3 actions:
```

Do not invent hard deadlines or authorities.
