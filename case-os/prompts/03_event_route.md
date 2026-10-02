# Case Event Routing

Process one new event: email, document, call, meeting, voice note, web evidence, form or system event.

## Step 1 — Source

Capture:
- Case
- source type
- occurred date
- authority
- certainty
- sensitivity
- source reference
- sanitized summary
- source key/hash where available

## Step 2 — Extract atomic objects

Possible objects:
- action
- document
- decision
- risk
- assumption
- issue
- dependency
- gate condition
- communication
- submission
- baseline change
- stakeholder

## Step 3 — Reconcile

For each object:
- find canonical existing record
- compare effective date / authority / semantic state
- classify:
  - CREATE
  - UPDATE
  - NO_CHANGE
  - CONFLICT

Do not overwrite stronger/confirmed state with weaker or older evidence.

## Step 4 — Approval

Protected changes remain proposals.

## Step 5 — Output

```
[EVENT ROUTING]
Source:
Case:
CREATE:
UPDATE:
NO_CHANGE:
CONFLICT:
Approval required:
P0/Blocker/Due alert:
Relations/evidence:
Next action:
```
