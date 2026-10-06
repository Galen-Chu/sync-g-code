# 🚀 GUIDE.md: 系統安裝與執行指南 (System Installation & Execution Guide)

本手冊旨在協助開發者（及 AI Agent）在地端環境與 GitHub Actions 中順利啟動 Daily Spiritual Navigator。

## 🛠️ 1. 地端環境設置 (Local Environment Setup)

### A. 複製專案與建立虛擬環境

為了保持系統潔淨，請務必使用 Python 虛擬環境：

```bash
# 複製專案 (Clone the repository)
git clone https://github.com/Galen-Chu/sync-g-code.git
cd sync-g-code

# 建立虛擬環境 (Create Virtual Environment)
python -m venv venv

# 啟動虛擬環境 (Activate)
# macOS/Linux:
source venv/bin/activate
# Windows:
# .\venv\Scripts\activate
```

### B. 安裝必要依賴 (Install Dependencies)

```bash
pip install -r requirements.txt
```

## 🧠 2. Gemini API 配置 (Gemini Configuration)

本專案核心大腦為 Google Gemini API（SDK：`google-genai`）。

- **取得金鑰**：至 [Google AI Studio](https://aistudio.google.com/apikey) 申請 API Key。
- **地端測試配置**：設定環境變數即可（CI 端則存於 GitHub Secrets）：

```bash
# macOS/Linux
export GEMINI_API_KEY=在此處貼上你的金鑰
# Windows PowerShell
# $env:GEMINI_API_KEY="在此處貼上你的金鑰"
```

- **驗證 Gemini 可用性**：

```bash
python -c "from google import genai; import os; genai.Client(api_key=os.environ['GEMINI_API_KEY']); print('Gemini Link: Success')"
```

## 📦 3. 歸檔管線 (Archive Pipeline)

「飛行日誌」的儲存已從 Google Docs 改為 **GitHub Actions artifact → Obsidian_Library**（pull 模型）：

1. `main.py` 將生成內容寫成 `out/{date}_G_Code_Navigator_每日導航.md` 與同名 `.json`（UTF-8 無 BOM、LF，符合 Library 端檔名契約）。
2. workflow 上傳 artifact `daily-notes-gcode-{date}`（保留 14 天）。
3. [Obsidian_Library](https://github.com/Galen-Chu/Obsidian_Library) 的 `import-reports.yml` 每日以 `fetch_reports.py` 抓取入庫 `raw/reports/{date}/`，成為第四條串流。
4. 唯一手動前置（在 Library repo，非本 repo）：設定唯讀 PAT secret `SYNC_G_CODE_TOKEN`。
5. 缺文自癒：手動 dispatch 補產 artifact 後，Library 端隔日 `--backfill` 自動入庫。

## 🚀 4. 執行與自動化 (Execution & Automation)

### 地端執行測試 (Local Run)

```bash
python main.py          # 產出會落在 out/ 目錄（已 gitignore）
```

### GitHub Actions 自動化 (Production)

每天台灣時間 08:23（UTC 00:23，刻意離開整點避開排程尖峰）自動執行；暫時性錯誤（503 滿載／429 限流）以指數退避重試約 17 分鐘。

本 repo 只需設定一個 Secret：

- `GEMINI_API_KEY`

## 🧭 5. CLI Agent 協作規範 (AI Agent Instructions)

當你使用 Claude Code 或 Gemini CLI 進行開發時，請遵循以下 Prompt 範本：
「請先讀取 GUIDE.md 與 SKILL.md。我目前在地端開發環境，請幫我檢查 main.py 的環境變數讀取與 out/ 產檔邏輯是否符合手冊中的歸檔管線，並確認輸出檔名符合 Obsidian_Library 的 raw/reports 契約。」

## 📜 6. 安全性與維運 (Security & Maintenance)

- **嚴禁 Commit 私密資訊**：`.gitignore` 已排除 `.env`、`credentials.json` 與 `out/`。
- **日誌格式**：每次執行應產生雙語日誌（Bilingual Log），紀錄 token 用量與解碼成功與否。
- **額度觀念**：本系統每日僅 1 次請求（約數百 token）；若遇 503 為 Google 端容量問題而非帳號限額，長期解法是在 AI Studio 專案開啟計費。
