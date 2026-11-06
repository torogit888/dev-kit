#!/usr/bin/env bash
# 新環境一鍵寫入 Antigravity 全域規則：
#   1. ~/.gemini/GEMINI.md
#   2. ~/.gemini/config/rules/guidance-only.md
#   3. ~/.gemini/antigravity/rules/guidance-only.md
# 用法：bash antigravity/setup_antigravity_rules.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python >/dev/null 2>&1 && python -c "import sys" >/dev/null 2>&1; then
  PY=python
elif command -v python3 >/dev/null 2>&1 && python3 -c "import sys" >/dev/null 2>&1; then
  PY=python3
else
  echo "python not found; cannot install Antigravity rules" >&2
  exit 1
fi

"$PY" "$SCRIPT_DIR/setup_antigravity_rules.py"

