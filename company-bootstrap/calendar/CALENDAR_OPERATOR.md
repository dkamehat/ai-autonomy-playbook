# Calendar Operator Contract

## Input

Natural language task/action.

## Output before write when ambiguous

```
[CALENDAR PROPOSAL]
Title:
Date:
Start:
Duration:
Source:
Conflict:
Reason:
```

## Auto-create allowed only when

- date/time are explicit
- no conflict
- user explicitly asked to create
- event does not invite external people
- no existing meeting is moved/cancelled

## Human approval required

- moving/cancelling event
- adding attendees
- external guests
- interpreting ambiguous deadline
- recurring schedule creation when cadence is not explicit

## Recommended event format

Title:
`[FOCUS] <action>`

Description:
```
Source:
Expected outcome:
Evidence/Doc:
Next gate:
```

The Calendar is for commitments/time blocks, not the project SoT.
