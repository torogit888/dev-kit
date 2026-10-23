#!/usr/bin/env bash
# 新環境一鍵寫入 Copilot 全域規則：
#   1. VS Code User prompts/guidance-only.instructions.md
#   2. ~/.copilot/copilot-instructions.md
# 用法：bash copilot/setup_copilot_rules.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python >/dev/null 2>&1 && python -c "import sys" >/dev/null 2>&1; then
  PY=python
elif command -v python3 >/dev/null 2>&1 && python3 -c "import sys" >/dev/null 2>&1; then
  PY=python3
else
  echo "python not found; cannot install Copilot rules" >&2
  exit 1
fi

"$PY" "$SCRIPT_DIR/setup_copilot_rules.py"
