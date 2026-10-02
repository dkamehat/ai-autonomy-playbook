#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DIST="$ROOT/dist"
APP="$DIST/Koe.app"
MACOS="$APP/Contents/MacOS"
RES="$APP/Contents/Resources"

if ! command -v swiftc >/dev/null 2>&1; then
  echo "ERROR: swiftc is not available."
  echo "On a managed company Mac, do not install developer tools without company approval."
  exit 2
fi

rm -rf "$APP"
mkdir -p "$MACOS" "$RES"

swiftc   "$ROOT/Sources/main.swift"   -o "$MACOS/Koe"   -framework AppKit   -framework AVFoundation   -framework Speech   -framework Carbon   -framework ApplicationServices

cp "$ROOT/Info.plist" "$APP/Contents/Info.plist"

echo "Built: $APP"
echo "Run: open '$APP'"
