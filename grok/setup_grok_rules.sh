#!/usr/bin/env bash
# 新環境一鍵寫入 Grok 全域規則：~/.grok/rules/guidance-only.md
# 用法：bash grok/setup_grok_rules.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="${SCRIPT_DIR}/rules/guidance-only.md"

GROK_HOME="${GROK_HOME:-${HOME}/.grok}"
RULES_DIR="${GROK_HOME}/rules"
TARGET="${RULES_DIR}/guidance-only.md"

if [[ ! -f "$SRC" ]]; then
  echo "missing source rule: $SRC" >&2
  exit 1
fi

mkdir -p "$RULES_DIR"
cp "$SRC" "$TARGET"

echo "wrote $TARGET"
ls -la "$TARGET"
