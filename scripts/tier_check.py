#!/usr/bin/env python3
"""Tierパターン検査（ハッシュ照合方式）。

機密パターンの平文をリポジトリに置かずに、混入を機械的に検査するスキャナ。

設計:
- パターンは HMAC-SHA256(salt, 正規化済み文字列) として .tier-patterns.sha256 に保存
- ソルトはリポジトリに置かない（ローカル: 環境変数 TIER_SALT / CI: Actions Secret）
- 検査はスライディングウィンドウの完全一致。NFKC正規化＋小文字化した本文と、
  さらに空白を除去したストリームの2系統を照合（分かち書き・スペース挿入による回避を防ぐ）
- 出力は既定で秘匿（ファイル名・位置・長さのみ）。CIログは公開されるため、
  一致した内容そのものは表示しない。ローカル確認時のみ TIER_CHECK_REVEAL=1 で内容表示

注意: 小規模リポジトリ向けの素朴な実装です。パターンは4文字以上を推奨。
"""
from __future__ import annotations

import hashlib
import hmac
import os
import sys
import unicodedata
from pathlib import Path

PATTERN_FILE = ".tier-patterns.sha256"
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
SKIP_FILES = {PATTERN_FILE, "tier-patterns.private.txt"}
MAX_BYTES = 2_000_000


def norm(s: str) -> str:
    return unicodedata.normalize("NFKC", s).lower()


def digest(salt: str, window: str) -> str:
    """HMAC-SHA256(salt, window) の16進。make_patterns.py のハッシュ経路と同一。

    検出の「照合キー生成」をこの1か所に閉じ込める。カナリア（test_tier_check_canary.py）が
    同じ関数で合成テーブルを作り、scan の照合が無言で no-op 化していないことを固定する。
    """
    return hmac.new(salt.encode(), window.encode(), hashlib.sha256).hexdigest()


def load_patterns(root: Path) -> dict[int, set[str]]:
    """`長さ:HMAC16進` 形式のパターン表を読み込む。"""
    table: dict[int, set[str]] = {}
    p = root / PATTERN_FILE
    if not p.exists():
        return table
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            ln_s, hx = line.split(":", 1)
            table.setdefault(int(ln_s), set()).add(hx.strip().lower())
        except ValueError:
            print(f"[tier-check] WARN: 不正な行を無視しました: {line[:24]}...", file=sys.stderr)
    return table


def iter_text_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        try:
            if path.stat().st_size > MAX_BYTES:
                continue
            yield path, path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue


def scan(text: str, table: dict[int, set[str]], salt: str, reveal: bool):
    hits = []
    cache: dict[tuple[int, str], bool] = {}
    base = norm(text)
    streams = [("raw", base), ("nospace", "".join(base.split()))]
    for label, stream in streams:
        n = len(stream)
        for length, hashes in table.items():
            if length < 1 or length > n:
                continue
            for i in range(n - length + 1):
                window = stream[i : i + length]
                matched = cache.get((length, window))
                if matched is None:
                    matched = digest(salt, window) in hashes
                    cache[(length, window)] = matched
                if matched:
                    hits.append((label, i, length, window if reveal else None))
    return hits


def run(root: Path, salt: str, reveal: bool) -> int:
    """root 配下を salt で検査する実際の検出経路（load_patterns→scan→終了コード）。

    パターン未設定は 0（スキップ）、一致ありは 1、一致なしは 0。
    カナリアはこの関数を合成パターンで叩き、一致時に必ず 1 を返すことを固定する。
    """
    table = load_patterns(root)
    if not table:
        print("[tier-check] パターン未設定（.tier-patterns.sha256 にエントリなし）。スキップします。")
        return 0
    total = 0
    for path, text in iter_text_files(root):
        for label, pos, length, content in scan(text, table, salt, reveal):
            total += 1
            shown = f" 内容: {content}" if reveal else ""
            print(f"[HIT] {path.relative_to(root)} stream={label} pos={pos} len={length}{shown}")
    if total:
        print(f"[tier-check] FAIL: {total} 件のTierパターン一致。公開前に除去してください。", file=sys.stderr)
        return 1
    print("[tier-check] PASS: 一致なし。")
    return 0


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    salt = os.environ.get("TIER_SALT", "")
    if not salt:
        # パターンが無ければソルト未設定でもスキップ（従来挙動を維持）
        if not load_patterns(root):
            print("[tier-check] パターン未設定（.tier-patterns.sha256 にエントリなし）。スキップします。")
            return 0
        print(
            "[tier-check] ERROR: TIER_SALT が未設定です。"
            "ローカルは環境変数、CIは Actions Secret で設定してください。",
            file=sys.stderr,
        )
        return 2
    reveal = os.environ.get("TIER_CHECK_REVEAL") == "1"
    return run(root, salt, reveal)


if __name__ == "__main__":
    sys.exit(main())
