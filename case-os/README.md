# Case OS — Project Factory

Case OS is a reusable control system for complex personal projects/cases.

Examples:
- property purchase
- immigration / naturalization
- mortgage / insurance
- onboarding / career transition
- side-business engagements
- high-stakes administrative procedures

## Architecture

```
Email / Doc / Call / Meeting / Voice / Web
                    ↓
           Evidence & Event Intake
                    ↓
        Router / Reconciliation
                    ↓
WBS / Document / Decision / RAID / Gate /
Communication / Submission / Change / Stakeholder
                    ↓
             Case Control Tower
```

## Where things live

- **Notion**: Case Registry + shared control registers
- **Drive / official system**: file originals
- **Gmail**: email originals
- **Calendar**: time commitments, not project SoT
- **GitHub**: generic prompts, schemas, agent contracts, automation
- **Slack / Chat**: exception notification only

## Key design decision

Do **not** create a new set of databases for every case.

One shared register set is filtered by a `Case` relation.

Simple work stays in a lightweight task system. Full Case OS is activated only when control complexity justifies it.

## Full Case OS threshold

Use Full Case OS when 2 or more apply:

- hard deadline
- 2+ external counterparties
- 5+ required documents
- irreversible decision/event
- material financial impact
- legal/tax/loan/medical high-stakes
- waiting/follow-up management
- multi-thread / multi-agent execution

## Prompts

- `01_case_intake.md`: decide whether a case needs Full Case OS
- `02_thread_start.md`: restore current case state
- `03_event_route.md`: route a new event into registers
- `04_thread_close.md`: sync state before ending a work thread
- `05_daily_audit.md`: exception-only daily PMO audit
- `06_weekly_audit.md`: weekly quality/control review

## Core invariant

A chat is not the source of truth.

Important work is complete only when the relevant Case OS state and evidence are synchronized.
