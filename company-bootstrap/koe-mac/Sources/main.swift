import AppKit
import AVFoundation
import Speech
import Carbon
import ApplicationServices

final class KoeApp: NSObject, NSApplicationDelegate {
    private let statusItem = NSStatusBar.system.statusItem(withLength: NSStatusItem.squareLength)
    private let audioEngine = AVAudioEngine()
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private var recognizer = SFSpeechRecognizer(locale: Locale(identifier: "ja-JP"))
    private var hotKeyRef: EventHotKeyRef?
    private var currentTranscript = ""
    private var isRecording = false

    private let defaults = UserDefaults.standard
    private var operatorMode: Bool {
        get { defaults.object(forKey: "operatorMode") == nil ? true : defaults.bool(forKey: "operatorMode") }
        set { defaults.set(newValue, forKey: "operatorMode") }
    }
    private var onDeviceOnly: Bool {
        get { defaults.object(forKey: "onDeviceOnly") == nil ? true : defaults.bool(forKey: "onDeviceOnly") }
        set { defaults.set(newValue, forKey: "onDeviceOnly") }
    }
    private var autoPaste: Bool {
        get { defaults.bool(forKey: "autoPaste") }
        set { defaults.set(newValue, forKey: "autoPaste") }
    }

    func applicationDidFinishLaunching(_ notification: Notification) {
        configureStatusItem()
        registerGlobalHotKey()
        requestPermissions()
    }

    func applicationWillTerminate(_ notification: Notification) {
        stopRecording(deliver: false)
        if let hotKeyRef {
            UnregisterEventHotKey(hotKeyRef)
        }
    }

    private func configureStatusItem() {
        statusItem.button?.title = "声"
        statusItem.button?.toolTip = "Koe — Voice Command Bar"

        let menu = NSMenu()

        let toggle = NSMenuItem(
            title: "Start / Stop Recording  ⌃⌥Space",
            action: #selector(toggleRecording),
            keyEquivalent: ""
        )
        toggle.target = self
        menu.addItem(toggle)

        let copy = NSMenuItem(
            title: "Copy Last Transcript",
            action: #selector(copyLastTranscript),
            keyEquivalent: ""
        )
        copy.target = self
        menu.addItem(copy)

        let openGemini = NSMenuItem(
            title: "Open Gemini",
            action: #selector(openGemini),
            keyEquivalent: ""
        )
        openGemini.target = self
        menu.addItem(openGemini)

        menu.addItem(.separator())

        let operatorItem = NSMenuItem(
            title: "Operator Mode",
            action: #selector(toggleOperatorMode(_:)),
            keyEquivalent: ""
        )
        operatorItem.target = self
        operatorItem.state = operatorMode ? .on : .off
        menu.addItem(operatorItem)

        let onDeviceItem = NSMenuItem(
            title: "On-device Recognition Only",
            action: #selector(toggleOnDeviceOnly(_:)),
            keyEquivalent: ""
        )
        onDeviceItem.target = self
        onDeviceItem.state = onDeviceOnly ? .on : .off
        menu.addItem(onDeviceItem)

        let autoPasteItem = NSMenuItem(
            title: "Auto-paste After Recording",
            action: #selector(toggleAutoPaste(_:)),
            keyEquivalent: ""
        )
        autoPasteItem.target = self
        autoPasteItem.state = autoPaste ? .on : .off
        menu.addItem(autoPasteItem)

        menu.addItem(.separator())

        let quit = NSMenuItem(
            title: "Quit Koe",
            action: #selector(NSApplication.terminate(_:)),
            keyEquivalent: "q"
        )
        menu.addItem(quit)

        statusItem.menu = menu
        refreshStatus()
    }

    private func refreshStatus() {
        DispatchQueue.main.async {
            self.statusItem.button?.title = self.isRecording ? "●" : "声"
            self.statusItem.button?.toolTip = self.isRecording
                ? "Koe is listening — ⌃⌥Space to stop"
                : "Koe — ⌃⌥Space to speak"
        }
    }

    private func requestPermissions() {
        SFSpeechRecognizer.requestAuthorization { status in
            if status != .authorized {
                self.showMessage(
                    title: "Speech Recognition permission required",
                    message: "Enable Speech Recognition for Koe in System Settings."
                )
            }
        }

        AVCaptureDevice.requestAccess(for: .audio) { granted in
            if !granted {
                self.showMessage(
                    title: "Microphone permission required",
                    message: "Enable Microphone access for Koe in System Settings."
                )
            }
        }
    }

    private func registerGlobalHotKey() {
        var eventType = EventTypeSpec(
            eventClass: OSType(kEventClassKeyboard),
            eventKind: UInt32(kEventHotKeyPressed)
        )

        InstallEventHandler(
            GetApplicationEventTarget(),
            { _, event, userData in
                guard let event, let userData else { return noErr }
                var hotKeyID = EventHotKeyID()
                let status = GetEventParameter(
                    event,
                    EventParamName(kEventParamDirectObject),
                    EventParamType(typeEventHotKeyID),
                    nil,
                    MemoryLayout<EventHotKeyID>.size,
                    nil,
                    &hotKeyID
                )

                if status == noErr && hotKeyID.id == 1 {
                    let app = Unmanaged<KoeApp>.fromOpaque(userData).takeUnretainedValue()
                    DispatchQueue.main.async {
                        app.toggleRecording()
                    }
                }
                return noErr
            },
            1,
            &eventType,
            Unmanaged.passUnretained(self).toOpaque(),
            nil
        )

        let hotKeyID = EventHotKeyID(
            signature: OSType(0x4B4F4521), // KOE!
            id: 1
        )

        let modifiers = UInt32(controlKey | optionKey)
        let keyCode = UInt32(kVK_Space)

        RegisterEventHotKey(
            keyCode,
            modifiers,
            hotKeyID,
            GetApplicationEventTarget(),
            0,
            &hotKeyRef
        )
    }

    @objc private func toggleRecording() {
        if isRecording {
            stopRecording(deliver: true)
        } else {
            startRecording()
        }
    }

    private func startRecording() {
        guard !isRecording else { return }

        guard SFSpeechRecognizer.authorizationStatus() == .authorized else {
            showMessage(
                title: "Speech permission missing",
                message: "Koe cannot start until Speech Recognition is authorized."
            )
            return
        }

        guard let recognizer else {
            showMessage(
                title: "Japanese speech recognition unavailable",
                message: "Could not initialize ja-JP speech recognition."
            )
            return
        }

        if onDeviceOnly && !recognizer.supportsOnDeviceRecognition {
            showMessage(
                title: "On-device recognition unavailable",
                message: "This Mac/locale does not report on-device recognition support. Koe will not fall back to network recognition while On-device Only is enabled."
            )
            return
        }

        recognitionTask?.cancel()
        recognitionTask = nil
        currentTranscript = ""

        let request = SFSpeechAudioBufferRecognitionRequest()
        request.shouldReportPartialResults = true
        request.taskHint = .dictation
        request.requiresOnDeviceRecognition = onDeviceOnly

        // Keep this public repo generic. Company-specific terms should be added
        // only in local builds/configuration, never committed here.
        request.contextualStrings = [
            "PMO", "KPI", "API", "MCP", "Gemini", "Dify", "Claude",
            "Decision", "Task", "Risk", "Blocker", "Workstream"
        ]

        recognitionRequest = request

        let inputNode = audioEngine.inputNode
        let format = inputNode.outputFormat(forBus: 0)

        inputNode.removeTap(onBus: 0)
        inputNode.installTap(
            onBus: 0,
            bufferSize: 1024,
            format: format
        ) { [weak self] buffer, _ in
            self?.recognitionRequest?.append(buffer)
        }

        recognitionTask = recognizer.recognitionTask(with: request) { [weak self] result, error in
            guard let self else { return }

            if let result {
                self.currentTranscript = result.bestTranscription.formattedString
            }

            if error != nil {
                DispatchQueue.main.async {
                    if self.isRecording {
                        self.stopRecording(deliver: false)
                        self.showMessage(
                            title: "Speech recognition stopped",
                            message: "Recognition ended unexpectedly. Try again."
                        )
                    }
                }
            }
        }

        do {
            audioEngine.prepare()
            try audioEngine.start()
            isRecording = true
            NSSound.beep()
            refreshStatus()
        } catch {
            recognitionRequest = nil
            recognitionTask = nil
            showMessage(
                title: "Microphone start failed",
                message: error.localizedDescription
            )
        }
    }

    private func stopRecording(deliver: Bool) {
        guard isRecording else { return }

        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        recognitionRequest?.endAudio()
        recognitionTask?.cancel()
        recognitionTask = nil
        recognitionRequest = nil
        isRecording = false
        NSSound.beep()
        refreshStatus()

        let transcript = currentTranscript.trimmingCharacters(in: .whitespacesAndNewlines)
        guard deliver, !transcript.isEmpty else { return }

        let output = operatorMode ? operatorPrompt(for: transcript) : transcript
        copyToPasteboard(output)

        if autoPaste {
            pasteIntoFrontmostApp()
        }
    }

    private func operatorPrompt(for transcript: String) -> String {
        return """
        [VOICE REQUEST / COMPANY OPERATOR]
        以下は音声入力です。言い淀み・誤変換・助詞抜け・途中の言い直しがあっても、文脈から依頼の目的を復元してください。

        あなたは相談相手ではなく、Company-approved toolsを使って仕事を前へ進めるOperatorです。

        実行順:
        1. 依頼の最終目的を推定
        2. 必要ならCalendar / Gmail / Drive / Docs / Tasks / Chat / approved company sourcesを取得
        3. 作業を小さな実行単位へ分解
        4. 今の権限で安全に実行できるREAD / DRAFT / low-risk WRITEは進める
        5. 実行できなかった操作は、何が足りないかを明示する
        6. 最後にDone / Need approval / Blocked / Nextを短く返す

        原則:
        - 不足情報が実行を妨げない限り、細かい確認質問から始めない
        - 「方法を説明する」だけで終わらず、可能な操作は実行する
        - 同じ情報を何度も聞かない
        - 利用可能なCompany sourceを優先し、推測よりEvidenceを使う
        - Decision / deadline / owner / policy / risk / delete / permission / external send / invite は勝手に確定せず承認を求める
        - 会社情報をPublic GitHubや未承認サービスへ送らない

        依頼:
        \(transcript)
        """
    }

    private func copyToPasteboard(_ text: String) {
        let pb = NSPasteboard.general
        pb.clearContents()
        pb.setString(text, forType: .string)
    }

    private func pasteIntoFrontmostApp() {
        let options = [kAXTrustedCheckOptionPrompt.takeUnretainedValue() as String: true] as CFDictionary
        guard AXIsProcessTrustedWithOptions(options) else {
            showMessage(
                title: "Accessibility permission required",
                message: "Auto-paste needs Accessibility permission. The transcript is already in the clipboard."
            )
            return
        }

        guard
            let source = CGEventSource(stateID: .hidSystemState),
            let keyDown = CGEvent(
                keyboardEventSource: source,
                virtualKey: 0x09, // V
                keyDown: true
            ),
            let keyUp = CGEvent(
                keyboardEventSource: source,
                virtualKey: 0x09,
                keyDown: false
            )
        else { return }

        keyDown.flags = .maskCommand
        keyUp.flags = .maskCommand
        keyDown.post(tap: .cghidEventTap)
        keyUp.post(tap: .cghidEventTap)
    }

    @objc private func copyLastTranscript() {
        let transcript = currentTranscript.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !transcript.isEmpty else {
            showMessage(title: "No transcript", message: "Record something first.")
            return
        }
        copyToPasteboard(operatorMode ? operatorPrompt(for: transcript) : transcript)
    }

    @objc private func openGemini() {
        guard let url = URL(string: "https://gemini.google.com/app") else { return }
        NSWorkspace.shared.open(url)
    }

    @objc private func toggleOperatorMode(_ sender: NSMenuItem) {
        operatorMode.toggle()
        sender.state = operatorMode ? .on : .off
    }

    @objc private func toggleOnDeviceOnly(_ sender: NSMenuItem) {
        onDeviceOnly.toggle()
        sender.state = onDeviceOnly ? .on : .off
    }

    @objc private func toggleAutoPaste(_ sender: NSMenuItem) {
        autoPaste.toggle()
        sender.state = autoPaste ? .on : .off
    }

    private func showMessage(title: String, message: String) {
        DispatchQueue.main.async {
            let alert = NSAlert()
            alert.messageText = title
            alert.informativeText = message
            alert.alertStyle = .informational
            alert.runModal()
        }
    }
}

let app = NSApplication.shared
let delegate = KoeApp()
app.delegate = delegate
app.setActivationPolicy(.accessory)
app.run()
