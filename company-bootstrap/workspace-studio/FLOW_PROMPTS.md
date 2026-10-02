# Workspace Studio — Copy/Paste Flow Prompts

Workspace Studioの「Geminiに自動化したいことを説明」にそのまま貼るためのPrompt。

## Flow 1 — Morning Brief

平日の朝に実行するFlowを作ってください。

使用するアプリ:
- Google Calendar
- Google Tasks
- Gmail（管理者設定と会社Policyで許可される場合）
- Google Chat（利用可能なら）

処理:
1. 今日のCalendarを取得
2. 今日/期限接近のTasksを取得
3. 重要度が高い未読/要対応メールを抽出（許可される場合のみ）
4. Geminiで以下を生成
   - 今日のP0 最大3件
   - 会議前に準備が必要なもの
   - Blocker
   - 時間不足/重複の懸念
5. 自分向けのChatまたは指定された安全な出力先へBriefを送る

禁止:
- Calendarの既存予定を移動/削除しない
- メールを自動送信しない
- Taskの期限/担当者を変更しない

曖昧な場合は提案だけにしてください。

## Flow 2 — Meeting Follow-up

承認済みのMeeting noteまたはTranscriptが作成された後に、
会議内容をPMO更新候補へ変換するFlowを作ってください。

処理:
1. Meeting sourceを読む
2. Geminiで以下を抽出
   - Decision
   - Task / Action
   - Risk
   - Issue / Blocker
   - Stakeholder
   - System / Tool
   - Rule / Policy
   - Fact
   - Milestone
   - Open Question
3. 各項目にsource/evidenceを付ける
4. TaskのOwner/Dueが明示されていない場合は推測しない
5. Decision/Deadline/Owner/Policy/Risk severityは「要承認」とする
6. reviewable follow-up documentを作る
7. P0/Blocked/重要Decision/要承認だけ通知する

禁止:
- Transcriptの内容だけで既存SoTを自動上書きしない
- Rule/Policyを公式扱いにしない
- 会社Policyで認められていない外部サービスへデータを送らない

## Flow 3 — Calendar Work-block

承認済みTaskまたは手動リクエストから、
作業時間をCalendarへ確保するFlowを作ってください。

処理:
1. TaskのAction/期限/推定時間を読む
2. Calendarの空き時間を検索
3. 1〜3個の候補を出す
4. 日時/所要時間が明示済みで、競合がなく、ユーザーが作成を明示した場合のみeventを作る
5. event descriptionにsource/expected outcome/next gateを入れる

Human Approval:
- 既存予定の移動/削除
- 外部attendee追加
- 曖昧なdeadline解釈
- recurring event
