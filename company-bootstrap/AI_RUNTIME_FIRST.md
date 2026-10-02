# AI Runtime First — Company PC

Do **not** start by manually building Case OS tables.

First make the company Google environment operable by AI.

## Target

```
Voice / rough text
→ Gemini
→ Google Workspace
→ Workspace Studio
→ Calendar / Gmail / Drive / Tasks / Chat
```

Case OS / Sheets are backend control structures. The human should not maintain them manually.

## Phase 0 — Gemini capability check

In Gemini, run:

```
あなたを私のCompany AI Operatorとして使います。

まず実行環境を確認してください。

以下について、
READ / DRAFT / WRITE / AUTOMATE の4段階で
「利用可能 / 管理者無効 / 未確認」を判定してください。

- Gmail
- Google Calendar
- Google Drive
- Google Docs
- Google Sheets
- Google Tasks
- Google Chat
- GitHub
- Workspace Studio

実際に利用できるConnected Appsは、可能な範囲で簡単なread-only確認を行ってください。
会社規程を推測しないでください。

最後に、

1. 今すぐAIが操作できるGoogleサービス
2. 私の承認が必要な操作
3. 管理者申請が必要なもの
4. 今日作れる自動化

だけ返してください。
```

## Phase 1 — Workspace Studio

Open:

https://studio.workspace.google.com

If it opens, the AI execution runtime exists.

Use:
`company-bootstrap/workspace-studio/AI_OPERATOR_RUNTIME_FLOW.md`

Do not build Case OS yet.

## Phase 2 — Voice

Use:
- zero-install: macOS Dictation → Gemini
- later: Koe → Gemini

The user speaks a rough request. Gemini should execute through Connected Apps when safe.

## Phase 3 — Backend only when needed

After the runtime works:

- create Case OS Sheet only if structured persistent state is necessary
- let Gemini in Sheets provision it
- let Workspace Studio write rows
- do not ask the user to maintain the workbook manually

## Success condition

The runtime is ready when the user can say/type:

> 明日の空いてるところに、この作業を60分入れたい

and the environment can:
1. inspect Calendar
2. propose/perform the safe action
3. ask approval only where required

Then proceed to meeting intake and Case OS automation.
