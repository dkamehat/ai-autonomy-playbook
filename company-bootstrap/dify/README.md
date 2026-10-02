# Dify Role in Company AI Operator

Dify is **not the first dependency** when Gemini + Workspace Studio can perform the task.

Use Dify when you need:

- custom multi-step agent workflows
- internal knowledge/RAG
- model switching
- custom HTTP/API tools
- structured output pipeline
- reusable internal AI app
- tool routing beyond Workspace-native integrations

## Deployment

For a low-spec company Mac:
- do not self-host locally unless IT explicitly approves and hardware is sufficient
- prefer company-approved shared Dify / cloud / VPC deployment
- keep runtime and data in Company Zone

## Recommended app: PMO Intake Agent

Input:
- approved meeting note/transcript
- manually pasted sanitized note
- company document reference

Workflow:
1. normalize
2. structured extraction
3. classify Project/Workstream/Domain
4. retrieve existing PMO metadata
5. output mutation candidates
6. deterministic reconciliation service decides mutation status
7. human approval for protected changes
8. writer/API applies approved patch
9. notification

Dify/LLM must **not** be the authority for CREATE/UPDATE approval.

## Tool contract

Useful tools:

- search_company_docs(query)
- get_calendar(date_range)
- create_calendar_event(draft)
- get_pmo_record(canonical_key)
- propose_pmo_patch(...)
- apply_approved_pmo_patch(...)
- send_notification(...)
- lookup_person(...)
- get_meeting_notes(...)

Names are examples; map them to approved company APIs/MCP/tools.

## MCP / tool strategy

Prefer:
1. official Workspace integrations
2. approved internal API
3. approved MCP server
4. Dify plugin/tool
5. browser automation as last resort
