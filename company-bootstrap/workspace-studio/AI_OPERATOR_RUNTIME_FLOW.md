# Workspace Studio — AI Operator Runtime

Paste the following into Workspace Studio's Gemini flow builder.

## Flow A — Personal AI Action Inbox

Create a flow for my own company account.

Starter:
- When I get a Google Chat message
- Prefer a private/self-use space if available
- Only process messages beginning with `AI:`

Steps:
1. Ask Gemini to interpret the message as a work request.
2. Allow Gemini to use Workspace sources I can access.
3. Classify the request into one of:
   - READ
   - TASK
   - CALENDAR
   - DRAFT
   - MEETING_FOLLOWUP
   - CASE
   - NEEDS_APPROVAL
4. Return a concise execution plan.
5. For low-risk requests:
   - TASK → create a Google Task when title/date are explicit
   - CALENDAR → block time only when date/time/duration are explicit and no existing event is moved
   - READ → retrieve/summarize from approved Workspace sources
6. For protected/ambiguous requests:
   - do not execute
   - notify me in Chat with:
     [APPROVAL REQUIRED]
     Request:
     Proposed action:
     Reason:
     Missing/ambiguous:
7. Notify me in Chat with:
   Done:
   Need approval:
   Blocked:
   Next:

Safety:
- never move/delete an existing Calendar event automatically
- never send an email automatically
- never change permissions
- never infer a hard deadline as fact
- never expose Workspace data to an unapproved external service
- do not create Case OS records yet; return CASE as a candidate

## Flow B — Morning Operator

Starter:
- Weekdays in the morning

Steps:
1. inspect today's Calendar
2. inspect Tasks due today/overdue
3. use Gemini to produce:
   - P0 max 3
   - meetings needing preparation
   - blockers
   - work blocks needed
4. notify me in Chat

Do not reschedule meetings automatically.

## Flow C — Meeting Follow-up

Starter:
- Based on a meeting / approved meeting note when available

Steps:
1. use approved meeting source
2. Ask Gemini to extract:
   - Decision
   - Task
   - Risk
   - Blocker
   - Open Question
3. do not finalize Decision/Owner/Due when ambiguous
4. create clear low-risk Tasks only if explicit
5. notify me in Chat with:
   - actions
   - approval-required items
   - next step

Do not write to public GitHub or unapproved external services.
