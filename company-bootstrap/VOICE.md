# Voice-first Company PC

## Goal

会社PCの操作を「キーボード中心」から「音声 → Gemini/Flow → Action」へ寄せる。

## Level 1 — Dictation

最小構成。

Macの標準音声入力を使い、Gemini/Chat/Docs等のテキストボックスへ直接話す。

推奨:
- 会社Policy上許可されるか確認
- macOSのKeyboard > Dictationで処理方法/Privacy表示を確認
- 認証情報・秘密情報を音声入力しない

## Level 2 — Voice Control

MacのVoice Controlが許可される場合:

- アプリを開く
- スクロール
- ボタン操作
- テキスト入力
- Geminiへ指示

これにより「Geminiを開く → 音声で指示 → Calendar/Workspace操作」がかなりhands-freeになる。

## Level 3 — Gemini desktop/browser microphone

利用可能ならGeminiのマイク入力を使う。

Voice command examples:

### Morning
「今日のCalendarと重要メールを見て、P0を3件に絞って。予定変更は提案だけにして」

### Meeting
「このMeeting noteからDecision、Task、Risk、Open Questionを抽出。既存情報とのConflict候補も出して」

### Calendar
「このActionを明日午後に60分確保したい。空いている時間を探してCalendarへ追加する前に候補を出して」

### Research
「DriveとGmailからこのテーマの一次情報を探し、出典付きで5行にまとめて」

### End of day
「今日のCalendar、Tasks、作業結果からDone / Blocked / Tomorrow P0を作って」

## Voice safety

音声UIは便利だが、誤認識を前提にする。

必ず確認を残す:
- 日時
- 宛先
- 外部送信
- Decision
- delete
- access/permission
- deadline
