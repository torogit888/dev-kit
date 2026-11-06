#!/usr/bin/env bash
# 安裝或更新官方 Google Antigravity Python SDK (google-antigravity)
set -euo pipefail

echo "檢查並安裝官方 google-antigravity SDK..."

# 1. 若已在容器內（例如 /workspace 存在），直接安裝於當前 Python 環境
if [ -d "/workspace" ]; then
  python3 -m pip install --upgrade google-antigravity
  python3 -c "import google.antigravity as ag; print('容器內 google-antigravity 安裝成功')"
  exit 0
fi

# 2. 若在主機端且 aivideo-pipeline 容器正在執行，直接裝進容器內
if command -v docker >/dev/null 2>&1; then
  CONTAINER_ID="$(docker ps --filter "name=aivideo-pipeline" --format "{{.ID}}" | head -n 1 || true)"
  if [ -n "$CONTAINER_ID" ]; then
    echo "偵測到執行中的 aivideo-pipeline 容器 ($CONTAINER_ID)，正在容器內安裝 google-antigravity..."
    docker exec "$CONTAINER_ID" python3 -m pip install --upgrade google-antigravity
    docker exec "$CONTAINER_ID" python3 -c "import google.antigravity as ag; print('aivideo-pipeline 容器內 google-antigravity 安裝完成！')"
  fi
fi

# 3. 若主機端有 Python 3.10+ 環境，也一併嘗試安裝於主機
if command -v python3 >/dev/null 2>&1 && python3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >/dev/null 2>&1; then
  echo "正在主機 Python 3.10+ 環境安裝 google-antigravity..."
  python3 -m pip install --upgrade google-antigravity
elif command -v python >/dev/null 2>&1 && python -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >/dev/null 2>&1; then
  echo "正在主機 Python 3.10+ 環境安裝 google-antigravity..."
  python -m pip install --upgrade google-antigravity
else
  echo "主機端無 Python 3.10+（略過主機端安裝，已於容器中完成安裝）。"
fi

echo "google-antigravity SDK 安裝任務完成。"

