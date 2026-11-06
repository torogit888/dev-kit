#!/usr/bin/env bash
# 測試 ComfyUI Z-Image Turbo 16:9 本地生圖
set -euo pipefail

echo "========================================="
echo " 測試 ComfyUI (Z-Image Turbo) 16:9 生圖"
echo "========================================="

# 1. 判斷執行環境
if [ -d "/workspace" ]; then
  # 容器內執行
  python3 -m aivideo check --comfy-image
  exit 0
fi

# 2. 主機端執行：優先使用 docker compose pipeline 容器
if command -v docker >/dev/null 2>&1; then
  echo "正在透過 Docker Compose 執行測試生圖..."
  docker compose run --rm pipeline python -m aivideo check --comfy-image
  if command -v code >/dev/null 2>&1 && [ -f "jobs/_smoke/comfyui_z_image_turbo_16x9.png" ]; then
    code -r "jobs/_smoke/comfyui_z_image_turbo_16x9.png"
  fi
  exit 0
fi

# 3. 本機直接執行（若本機有安裝環境）
if command -v python3 >/dev/null 2>&1; then
  python3 -m aivideo check --comfy-image
elif command -v python >/dev/null 2>&1; then
  python -m aivideo check --comfy-image
else
  echo "[錯誤] 找不到 docker 或 python 環境！"
  exit 1
fi

if command -v code >/dev/null 2>&1 && [ -f "jobs/_smoke/comfyui_z_image_turbo_16x9.png" ]; then
  code -r "jobs/_smoke/comfyui_z_image_turbo_16x9.png"
fi

