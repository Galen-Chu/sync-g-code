🚀 GUIDE.md: 系統安裝與執行指南 (System Installation & Execution Guide)
本手冊旨在協助開發者（及 AI Agent）在地端伺服器與 GitHub 環境中順利啟動 Daily Spiritual Navigator。

🛠️ 1. 地端環境設置 (Local Environment Setup)
A. 複製專案與建立虛擬環境
為了保持系統潔淨，請務必使用 Python 虛擬環境：

Bash
# 複製專案 (Clone the repository)
git clone <your-repo-url>
cd sync-g-code

# 建立虛擬環境 (Create Virtual Environment)
python3 -m venv venv

# 啟動虛擬環境 (Activate)
# macOS/Linux:
source venv/bin/activate
# Windows:
# .\venv\Scripts\activate

B. 安裝必要依賴 (Install Dependencies)
Bash
pip install -r requirements.txt

🧠 2. Gemini CLI 與 API 配置 (Gemini Configuration)
本專案核心大腦為 Google Gemini API。請確保您的地端環境已正確配置金鑰。

取得金鑰: 至 Google AI Studio 申請 API KEY。

地端測試配置:
在專案根目錄建立 .env 檔案（此檔案已被 .gitignore 排除，請安心存放金鑰）：

程式碼片段
GEMINI_API_KEY=在此處貼上你的金鑰
GOOGLE_DOCS_ID=在此處貼上目標Google文件ID
驗證 Gemini 可用性:
執行以下簡單指令，確保 CLI Agent 能與 Google AI 通訊：

Bash
python -c "import os; import google.generativeai as genai; genai.configure(api_key=os.environ.get('GEMINI_API_KEY')); print('Gemini Link: Success')"

☁️ 3. Google Cloud 授權 (Cloud Infrastructure)
為了讓程式具備寫入「飛行日誌」(Google Docs) 的能力，請完成以下「接地」步驟：

下載憑證: 從 Google Cloud Console 下載 Service Account 的 JSON 金鑰。
重新命名: 將檔案重新命名為 credentials.json 並存放在專案根目錄。
手動授權: 打開目標 Google Doc，點擊「共用」，將 Service Account 的 Email 加入並給予「編輯者」權限。

🚀 4. 執行與自動化 (Execution & Automation)
地端執行測試 (Local Run)

Bash
# 啟動腳本進行解碼與紀錄
python main.py
GitHub Actions 自動化 (Production)
本系統預計於每天台灣時間 08:00 (UTC 00:00) 自動執行。

請確保已在 GitHub Secrets 設定:
GEMINI_API_KEY
GOOGLE_DOCS_ID
GOOGLE_CREDENTIALS (將 credentials.json 內容完整貼入)

🧭 5. CLI Agent 協作規範 (AI Agent Instructions)
當你使用 Claude Code 或 Gemini CLI 進行開發時，請遵循以下 Prompt 範本：
「請先讀取 GUIDE.md 與 SKILL.md。我目前在地端開發環境，請幫我檢查 main.py 的環境變數讀取邏輯是否符合手冊中的 .env 配置，並確保 credentials.json 的讀取路徑正確。」

📜 6. 安全性與維護 (Security)
嚴禁 Commit 私密資訊: 請再次檢查 .gitignore 是否包含 .env 與 *.json。
日誌格式: 每次執行應產生雙語日誌 (Bilingual Log)，紀錄解碼成功與否。
