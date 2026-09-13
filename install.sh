#!/usr/bin/env bash
# 一次套用本倉庫目前所有 user task。
# 用法：bash install.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$ROOT/grok/setup_grok_rules.sh"

if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "python not found; skip VS Code Dev Container defaults" >&2
  exit 1
fi

"$PY" "$ROOT/vscode/merge_user_settings.py"
