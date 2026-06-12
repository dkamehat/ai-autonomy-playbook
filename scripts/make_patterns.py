#!/usr/bin/env python3
"""tier-patterns.private.txt（平文・git管理外）から .tier-patterns.sha256 を生成する。

使い方:
  1. tier-patterns.private.txt を作成（1行1パターン、# でコメント）。絶対にコミットしない（.gitignore済み）
  2. export TIER_SALT=$(openssl rand -hex 32)   # 初回のみ。生成した値はパスワードマネージャに保管
  3. python3 scripts/make_patterns.py
  4. gh secret set TIER_SALT --body "$TIER_SALT"   # CI用に同じソルトをSecretへ

出力形式: `長さ:HMAC-SHA256(salt, NFKC正規化＋小文字化した文字列)`
空白を含むパターンは、空白除去版も自動登録される（回避策対策）。
"""
from __future__ import annotations

import hashlib
import hmac
import os
import sys
import unicodedata
from pathlib import Path

SRC = "tier-patterns.private.txt"
DST = ".tier-patterns.sha256"


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    salt = os.environ.get("TIER_SALT", "")
    if not salt:
        print(
            "ERROR: TIER_SALT が未設定です。例: export TIER_SALT=$(openssl rand -hex 32)",
            file=sys.stderr,
        )
        return 2
    src = root / SRC
    if not src.exists():
        print(f"ERROR: {SRC} が見つかりません。1行1パターンで作成してください（コミット禁止）。", file=sys.stderr)
        return 2

    entries: set[str] = set()
    n_terms = 0
    for raw in src.read_text(encoding="utf-8").splitlines():
        term = raw.strip()
        if not term or term.startswith("#"):
            continue
        n_terms += 1
        base = unicodedata.normalize("NFKC", term).lower()
        for variant in {base, "".join(base.split())}:
            if len(variant) < 4:
                # パターン内容は表示しない（このスクリプトの出力も画面共有等で漏れうるため）
                print(f"WARN: 4文字未満のパターンは誤検知しやすいため非推奨です (len={len(variant)})", file=sys.stderr)
            digest = hmac.new(salt.encode(), variant.encode(), hashlib.sha256).hexdigest()
            entries.add(f"{len(variant)}:{digest}")

    header = [
        "# tier-patterns（HMAC-SHA256ハッシュ表）。平文パターンはここに置かない。",
        "# 生成: python3 scripts/make_patterns.py（要 TIER_SALT 環境変数）",
        "# 形式: 長さ:HMAC16進",
        "",
    ]
    (root / DST).write_text("\n".join(header + sorted(entries)) + "\n", encoding="utf-8")
    print(f"OK: {n_terms} 件のパターンから {len(entries)} エントリを {DST} に書き出しました。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
