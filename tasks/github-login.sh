#!/usr/bin/env bash
# 主機新環境一次性任務：登入 GitHub CLI 並配置 Git 憑證
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "未安裝 GitHub CLI (gh)。"
  echo "請先安裝 gh："
  echo "  - Windows (PowerShell): winget install --id GitHub.cli"
  echo "  - macOS: brew install gh"
  echo "  - Linux (Debian/Ubuntu): sudo apt install gh"
  exit 1
fi

echo "檢查 GitHub 認證狀態..."
if gh auth status >/dev/null 2>&1; then
  echo "GitHub 已經登入成功。"
else
  echo "尚未登入 GitHub，啟動互動式登入..."
  gh auth login
fi

echo "配置 Git 憑證助手 (gh auth setup-git)..."
gh auth setup-git
echo "GitHub 登入與憑證配置完成。"
