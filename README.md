# dev-kit

個人常用的開發 bootstrap：Grok 全域規則、VS Code / Dev Container 預設 extension 與 Python 編輯設定。

容器裡不要再 clone、也不要再跑 `install.sh`。設一次在主機的 VS Code User settings，之後每個 Dev Container 會自己把 extension 裝進去。

這台已經套用好了：你的 11 個 extension 和 Black / isort / flake8 / pytest 設定寫進了 VS Code User `settings.json`，Grok 規則寫進了 `~/.grok/rules/guidance-only.md`。

## 三種情況

### 新機器（只做一次）

主機要有 VS Code + **Dev Containers** 擴充功能（裝在主機，不要裝進容器）。

```powershell
git clone https://github.com/<YOU>/dev-kit.git
cd dev-kit
& "C:\Program Files\Git\bin\bash.exe" .\install.sh
```

### 新容器

1. 用 VS Code 打開專案
2. Command Palette → **Dev Containers: Reopen in Container**
3. 容器起來後，VS Code 會依 User 裡的 `dev.containers.defaultExtensions` 安裝那 11 個套件

已經在跑的舊容器看不到新清單：再跑一次 **Rebuild Container**。

### 新專案

`.devcontainer/devcontainer.json` 只留映像 / compose / port / interpreter，不要再貼 extension 清單。AIVideo 已改成這樣，只保留：

```json
"python.defaultInterpreterPath": "/usr/local/bin/python"
```

同事或 Codespaces 沒裝 dev-kit 時，才把 `dev-kit/devcontainer/fragment.json` 貼進該專案。

清單要改就改 `devcontainer/extensions.json` 和 `devcontainer/common-settings.json`，再跑一次 `install.sh`。另外加了 `flake8.args`（現在的 flake8 擴充功能讀這個；你原本的 `python.linting.*` 也留著）。

原理就一句話：**extension 是「這台機器裡的這個 VS Code 視窗」裝的，不是專案資料夾自帶的。** 主機和容器是兩台不同的環境，所以主機裝過 Python，容器裡預設還是空的。

## 兩層設定

```
你的電腦（主機）
  VS Code User settings.json     ← install.sh 寫這裡，整台電腦一份
    dev.containers.defaultExtensions = [那 11 個]
    [python] / black / flake8 / isort ...

某個專案
  .devcontainer/devcontainer.json ← 只寫「這個專案的容器長怎樣」
    映像、compose、port、interpreter
```

打開容器時，VS Code 做的是：

1. 用專案的 `devcontainer.json` 起一個容器（Docker / compose）
2. 在容器裡再裝一個 VS Code Server
3. 讀你主機 User settings 裡的 `dev.containers.defaultExtensions`，往這個容器的 VS Code Server 裝那 11 個套件
4. 編輯器設定（format on save、line length 120）跟著 User settings 進這個視窗

所以不是「容器 clone 了 dev-kit」，也不是「每個專案複製一份 extensions」。是 **VS Code 連進容器時，把你的個人清單帶進去**。

## 為什麼專案檔要薄

| 寫在專案 `.devcontainer` | 寫在 User `defaultExtensions` |
|--------------------------|-------------------------------|
| 每個 repo 都要抄、會漂 | 設一次，之後每個容器都有 |
| 同事也會被強迫裝你的 Grok / taskexpl | 只有你的 VS Code 會帶 |
| 適合：映像、port、這個專案的 Python 路徑 | 適合：你個人一定要的套件和格式化習慣 |

`python.defaultInterpreterPath` 仍放專案裡，因為每個容器的 Python 路徑可能不同；Black / flake8 則是你個人習慣，放 User 層。

## 和「在容器裡跑 install.sh」的差別

`install.sh` 是給新電腦用的：把清單寫進這台主機的 User settings。  
容器每次重建都會是乾淨環境，靠步驟 3 自動再裝套件，不必進容器再設一次。

## 這份清單

來源：[`devcontainer/extensions.json`](devcontainer/extensions.json) 與 [`devcontainer/common-settings.json`](devcontainer/common-settings.json)。要改就改這兩個檔，再跑一次 `install.sh`。

- Python、Pylance、Black、isort、flake8
- YAML、Docker、Even Better TOML
- taskexpl、Grok、Format Files

Python：pytest、Black / isort line length 120、flake8 max 120、存檔時 format + organize imports。

`python.linting.*` 是舊鍵，仍寫入以相容；flake8 擴充功能實際讀的是 `flake8.args`。
