# Koe for macOS — Voice Command Bar

**Koe** is a tiny macOS menu-bar front end for a company AI operator.

Goal:

```
hotkey
→ speak rough Japanese
→ on-device speech recognition when available
→ operator-formatted text
→ clipboard / optional auto-paste
→ Gemini
→ Workspace actions
```

Koe is intentionally thin.

It is **not**:
- an LLM
- a project SoT
- a company data store
- a browser-automation bot
- a replacement for Gemini/Dify

The intelligence lives in the approved Company AI stack. Koe removes input friction.

## MVP controls

- **Control + Option + Space**: start/stop recording
- menu-bar icon: start/stop
- copy last transcript
- open Gemini
- toggle Operator / Raw mode
- toggle on-device-only recognition
- optional auto-paste to the active field

## Safe defaults

- on-device-only speech recognition = ON
- auto-paste = OFF
- auto-submit = NOT IMPLEMENTED
- transcript persistence = OFF
- audio persistence = OFF
- no analytics
- no telemetry
- no network request from Koe itself

If the Mac/locale does not support on-device speech recognition, Koe fails closed while on-device-only mode is enabled.

Apple's Speech framework exposes whether on-device recognition is supported and allows a request to require it.

## Build requirement

Koe uses Apple frameworks only:

- AppKit
- SwiftUI
- AVFoundation
- Speech
- Carbon

No Homebrew, Python, Node, Docker, Whisper, or local LLM is required.

A Swift compiler is required to build the app. On a managed company Mac, confirm software/build policy before building or installing.

## Build

```bash
cd company-bootstrap/koe-mac
./build.sh
```

Output:

```
dist/Koe.app
```

Run locally:

```bash
open dist/Koe.app
```

The first launch asks for:
- Microphone
- Speech Recognition

Auto-paste additionally needs Accessibility permission.

## Company usage

Recommended workflow:

1. open Gemini in the browser
2. put cursor in the Gemini input box
3. press Control + Option + Space
4. speak
5. press Control + Option + Space
6. transcript is copied
7. paste manually, or enable auto-paste if company policy allows Accessibility permission
8. press Enter yourself

The final manual Enter is an intentional human gate.

## Operator mode

Raw speech like:

> あのさ今日の会議のやつ見てなんかやること3つぐらい出して明日の予定に入れたい

becomes:

```
[VOICE REQUEST]
以下は音声入力です。言い淀み・誤変換・助詞抜けを補正し、意図を復元してください。
必要なCompany-approved sources/toolsを使って、実行可能な次アクションまで進めてください。
Decision / deadline / owner / policy / risk / delete / permission / external send は勝手に確定せず、必要なら承認を求めてください。

依頼:
あのさ今日の会議のやつ見てなんかやること3つぐらい出して明日の予定に入れたい
```

This is designed to work with:
- Gemini
- Claude
- Dify
- another approved agent

## Local configuration

Koe stores preferences using macOS UserDefaults only.

It does not store transcripts or audio files.

Company-specific vocabulary should be entered locally and must never be committed to this public repo.

## Next stage

After Company policy / API approval:
- approved Dify endpoint adapter
- Gemini/Workspace action feedback
- command history with redacted local metadata only
- push-to-talk mode
- custom vocabulary editor
- optional meeting-note handoff

Do not add an external endpoint until the Company Environment Gate explicitly allows it.
