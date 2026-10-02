# Browser Automation Policy

Browser automation is a fallback, not the default integration layer.

## Use order

1. native Workspace action
2. official API
3. approved MCP
4. Dify/approved connector
5. browser automation

## Browser automation is appropriate for

- internal UI without API
- repetitive read-only navigation
- form prefill
- retrieving non-sensitive status
- human-approved final submit

## Keep human approval for

- send/post/submit
- deleting
- changing permissions
- financial/contractual actions
- changing dates/owners/status
- publishing externally

## Reliability

Every browser workflow must have:
- expected page/title check
- target element verification
- timeout
- retry ceiling
- screenshot/evidence where policy allows
- NEEDS_HUMAN on unexpected UI
- no blind click by coordinates when a semantic selector exists

Never bypass company security controls or MFA.
