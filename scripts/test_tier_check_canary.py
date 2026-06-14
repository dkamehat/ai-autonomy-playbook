#!/usr/bin/env python3
"""カナリア（負テスト）— tier_check の vacuous PASS（緑だが no-op）を構造的に不能化する。

背景: SCR-007 / DL-0001 §4。CI Secret のソルトと公開ハッシュ表のソルトが乖離すると、
ハッシュが永遠に一致せず検査が「緑のまま何も検出しない」状態になりうる（緑≠機能）。

方針（canon-sync で得た教訓の適用）: コア関数だけでなく *実際の検出経路*
（load_patterns → scan のハッシュ照合 → 終了コード）を、合成パターンで叩いて固定する。
検出器が一致を取りこぼしたら（= no-op）このカナリアが落ちる。

§M6-2 厳守:
- 実Tierパターンの平文は一切使わない。明らかに合成のダミー文字列のみ。
- 照合は make_patterns.py / tier_check.py と同一のハッシュ経路（digest 関数）で行う。
- reveal=False のとき HIT 出力にパターン平文が出ないことも検証する（CIログ＝ファイル名・位置・長さのみ）。

ネットワーク不要・TIER_SALT 不要（カナリア専用のテスト用ソルトを使う）。
実行: python scripts/test_tier_check_canary.py
"""
from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from tier_check import digest, norm, run, scan  # noqa: E402

# 合成パターン（実Tierパターンではない。明示的にダミーと分かる文字列）。
TEST_SALT = "canary-test-salt-not-production"
WRONG_SALT = "a-different-salt-models-scr007-drift"
SYNTH = "qqqcanarysynthetictokenqqq"  # NFKC+lower 後も不変・len>=4


def _table_for(salt: str, pattern: str) -> dict[int, set[str]]:
    """合成パターンのハッシュ表を、本番と同一の経路（digest）で組む。"""
    table: dict[int, set[str]] = {}
    base = norm(pattern)
    for variant in {base, "".join(base.split())}:
        table.setdefault(len(variant), set()).add(digest(salt, variant))
    return table


def _write_pattern_file(root: Path, salt: str, pattern: str) -> None:
    base = norm(pattern)
    lines = ["# canary synthetic table（合成・実パターンではない）"]
    for variant in sorted({base, "".join(base.split())}):
        lines.append(f"{len(variant)}:{digest(salt, variant)}")
    (root / ".tier-patterns.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


class TestScanHashPath(unittest.TestCase):
    """scan のハッシュ照合（実際の検出経路の中核）を合成パターンで固定する。"""

    def test_scan_is_not_silent(self):
        table = _table_for(TEST_SALT, SYNTH)
        hits = scan(f"前文 {SYNTH} 後文", table, TEST_SALT, reveal=False)
        # ── no-op 検出の本体。空＝照合が機能していない。
        self.assertTrue(hits, "no-op: 合成パターンに対し scan が何も検出しなかった（照合が壊れている）。")

    def test_absent_pattern_yields_no_hit(self):
        table = _table_for(TEST_SALT, SYNTH)
        self.assertEqual(scan("ここには無い無害なテキスト", table, TEST_SALT, reveal=False), [])

    def test_salt_mismatch_is_vacuous_pass(self):
        # SCR-007 の条件再現: 表と検査のソルトが食い違うと永遠に一致しない（= vacuous PASS）。
        table = _table_for(TEST_SALT, SYNTH)
        self.assertEqual(
            scan(f"x {SYNTH} y", table, WRONG_SALT, reveal=False), [],
            "ソルト不一致でも一致してしまう（テーブルとソルトの結合が壊れている）。",
        )

    def test_spaced_evasion_detected(self):
        # 分かち書き回避（空白挿入）も nospace ストリームで捕捉されること。
        table = _table_for(TEST_SALT, SYNTH)
        spaced = " ".join(SYNTH)  # "q q q c a n ..."
        hits = scan(spaced, table, TEST_SALT, reveal=False)
        self.assertTrue(any(label == "nospace" for label, *_ in hits), "空白挿入回避を検出できていない")

    def test_reveal_false_hides_plaintext(self):
        # §M6-2: reveal=False では内容を持たない（CIログに平文を出さない）。
        table = _table_for(TEST_SALT, SYNTH)
        hits = scan(f"{SYNTH}", table, TEST_SALT, reveal=False)
        self.assertTrue(hits, "前提崩れ: 合成パターンが検出されていない（空ループの空振り合格を防ぐ）")
        for _label, _pos, _len, content in hits:
            self.assertIsNone(content, "reveal=False なのに一致内容が露出している（M6-2 違反）")


class TestRunEndToEnd(unittest.TestCase):
    """実際の終了コード経路（run = load_patterns→iter_text_files→scan→exit）を固定する。"""

    def test_run_fails_on_known_synthetic(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_pattern_file(root, TEST_SALT, SYNTH)
            (root / "decoy.txt").write_text(f"無害な前文 {SYNTH} 無害な後文\n", encoding="utf-8")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = run(root, TEST_SALT, reveal=False)
            self.assertEqual(code, 1, "no-op: 既知の合成パターンを含むのに run が FAIL(1) を返さなかった。")
            out = buf.getvalue()
            self.assertIn("[HIT]", out)
            self.assertNotIn(SYNTH, out, "§M6-2: HIT 出力にパターン平文が漏れている（位置・長さのみにすべき）")

    def test_run_passes_when_clean(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_pattern_file(root, TEST_SALT, SYNTH)
            (root / "clean.txt").write_text("ここには合成パターンは無い。\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(run(root, TEST_SALT, reveal=False), 0)

    def test_run_vacuous_pass_on_salt_mismatch(self):
        # 表は TEST_SALT で生成、検査は WRONG_SALT → 一致せず PASS（SCR-007 の vacuous PASS）。
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            _write_pattern_file(root, TEST_SALT, SYNTH)
            (root / "decoy.txt").write_text(f"{SYNTH}\n", encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(
                    run(root, WRONG_SALT, reveal=False), 0,
                    "ソルト不一致でも検出されている（このテストの前提が崩れている）",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
