# Case Thread Close / Sync

Before ending this work thread, synchronize only changes that occurred in this thread.

Do not recreate historical records.

Checklist:

1. reconcile thread events vs Case OS
2. update WBS status/evidence/deadline/dependency
3. outbound request → Communication + WAITING + follow-up
4. inbound response → Communication outcome + done criteria check
5. document: MISSING → REQUESTED → RECEIVED → VERIFIED as evidence supports
6. material baseline change → Change Log + cascade
7. update Decision / RAID / Gate / Submission
8. verify DONE has evidence
9. verify WAITING has counterparty + follow-up
10. verify BLOCKED has dependency/unblock condition
11. update Case Health / Next Gate / Next Irreversible Event / Last Audit if changed

Return:

```
[CASE SYNC]
Updated:
Created:
No change:
Conflicts:
Waiting:
Blocked:
Approval needed:
Next irreversible event:
Next 3 actions:
```
