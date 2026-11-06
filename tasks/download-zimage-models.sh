#!/usr/bin/env bash
# 下載 Z-Image Turbo 官方模型檔案至 ComfyUI 容器
python3 "$(dirname "$0")/../../AIVideo/scripts/download_zimage_models.py" || python "$(dirname "$0")/../../AIVideo/scripts/download_zimage_models.py"
