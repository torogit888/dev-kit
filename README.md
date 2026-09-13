# dev-kit

個人常用的開發 bootstrap：Grok 全域規則、VS Code Dev Container 預設 extension。
新機器 clone 一次、跑 `install.sh`，之後每個新專案不必再抄同一套設定。

## 怎麼拆比較好

不要把「我個人習慣」寫進每一個專案的 `.devcontainer/devcontainer.json`。那會漂移，而且跟同事的環境綁在一起。

| 層 | 放哪 | 誰會帶到 |
|----|------|----------|
| **你的習慣**（幾乎每個容器都要的 extension、format on save） | 這份 repo → 寫進 VS Code **User** `settings.json` 的 `dev.containers.defaultExtensions` | 你開的每一個 Dev Container，自動裝 |
| **這個專案才需要的**（映像、port、compose、該語言的 interpreter path） | 該專案 `.devcontainer/devcontainer.json` | 只這個 repo |
| **給沒裝 dev-kit 的人**（同事、Codespaces） | 可選：把 [`devcontainer/fragment.json`](devcontainer/fragment.json) 貼進專案 | 打開該專案的人 |

編輯器設定（format on save、去行尾空白）本身會跟著 User settings 進容器。真正不會自動跟進去的是 **extension**：主機裝過 Python，容器裡還是空的。所以用 `dev.containers.defaultExtensions`，不要靠每個專案列一份。

專案檔請保持薄，像 [`templates/python-devcontainer.json`](templates/python-devcontainer.json)：只寫 image / port / 該專案的 interpreter。不要再複製一整串 extension。

## 新環境

Git Bash / WSL / macOS / Linux：

```bash
git clone https://github.com/<YOU>/dev-kit.git
cd dev-kit
bash install.sh
```

Windows PowerShell 可呼叫 Git 自帶的 bash：

```powershell
& "C:\Program Files\Git\bin\bash.exe" .\install.sh
```

`install.sh` 會：

1. 把 [`grok/rules/guidance-only.md`](grok/rules/guidance-only.md) 寫到 `~/.grok/rules/guidance-only.md`
2. 把 [`devcontainer/extensions.json`](devcontainer/extensions.json) **合併**進 VS Code User settings（已有的 key 不覆蓋；extension 做聯集）

改完 User settings 後，**新開**的 Dev Container 才會裝到這些 extension。已在跑的容器：Command Palette → `Dev Containers: Rebuild Container`。

Grok 規則：重開 session，或 `grok inspect` 確認有載入 `guidance-only.md`。

可選：clone 進某個專案的 `docs/`：

```bash
git clone https://github.com/<YOU>/dev-kit.git docs/dev-kit
bash docs/dev-kit/install.sh
```

## 目前的 task

| Task | 怎麼跑 | 寫到哪 |
|------|--------|--------|
| Grok：不要擅自跑編譯 / Docker / 測試 | `grok/setup_grok_rules.sh` | `~/.grok/rules/guidance-only.md` |
| Dev Container 常用 extension | `vscode/merge_user_settings.py` | VS Code User `dev.containers.defaultExtensions` |

清單來源：[`devcontainer/extensions.json`](devcontainer/extensions.json)（`common` + `python`）。要加減就改那個檔，再跑一次 `install.sh`。

預設會裝：

- EditorConfig、Even Better TOML、YAML、Prettier、Docker
- Python、Pylance、debugpy、Ruff

不裝 GitLens、遠端套件（`Remote - Containers` 是主機用的，不要塞進容器）。

## 之後怎麼加 task

1. 可重複執行、幂等。
2. 來源是 repo 裡的真實檔案；腳本只負責寫到本機。
3. 在這個 README 表格加一行，並把呼叫加進 `install.sh`。

適合：Grok `~/.grok/rules`、User-level VS Code / Dev Container 預設、新環境檢查。

不適合：某個產品的 build / Docker / 測試（那些寫在該專案 `AGENTS.md`）。
