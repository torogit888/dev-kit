# dev-kit

個人常用的開發 bootstrap：Grok 全域規則、VS Code / Dev Container 預設 extension 與 Python 編輯設定。
新機器 clone 一次、跑 `install.sh`，之後每個新專案不必再抄同一套。

## 新機器、新容器、新專案分別做什麼

### 1. 新機器（Windows / WSL / 另一台電腦）— 只做一次

主機要先有 VS Code 和 **Dev Containers** 擴充功能（`ms-vscode-remote.remote-containers`，裝在主機，不要裝進容器）。

```bash
git clone https://github.com/<YOU>/dev-kit.git
cd dev-kit
bash install.sh
```

Windows PowerShell：

```powershell
& "C:\Program Files\Git\bin\bash.exe" .\install.sh
```

這會寫入：

| 寫到哪 | 內容 |
|--------|------|
| `~/.grok/rules/guidance-only.md` | Grok 全域規則 |
| VS Code **User** `settings.json` | `dev.containers.defaultExtensions` + Black / isort / flake8 / pytest 等 |

之後這台電腦開任何 Dev Container，VS Code 都會自動把這份 extension 清單裝進容器。編輯器設定（format on save、line length 120）跟著 User settings 進容器。

### 2. 新容器 — 不必在容器裡再跑 install

不要進容器再 clone / 再跑 `install.sh`。流程是：

1. 主機已經跑過上面的 `install.sh`
2. 用 VS Code 打開專案 → Command Palette → **Dev Containers: Reopen in Container**
3. 容器建好後，VS Code 依 User 裡的 `dev.containers.defaultExtensions` 安裝 extension

已在跑的舊容器看不到新清單：再跑一次 **Dev Containers: Rebuild Container**。

容器裡的專案 `.devcontainer/devcontainer.json` **不必**再列那 11 個 extension。只留這個專案才有的東西（compose、port、interpreter）：

```json
{
  "name": "python-app",
  "dockerComposeFile": ["../docker-compose.yml"],
  "service": "pipeline",
  "workspaceFolder": "/workspace",
  "customizations": {
    "vscode": {
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python"
      }
    }
  }
}
```

完整薄範本：[`templates/python-devcontainer.json`](templates/python-devcontainer.json)。

### 3. 新專案

1. 加一個薄的 `.devcontainer/devcontainer.json`（映像 / compose / port / interpreter）
2. 不要複製 extension 清單
3. Reopen in Container

只有 **沒裝 dev-kit 的人**（同事、Codespaces）才需要把 [`devcontainer/fragment.json`](devcontainer/fragment.json) 貼進該專案的 `customizations.vscode`。

## 這份清單

來源：[`devcontainer/extensions.json`](devcontainer/extensions.json) 與 [`devcontainer/common-settings.json`](devcontainer/common-settings.json)。要改就改這兩個檔，再跑一次 `install.sh`。

- Python、Pylance、Black、isort、flake8
- YAML、Docker、Even Better TOML
- taskexpl、Grok、Format Files

Python：pytest、Black / isort line length 120、flake8 max 120、存檔時 format + organize imports。

`python.linting.*` 是舊鍵，仍寫入以相容；flake8 擴充功能實際讀的是 `flake8.args`。

## 之後怎麼加 task

1. 可重複執行、幂等。
2. 來源是 repo 裡的真實檔案；腳本只負責寫到本機。
3. 在 README 加一行，並把呼叫加進 `install.sh`。
