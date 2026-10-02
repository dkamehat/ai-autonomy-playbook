# START HERE — Company AI Operator

会社PCでの最短セットアップ。

## 0. 前提

この公開repoには汎用Prompt/Schema/Workflowだけがあります。
会社固有情報をGitHubへ書き戻さないでください。

## 1. GeminiをCompany Operator化

Geminiでこのrepoを添付/参照し、次に進む。

1. `company-bootstrap/BOOTSTRAP_PROMPT.md` を読む
2. `company-bootstrap/GEMINI_INSTRUCTIONS.md` を運用Contractとして使う
3. Calendar / Gmail / Drive / Docs / Tasks / Chat / GitHub の能力を
   READ / DRAFT / WRITE / AUTOMATEで棚卸しする

期待する最初の回答:

```
Capabilities
- Calendar:
- Gmail:
- Drive:
- Docs:
- Tasks:
- Chat:
- GitHub:
- Workspace Studio:

Admin approval required:
-

Today I can automate:
1.
2.
3.
```

## 2. Workspace Studio

利用可能なら
`company-bootstrap/workspace-studio/FLOW_PROMPTS.md`
の3本を上から作る。

1. Morning Brief
2. Meeting Follow-up
3. Calendar Work-block

## 3. Voice

まずMac標準DictationでGeminiへ入力する。
詳細:
`company-bootstrap/VOICE.md`

最初の音声:

> 今日のCalendarを見て、午前中に準備が必要な予定とP0を3件だけ教えて。予定はまだ変更しないで。

## 4. Dify

Dify承認後のみ:
`company-bootstrap/dify/README.md`

Workspace-nativeで足りる処理をDifyへ重複実装しない。

## 5. Daily UX

朝:
> 今日のCalendar、Tasks、重要メールからP0を3つ。

会議後:
> このMeeting noteからDecision/Task/Risk/Open Questionを抽出して。既存情報を勝手に上書きしない。

作業確保:
> このActionを今週中に終わらせたい。Calendarの空きを見て60分の候補を3つ。追加前に確認して。

夕方:
> 今日のDone/Blocked/Carry-over/Tomorrow P0をまとめて。

## 6. Escalation

以下はAIが勝手に確定しない:
- Decision
- Deadline
- Owner
- Priority/Status with execution impact
- Rule/Policy
- Risk severity/status
- Delete
- Permission
- external send/invite


## 7. Koe — voice command bar

If company policy allows running a small unsigned/local app, use:
`company-bootstrap/koe-mac/`

Koe adds a global `Control + Option + Space` voice capture flow and wraps rough speech into the Company Operator contract.

Until installation is approved, use the **Zero-install path**:
1. keep Gemini open
2. use macOS Dictation directly in the prompt box
3. start the first chat with `BOOTSTRAP_PROMPT.md`
4. speak rough requests; Gemini should follow the Operator contract


## 8. Complex project / case

When work becomes a multi-step, high-stakes case, load:

`case-os/CASE_OS_AGENT.md`

Then use:

`case-os/prompts/01_case_intake.md`

Voice/text example:

> これ案件化して。ゴールと期限と関係者を整理して、Case OSが必要か判定して。必要ならControl Towerの初期状態まで作って。

Case OS should be used for complex cases; do not force it onto one-off simple tasks.


## 9. Provision the Company Case OS storage

If Gemini in Sheets is available, use:

`company-bootstrap/PROVISION_CASE_OS_SHEETS.md`

Recommended:
1. manually create one blank Google Sheet named `BizOps Case OS｜Control Plane`
2. open Gemini in Sheets
3. paste the provisioning prompt
4. review Gemini's build plan
5. apply it
6. do not add real case data until the schema/validation review passes

This creates the shared register structure. Do not create one workbook per case.
