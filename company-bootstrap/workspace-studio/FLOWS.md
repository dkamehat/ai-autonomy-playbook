# Google Workspace Studio — First Flows

利用可能なら、会社PC自動化の第一候補。

## Flow 01 — Morning Brief

Trigger:
- weekday schedule

Read:
- Calendar
- Tasks
- optionally Gmail/Chat within company policy

Gemini step:
- today commitments
- P0 max 3
- blockers
- preparation needed before meetings

Output:
- Google Chat self/approved channel
- optional Google Doc daily log

Do not:
- reschedule existing meetings automatically

## Flow 02 — Meeting Follow-up

Trigger:
- meeting note/transcript created
- or manual trigger

Steps:
1. read approved meeting source
2. Ask Gemini to extract Decision / Task / Risk / Open Question
3. create a reviewable follow-up document
4. create Tasks only for approved/clear Action Items
5. propose Calendar work blocks
6. notify only protected/urgent items

Protected:
- Decision
- due date interpretation
- owner ambiguity
- policy/rule interpretation

## Flow 03 — Calendar Work-block Assistant

Trigger:
- new approved task
- manual request

Steps:
1. inspect Calendar availability
2. propose 1–3 work blocks
3. require approval when duration/priority is ambiguous
4. create Calendar event
5. link source task/doc in description

## Flow 04 — Daily EOD

Trigger:
- weekday schedule

Read:
- Calendar
- Tasks
- daily work log

Output:
- Done
- Blocked
- Carry-over
- Tomorrow P0

## Flow 05 — Information Intake

Trigger:
- starred/specified Gmail
- new file in approved Drive folder
- manual URL/doc selection

Steps:
1. classify domain/workstream
2. extract action/decision/risk/fact
3. detect duplicate candidate
4. generate update proposal
5. protected changes require approval

## Flow design rule

Use Workspace-native action before browser automation.
Use browser automation only when no approved integration/API exists.
