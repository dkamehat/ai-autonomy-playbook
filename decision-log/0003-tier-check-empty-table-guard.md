# DL-0003: tier_check 空テーブルガード（残存 vacuous PASS 面の封鎖）

- **日付**: 2026-06-14（計画・実装）/ 2026-06-15（Gate-C・公開push・CI確認）
- **統治根拠**: MECHANISM-CHARTER v1.3 §M2（Gate-C: 公開push）/ §M6-2（一致内容・秘密を出さない）
- **レーン分担**:
  - 設計: 対話型AI（Claude Web）── 方式選定・本計画の起草
  - 注釈: 人間（だいき）── 計画の修正・却下・承認（Gate-C）
  - 実行: エージェント型AI（Claude Code）── 実装・ローカル検査
- **関連**: DL-0002（tier_check カナリア）/ SCR-007（緑のまま no-op 化した検査）

**位置づけ**: 本エントリは **DL-0002 §4 の「カナリアの境界」注記が指摘した、カナリアが構造上カバーしない面を
一段上で閉じる follow-up** である。DL-0002 のカナリアは「ソルト整合下で照合が機能する」ことを固定したが、
*本番 `.tier-patterns.sha256` 自体が空/切り詰め/破損* した場合、`run()` が「パターン未設定→スキップ(0)」で
緑になりうる残存 vacuous PASS 面があった。これを構造的に封鎖する。

---

## 1. 計画（設計レーンで作成）

- **目的**: 本番ハッシュ表が空/切り詰め/破損だと検査が緑のままになる残存 no-op 面を閉じる。
- **実装**: `tier_check.py` に「`TIER_SALT` が設定されているのに committed table のエントリ数が
  `--min-entries`（既定1）未満なら FAIL（非ゼロ終了=3）」を追加。エントリ数は非秘密（公開ファイルの行数）。
- **非衝突**: `TIER_SALT` 未設定時は従来どおりスキップ可。`TIER_SALT` 設定時のみ空表を異常扱い。
  既存の終了コード（0=一致なし / 1=一致 / 2=ソルト未設定）は保ち、3=表が下限未満 を追加する。
- **カナリア**: 空（0件）テーブル＋`TIER_SALT` 設定下で FAIL(3) すること、および下限未満（切り詰め）でも
  FAIL(3) することを固定（既存 canary→tier-check の needs ゲートは維持）。

---

## 2. 人間による注釈

> （だいきさんが記入: 計画に対する修正・却下・承認。Gate-C の明示承認をここに）

- **2026-06-15 だいき（Gate-C）**: 2026-06-15 設計レーン経由でCEO承認・Tier-safe確認済
  （grep 0件・件数のみ表示§M6-2）。本変更（空テーブルガード）の公開pushを承認する。

---

## 3. 実行ログ（実行レーンで記録）

- 実行日時: 2026-06-14（実装・ローカル検査）→ 2026-06-15（Gate-C 承認・公開push・CI確認）。
- 変更点:
  - `scripts/tier_check.py`: `run(root, salt, reveal, min_entries=1)` にエントリ数ガードを追加
    （`n_entries < min_entries` で `[tier-check] FAIL: ... エントリ数 N が下限 M 未満` を stderr に出し 3 を返す）。
    `main()` に `--min-entries`（既定1）を argparse で追加。`TIER_SALT` 未設定時の挙動は不変。
  - **意図的な意味論変更**: 「`TIER_SALT` 設定 ＋ 空表」は従来 0（スキップ）だったが 3（FAIL）に変更。
    これは本follow-upの目的そのもの（DL-0002 §3「終了コード意味論は不変」に対する、本DLで承認を取る逸脱）。
    `TIER_SALT` 未設定時の空表スキップ（0）は維持。
  - `scripts/test_tier_check_canary.py`: `test_run_fails_on_empty_table`（空表→3）と
    `test_run_fails_on_truncated_table`（min_entries=999 で下限未満→3）を追加。
- ローカル検査結果:
  - カナリア: **10 tests OK**（`python scripts/test_tier_check_canary.py`、TIER_SALT 不要）。
  - スモーク: ダミーソルト＋本番表（37エントリ）→ **PASS exit 0**（ガード通過・CI緑を維持）。
    `--min-entries 9999` → **FAIL exit 3**（メッセージに「エントリ数 37」＝非秘密の件数のみ）。
    パターン有り×ソルト無し → **ERROR exit 2**（不変）。
  - 公開差分に実Tierパターン平文・実ID・固有名詞が無いことを push 前 grep で再確認（§4で記録）。
- Gate-C: 2026-06-15 設計レーン経由でCEO承認・Tier-safe確認済（§2）。push 前に grep 再確認
  （c4603d98 / NOTION_TOKEN / collection:// / 社名・サービス名 すべて 0 件）。
- コミット（単一・3ファイル同一目的）: `2e87c04a92d34d52679f4ae2cd17ad7bbc99f6d2`
- push: `84cddde..2e87c04  main -> main`（https://github.com/dkamehat/ai-autonomy-playbook）。
- CI（Run 27505263425 / head 2e87c04）: **canary → tier-check の順で success**。本番表（37エントリ）が
  `--min-entries 1` のガードを通過し tier-check 緑を維持（実ソルト下でも回帰なし）。
- 計画からの逸脱: なし。意図的な意味論変更（salt 設定下の空表 0→3）は本DLで承認済（§2）。
  本実行ログ自体は DL-0001/0002 同様、コミットID・CI結果が事後確定のため後続コミットで追記。

---

## 4. 結果と教訓

- 完遂: 公開push・CI緑（**canary → tier-check success**、Run 27505263425）まで到達。本番表のガード通過も確認。
- DL-0002 §4 が「カナリアの境界」として明示した残存面（本番表の空化）を、一段上のガードで構造的に封鎖した。
- **CI が構造保証する範囲（収束の宣言）**:
  - ① 検出可否 — カナリア（DL-0002）が「ソルト整合下で照合が機能する」ことを固定。
  - ② 全空非退化 — 本ガード（`--min-entries` 既定1）が「表のゼロ化・全空」で FAIL(3)。
  - 公開CIで構造保証できるのはこの2点まで。
- **既定 `--min-entries 1` の正確な保証範囲**: 構造保証は「全空・ゼロ化」まで。
  *部分切り詰め*（カウントが floor 以上に残る縮小、例 37→2）は CI では捕捉しない。
- **accepted・documented residual**: 部分切り詰めと内容・ソルト妥当性は、いずれも
  「`.tier-patterns.sha256` が私有ソース（`make_patterns.py` の生成元）の忠実な再生成か」に collapse する。
  私有ソースは公開CIから検証不能ゆえ、原理的に運用保証（ソルト/パターン変更時の表再生成＝DL-0001 §3 逸脱3）の領域。
  これを accepted・documented residual として運用で担保し、**新規CIガードは追加しない（収束規律）**。
- **pinned floor（例 `--min-entries 30`）を採らない理由**: below-floor の縮小しか捕捉できず（弱い）、
  パターン変更のたび手動 bump を要し、floor 値自体が新たな drift 面になる。費用対効果が合わず不採用。
- 教訓: no-op 面は層をなす。1つ塞ぐと「その検出器自身が見ない面」が次の面になる。
  閉じられる面は follow-up で閉じ（DL-0002→本DL）、閉じられない面は accepted residual として運用へ移す
  — この線引きが収束の本体。
- **収束**: 本コミットを以て本硬化スレッド（SCR-007 起点）は収束。以降に別の vacuous 面が出ても
  SCR-007 の蒸し返しではなく新規事象として扱う。SCR-007 は DL-0002 のカナリア＋本DLのガードで二重封鎖。
  クローズ判断は設計レーン（Notion）。
