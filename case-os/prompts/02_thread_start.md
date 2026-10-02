# Case Thread Start

Restore this case before doing new work.

1. identify Case / Case ID
2. retrieve Case Registry
3. retrieve:
   - P0
   - Critical Path
   - overdue
   - due <= 7 days
   - WAITING
   - BLOCKED
   - nearest OPEN/READY Gate
   - PENDING Decisions
   - Critical/High RAID
   - MISSING/REQUESTED/EXPIRED documents
   - NEW/CONFLICT events
4. identify this thread's workstream
5. match the user's request to existing records

Return a concise state:

```
Case:
Health:
Next irreversible event:
Nearest gate:
Critical path:
Waiting:
Blocked:
Decision required:
This thread:
```

Do not create duplicate tasks if the requested outcome already exists.
