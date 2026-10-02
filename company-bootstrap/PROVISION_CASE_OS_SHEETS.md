# Provision Company Case OS in Google Sheets

Use this when the company-side control plane should live in Google Workspace.

## Recommended provisioning path

### Path A — Gemini in Sheets
1. Create one blank Google Sheet manually.
2. Name it:
   `BizOps Case OS｜Control Plane`
3. Open Gemini in Sheets.
4. Paste the prompt below.
5. Review Gemini's plan before applying it.

### Path B — Gemini in Drive
If your account exposes spreadsheet generation in Gemini in Drive, ask it to create:
`BizOps Case OS｜Control Plane`
Then open the generated Sheet and run the same prompt in Gemini in Sheets.

Do not depend on Gemini Apps to create/move Drive folders. Create the parent folder manually if needed.

---

# Provisioning Prompt

You are provisioning a company-side Case OS control plane in this Google Sheets workbook.

This workbook is the structured operational control plane. It is not the file/document source of truth.

## Global rules

- Create or rename sheets exactly as specified below.
- Row 1 contains headers and starts at A1.
- Freeze row 1.
- Turn on filters.
- Do not merge cells.
- Use ISO-style dates: YYYY-MM-DD.
- Use dropdowns for enum/status columns.
- Use checkboxes for boolean columns.
- Do not create sample company-confidential data.
- Do not invent deadlines, owners, decisions, or policies.
- Keep raw documents/emails/transcripts outside this workbook; store only source references and sanitized summaries.
- Use stable IDs as the logical relation mechanism across sheets.
- Case_ID is required on every operational row except 99_CONFIG.
- Do not create dashboards/charts yet.
- Do not create formulas that silently modify source data.

Create these sheets:

## 00_CASES

Columns:
Case_ID
Case_Name
Case_Type
PMO_Mode
Sensitivity
Health
Mission
Current_State
Primary_SoT
Next_Gate
Next_Irreversible_Event
Next_Irreversible_Event_Date
Control_Tower_Ref
Operating_Model
Owner
Last_PMO_Audit
Status

Dropdowns:
Case_Type =
Transaction / Purchase
Legal / Administration
Finance
Career / Onboarding
Business / Revenue
Health / Procedure
Research / Decision
Other

PMO_Mode =
Simple
Full Case OS
Dedicated Legacy

Sensitivity =
Public
Personal
Sensitive
Highly Sensitive

Health =
GREEN
YELLOW
RED

Status =
Active
Waiting
Closed
Archived

## 01_WBS

Columns:
Task_ID
Case_ID
Task
Item_Type
Status
Priority
Critical_Path
Hard_Deadline
Workstream
Owner
Counterparty
Planned_Start
Deadline
Follow_Up
Done_Date
Next_Action
Done_Criteria
Dependency
Evidence_Ref
Certainty
Last_Reviewed

Dropdowns:
Item_Type = Task, Milestone, Control
Status = TODO, IN PROGRESS, WAITING, BLOCKED, DONE, NOT REQUIRED
Priority = P0, P1, P2, P3
Certainty = Confirmed, Reported, Estimated, Unknown

Checkboxes:
Critical_Path
Hard_Deadline

## 02_DOCUMENTS

Columns:
Document_ID
Case_ID
Document
Status
Required
Required_By
Owner
Issuer
Document_Type
Source_Ref
Version
Issued_Date
Expiry_Date
Sensitivity
Verification_Basis
Last_Checked

Dropdowns:
Status = MISSING, REQUESTED, RECEIVED, VERIFIED, EXPIRED, NOT REQUIRED
Sensitivity = Public, Personal, Sensitive, Highly Sensitive

Checkbox:
Required

## 03_DECISIONS

Columns:
Decision_ID
Case_ID
Decision
Status
Decision_Date
Decision_Deadline
Options
Selected_Decision
Basis
Evidence_Ref
Reversal_Trigger
Impact
Owner
Sensitivity
Last_Reviewed

Dropdowns:
Status = PENDING, DECIDED, SUPERSEDED
Sensitivity = Public, Personal, Sensitive, Highly Sensitive

## 04_RAID

Columns:
RAID_ID
Case_ID
RAID_Item
Type
Status
Severity
Owner
Due
Summary
Trigger_Condition
Impact
Mitigation
Dependency_Ref
Evidence_Ref
Last_Reviewed

Dropdowns:
Type = Risk, Assumption, Issue, Dependency
Status = OPEN, MONITORING, MITIGATED, CLOSED
Severity = Critical, High, Medium, Low

## 05_GATES

Columns:
Gate_ID
Case_ID
Gate
Status
Event_Date
Hard_Deadline
Pass_Criteria
Open_Items
Evidence_Ref
Owner
Last_Reviewed

Dropdown:
Status = OPEN, READY, PASSED, FAILED

Checkbox:
Hard_Deadline

## 06_COMMUNICATIONS

Columns:
Communication_ID
Case_ID
Communication
Type
Status
Counterparty
Subject
Occurred_Sent
Follow_Up
Requested_Promise
Outcome
Evidence_Ref
Workstream
Sensitivity
Last_Reviewed

Dropdowns:
Type = OUTBOUND, INBOUND, MEETING, CALL, OTHER
Status = OPEN, WAITING, RESPONDED, CLOSED
Sensitivity = Public, Personal, Sensitive, Highly Sensitive

## 07_SUBMISSIONS

Columns:
Submission_ID
Case_ID
Submission
Status
Counterparty
Due
Submitted_At
Receipt_At
Package_Summary
Version
Evidence_Ref
Sensitivity
Last_Reviewed

Dropdowns:
Status = PREPARING, SUBMITTED, RECEIPT CONFIRMED, ADDITIONAL REQUEST, CLOSED
Sensitivity = Public, Personal, Sensitive, Highly Sensitive

## 08_CHANGES

Columns:
Change_ID
Case_ID
Change
Status
Change_Type
Old_Baseline
New_Baseline
Reason
Impact
Required_Actions
Approved_At
Implemented_At
Evidence_Ref
Last_Reviewed

Dropdowns:
Status = PROPOSED, APPROVED, IMPLEMENTED, REJECTED
Change_Type = Scope, Date, Amount, Counterparty, Decision, Requirement, Other

## 09_EVIDENCE_EVENTS

Columns:
Event_ID
Case_ID
Event
Source_Type
Occurred_At
Ingested_At
Authority
Certainty
Sensitivity
Source_Ref
Summary
Source_Key_Hash
Routing_Status
Needs_Approval
Workstream
Last_Processed

Dropdowns:
Source_Type = Email, Document, Call, Meeting, Voice, Web, Form, System, Manual
Authority = Official, Direct, Reported, Derived, Unverified
Certainty = Confirmed, Reported, Estimated, Unknown
Sensitivity = Public, Personal, Sensitive, Highly Sensitive
Routing_Status = NEW, ROUTED, NO_CHANGE, NEEDS_REVIEW, APPLIED, CONFLICT

Checkbox:
Needs_Approval

## 10_STAKEHOLDERS

Columns:
Stakeholder_ID
Case_ID
Stakeholder
Role
Organization
Type
Authority
Status
Contact_Ref
Sensitivity
Notes
Last_Verified

Dropdowns:
Type = User / Family, Counterparty, Authority, Professional, Vendor, Internal, Other
Authority = Decision Maker, Owner, Official Source, Advisor, Contributor, Observer
Status = Active, Waiting, Inactive
Sensitivity = Public, Personal, Sensitive, Highly Sensitive

## 99_CONFIG

Create a two-column key/value table with:

Schema_Version | 1.0
Date_Format | YYYY-MM-DD
Primary_ID | Case_ID
Default_PMO_Mode | Simple
Full_Case_Threshold | 2 complexity signals
Notification_Mode | Exception only
Raw_Files_In_Sheet | No
Raw_Email_In_Sheet | No
Raw_Transcript_In_Sheet | No
Decision_Auto_Write | No
Hard_Deadline_Auto_Change | No
External_Action_Auto_Execute | No

## Conditional formatting

Apply simple conditional formatting:

01_WBS:
- Priority P0: prominent
- Status BLOCKED: prominent
- Status WAITING: warning
- Deadline before today and Status not DONE/NOT REQUIRED: overdue

02_DOCUMENTS:
- MISSING / EXPIRED: warning
- VERIFIED: complete

04_RAID:
- Critical / High: prominent

05_GATES:
- FAILED: prominent
- READY: warning
- PASSED: complete

09_EVIDENCE_EVENTS:
- CONFLICT: prominent
- NEEDS_REVIEW: warning
- APPLIED / NO_CHANGE: complete

## Final validation

After building, verify:

1. all named sheets exist
2. every header starts at A1
3. no merged cells exist
4. every operational sheet has Case_ID
5. all status/enum fields use dropdowns where supported
6. date columns use a consistent date format
7. no sample confidential data was inserted
8. no irreversible action automation was created

Then return only:

DONE:
- sheets created
- validations created
- formatting created

NEEDS REVIEW:
- anything Gemini could not create automatically

NEXT:
- create the first Case row only after I provide or approve its baseline.
