---
name: "Guidance Only & Confirm Before Major Changes"
description: "Always-on workflow rule: explain in Traditional Chinese before acting, present options and wait for user confirmation before major changes or heavy operations (build/test/Docker)."
applyTo: "**"
---

# Guidance Only & 重大變更前確認規範

## 1. 先解釋說明再開始做
- 在呼叫工具進行實質程式碼修改、檔案建立、刪除或執行終端指令之前，必須先以**繁體中文**向使用者簡明扼要地解釋問題成因、解法思路與預計執行的具體步驟，讓使用者清楚掌握操作脈絡。

## 2. 做大變動之前必須提供選項讓我選（Confirm Before Major Changes）
在執行以下任何**重大變更（Major Changes）**之前，**切勿直接動手修改**，必須先停下來提供具體方案選項讓使用者選擇並確認：
- **跨多檔案修改或架構調整**：涉及多個元件/模組連動、資料流變更、API 介面或設定結構調整。
- **存在多種實作方向或取捨**：當需求有不同解法（例如：最小改動 vs. 完整重構、不同 UI/UX 呈現方式、不同預設行為）時。
- **新增、刪除或大幅覆寫檔案**：建立新模組、刪除既有功能或大範圍改寫既有邏輯。

**詢問方式**：
- 若環境中有 `ask_user`（或 `askQuestions`）互動工具，**優先呼叫該工具**提供清楚的選項（包含推薦預設值與各選項優缺點說明），讓使用者直接勾選確認。
- 若無表單工具，請在回覆中列出清楚的編號選項（例如：選項 1 / 選項 2 / 選項 3），並等待使用者回覆確認後再執行。

## 3. Guidance Only — 預設不自動執行重型操作（Do Not Run Heavy Ops）
- **傾向說明做法而非直接代跑耗時指令**：提供清楚、可直接複製貼上的指令與步驟。
- 除非使用者在當下明確要求執行，否則**禁止自動執行**以下重型操作：
  - **編譯 / 建置 (Compile / Build)**：不要自動執行 build 腳本、打包、映像檔建置或安裝龐大依賴套件。
  - **Docker 操作**：不要自動啟動/停止容器、`docker compose`、`runDocker.sh` 或建置 image。
  - **測試 (Tests)**：不要自動執行單元測試、UAT、`pytest` 或完整測試套件。
- 當需要執行上述耗時步驟（如啟動服務、跑完整測試、打包建置、大型下載）時，**先提供精確指令並詢問使用者選擇**（由使用者自行執行 ／ 請 AI 代為執行 ／ 略過），等待確認後再動作。

## 4. 允許直接執行的輕量操作（Allowed Without Asking）
- 唯讀檢視、搜尋與解釋程式碼。
- 使用者已明確指定且範圍單純、可逆的局部微調（仍須先以繁體中文簡要說明）。
- 快速、非破壞性的狀態查詢指令（如查看檔案清單、`git status`）。

## 5. 專案文件衝突處理（Conflict Note）
- 若專案內的 `AGENTS.md` 或 `README.md` 記載了如何使用 Docker 建置或測試，請將其視為**提供給使用者的參考文件**，而非授權 AI 自動執行這些耗時指令。
