# DL-0002: tier_check カナリア負テスト ＆ Node.js 24 対応

- **日付**: 2026-06-14（計画・実行）/ 2026-06-14（公開push・CI確認）
- **統治根拠**: MECHANISM-CHARTER v1.3 §M2（Gate-C: 公開push）/ §M6-2（一致内容を出さない）
- **レーン分担**:
  - 設計: 対話型AI（Claude Web）── 方式選定・本計画の起草
  - 注釈: 人間（だいき）── 計画の修正・却下・承認（Gate-C）
  - 実行: エージェント型AI（Claude Code）── 実装・ローカル検査
- **関連**: DL-0001 §4（カナリア負テストの予約）/ SCR-007（緑のまま no-op 化した検査の教訓）

DL-0001 §4 で「次タスク」として予約したカナリア負テストを実装し、SCR-007 を恒久対策する。
あわせて Actions の Node.js 20 非推奨警告（DL-0001 §3 の非ブロッキング注記）を解消する。

---

## 1. 計画（設計レーンで作成）

### タスク1: tier_check カナリア負テスト（SCR-007 恒久対策）

- **目的**: tier_check が「緑だが何も検出しない」vacuous PASS に陥ることを構造的に不能化する。
- **方式**: 合成の既知パターン（実Tierパターンではないダミー）＋テスト用ソルトで、実際の検出経路
  （`load_patterns → scan のハッシュ照合 → 終了コード`）を叩き、必ず検出して FAIL(1) することを自動確認。
  検出器が空を返したら（= no-op）カナリアが落ちる。
- **canon-sync の教訓の適用**: コア関数だけでなく *境界（実際の照合経路）* を検証する。
  照合キー生成を `digest()` 関数に集約し、カナリアが本番と同一関数で合成テーブルを組む。
- **§M6-2**: 実Tierパターンの平文を使わず・出さない。合成パターンのみ、照合はハッシュ経路、
  HIT 出力は reveal=False で内容を持たない（ファイル名・位置・長さのみ）。
- **CI**: `canary → tier-check` の順（`needs: canary`）。カナリアが落ちたら本検査を止める。

### タスク2: Node.js 24 対応

- `actions/checkout@v4 → @v5`、`actions/setup-python@v5 → @v6`（いずれも Node24 ランタイム）。
  Node20 非推奨警告を解消し、CI が緑のままであることを確認。

---

## 2. 人間による注釈

> （だいきさんが記入: 計画に対する修正・却下・承認。Gate-C の明示承認をここに）

- **2026-06-13 だいき（Gate-C）**: 2026-06-13 設計レーン経由でCEO承認・Tier-safe確認済。
  本変更（tier_check カナリア＋Node24対応）の公開pushを承認する。

---

## 3. 実行ログ（実行レーンで記録）

- 実行日時: 2026-06-14（実装・ローカル検査 → Gate-C 承認 → 公開push・CI確認）。
- 変更点:
  - `scripts/tier_check.py`: 照合キー生成を `digest(salt, window)` に抽出（scan が使用）。
    `main()` の検査本体を `run(root, salt, reveal)` に分離（終了コード経路をテスト可能化）。
    終了コード意味論は不変（パターン無し=0 / 一致=1 / パターン有り×ソルト無し=2）。
  - `scripts/test_tier_check_canary.py`: 新規カナリア（unittest, 8 件）。scan 経路と run 経路の双方を
    合成パターンで固定。SCR-007 条件（ソルト不一致 → vacuous PASS）の再現テストと、
    分かち書き回避（nospace ストリーム）検出、reveal=False の平文非露出（M6-2）も含む。
  - `.github/workflows/tier-check.yml`: `canary`（TIER_SALT 不要）→ `tier-check`（`needs: canary`）の
    2ジョブ化。actions を Node24 版（checkout@v5 / setup-python@v6）へ更新。
- ローカル検査結果:
  - 新カナリア: **8 tests OK**（`python scripts/test_tier_check_canary.py`、TIER_SALT 不要）。
  - tier_check リファクタのスモーク: ダミーソルトで repo 全体を検査 → **PASS exit 0**（happy path 不変・
    実表はダミーソルトと一致しない）。パターン有り×ソルト無し → **ERROR exit 2**（意味論不変）。
  - 合成パターン文字列はカナリアソース内に平文で存在するが、実ソルト下の実表とは一致しないため
    実CIで誤検知しない（ダミーソルト走査でも 0 件を確認）。
- Gate-C: 2026-06-13 設計レーン経由で CEO 承認・Tier-safe 確認済（§2）。push 前に実ID・実Tier平文・
  固有名詞の不在を grep 再確認（c4603d98 / NOTION_TOKEN / collection:// / 社名・サービス名 すべて 0 件）。
- コミット（規律に従い2分離）:
  - A `90ed0ea957ce01c0df72d18b25c741c8b699c76c` — feat: tier_check カナリア＋Node24（本DL対象の5ファイル）
  - B `7604b5448fd87b2c347591d7b91bc41e3f3d7499` — docs: README 原則メモ（前タスク canon-sync の残）
- push: `eaad633..7604b54  main -> main`（https://github.com/dkamehat/ai-autonomy-playbook）。
- CI（Run 27500630091）: **canary → tier-check の順で success**（canary 13:39:30Z 開始 → tier-check 13:39:37Z 開始、`needs: canary`）。
  Node20 非推奨警告は解消（checkout@v5 / setup-python@v6、ログに deprecation 文字列なし）。
- 計画からの逸脱: なし。本実行ログ自体は DL-0001 と同様、コミットID・CI結果が事後確定のため後続コミットで追記。

---

## 4. 結果と教訓

- 完遂: 公開push・CI緑（**canary → tier-check success**）まで到達。検出器の no-op 緑化を構造的に不能化した。
- DL-0001 §4 の予約（カナリア負テスト）を実装し、SCR-007「緑のCIはソルト一致を保証しない／
  通るCI ≠ 機能するCI」を *構造的に検出可能* にした。
- 教訓: 「コアではなく境界（実際の照合経路）を検証する」を徹底するため、照合キー生成を1関数に集約し、
  カナリアが本番と同一経路を叩く形にした（canon-sync で得た知見の還流）。
- **カナリアの境界（二次的 vacuous 確信の回避）**: 本カナリアが保証するのは「ソルト整合下で照合が機能する」
  ことであり、*本番表と本番 Secret ソルトの不一致そのもの* は（実ソルトをカナリアに渡さない設計上）検出できない。
  その整合は「表を Secret と同一ソルトで再生成する」運用（DL-0001 §3 逸脱3）で別途担保する。
  「カナリアがある＝ドリフト安全」と読み替えないことを明記する。
- マージ後、設計レーンが Notion 側で **SCR-007 を Charter Updated にクローズ**する。
