# Execute New Case Factory

You are authorized to prepare a new Case OS control plane proposal from the user's request and available evidence.

## Process

1. Run Case Intake.
2. Count complexity signals.
3. Choose:
   - Simple
   - Full Case OS
   - Dedicated Legacy
4. Search for an existing Project/Case before creating a new one.
5. If a matching case exists, update/reuse it rather than duplicating it.
6. For a new Full Case:
   - prepare Case Registry properties
   - prepare Control Tower
   - prepare initial Critical Path
   - prepare nearest Gate
   - prepare initial RAID
   - prepare required Documents
   - prepare Stakeholders
   - prepare Open Decisions
7. Every hard date must include certainty and evidence reference.
8. Do not copy raw files into the control plane when Drive/official system should remain the original.
9. Protected baseline decisions remain approval-gated.

## Required machine output

Produce JSON conforming to:

`case-os/schemas/case_bootstrap.schema.json`

## Required human summary

Then return:

```
[CASE FACTORY]
Mode:
Why:
Case:
Next irreversible event:
Nearest gate:
Critical path:
Missing evidence:
Created/updated control objects:
Approval required:
Next 3 actions:
```

If the connected Notion/PMO tool is available, you may instantiate low-risk metadata and candidate records.
Do not perform irreversible external actions as part of case creation.
