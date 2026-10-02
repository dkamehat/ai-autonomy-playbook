# Company AI Operator Bootstrap

会社PCで **Gemini / Google Workspace Studio / Dify / Claude / browser automation** を使い、
「会話 → 情報収集 → Calendar/Task/Meeting/PMO更新候補 → 通知」までを
できるだけ自然言語・音声で操作するための公開Bootstrap Kitです。

このディレクトリには **公開してよい汎用設計だけ** を置きます。

## 原則

1. 会社固有情報・顧客情報・内部ルール本文・認証情報はこの公開repoへ書かない
2. Company dataはCompany-approved environment内で処理する
3. Public repoは **Prompt / Schema / Workflow Contract / Operating Method** の配布元
4. SoT更新は protected field ほどHuman Approvalを残す
5. LLMは抽出・要約・routing候補に使い、重要なmutation authorizationは決定論的にする
6. Browser automationはAPI/Workspace integrationが無い時の最後の手段

## Company-PC recommended stack

### Tier 1 — Gemini + Google Workspace
最優先。追加installなしで成立しやすい。

- Gemini: 対話 / 調査 / drafting / Workspace操作
- Google Calendar: calendar/time blocking
- Gmail: retrieval / draft
- Drive/Docs: source / output
- Tasks: lightweight actionable items
- Workspace Studio: schedule / event-driven automation / multi-step flows
- Meet notes/transcript: policy-approved時のみmeeting intake source

### Tier 2 — Dify
Google外または複雑Agent/Workflowが必要な場合。

- multi-step workflow
- RAG / knowledge base
- HTTP / API tools
- custom tools
- approval-gated automation
- model abstraction

**弱い会社PCにDifyをlocal self-hostしない。**
会社側で承認されたshared/cloud/VPC instanceがある場合に利用する。

### Tier 3 — Claude
利用承認後、複雑な設計・コード・長文レビューの補助。
Company dataの利用範囲は会社Policyに従う。

## 最短セットアップ

1. Geminiにこの公開repo URLを渡す
2. `GEMINI_INSTRUCTIONS.md` を読み込ませる
3. Workspace Connected Appsの利用可否を確認
4. Workspace Studioが使える場合は `workspace-studio/FLOWS.md` の順で作る
5. 音声入力は `VOICE.md`
6. Dify申請が通ったら `dify/README.md`

## Daily command concept

音声またはテキストで:

- 「今日の予定と重要メールを見て、P0を3つ出して」
- 「この会議メモからDecision/Task/Riskだけ抽出して」
- 「明日15時にこのActionの作業ブロックをCalendarへ入れて」
- 「この情報はどのWorkstreamに属する？」
- 「更新候補を出して。勝手にDecisionや期限は変更しないで」
- 「今日の終わりにDone/Blocked/Nextをまとめて」

## Data boundary

Public GitHubは **会社へ持ち込む“設計言語”の配布経路** です。
Company contentをPublic GitHubへ戻す経路ではありません。
