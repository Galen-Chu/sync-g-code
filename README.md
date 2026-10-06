# 🛰️ Sync G-Code: Daily Navigator

> **"Decoding Potential, Not Diagnosis."**
> 「解讀潛能，而非診斷。」

---

## 🧭 Project Philosophy

Sync G-Code is the technical infrastructure of the **Spiritual G-Code** brand.
It functions as an automated **Pilot's Log** — decoding daily celestial and
neuro-spiritual patterns into actionable insights for **Aetheric Pilots**
(Highly Sensitive Persons, HSPs).

Sync G-Code 是 Spiritual G-Code 品牌的技術基礎建設。它是一套自動化的「飛行日誌」——將每日的天體運行與神經靈性模式解碼為可執行的洞察，服務於「先行者」（高敏感族群，HSP）。

The core philosophy is **rational grounding**: using engineering principles
(APIs, automation, CI/CD) to deliver spiritual guidance that is practical
and technical in tone — never vague, mystical, or "New Age fluffy."

核心哲学是**理性接地**：運用工程原則（API、自動化、CI/CD）來傳遞靈性指引，語氣務實且具技術感——絕不虛無飄渺。

**Key metaphors · 核心隱喻：**
- Consciousness as an **Operating System** · 意識如同作業系統
- Spiritual growth as **Refactoring** or **Patch Notes** · 靈性成長如同重構與版本更新
- Daily guidance as a **Navigation System** · 每日指引如同導航系統

---

## ✨ Core Features · 核心功能

- **Automated Daily Generation** — Gemini generates personalized spiritual content every day at 08:23 Taiwan time (00:23 UTC, deliberately off the hour to avoid GitHub Actions schedule congestion)
- **Bilingual Output** — every insight is generated in both English and Traditional Chinese (繁體中文)
- **Flight Log Archive** — each run uploads a `daily-notes-gcode-{date}` artifact (14-day retention) that the [Obsidian_Library](https://github.com/Galen-Chu/Obsidian_Library) `import-reports` pipeline pulls into `raw/reports/` as the `G_Code_Navigator` stream
- **Transient-Error Resilience** — Gemini 503/429 responses are retried with exponential backoff; a single API hiccup no longer costs a missing day
- **Serverless Architecture** — GitHub Actions handles scheduling and execution; no server to maintain
- **Manual Trigger** — `workflow_dispatch` allows on-demand generation for testing

每日自動生成、雙語輸出、飛行日誌歸檔、暫時性錯誤重試、無伺服器架構、手動觸發——透過 GitHub Actions 排程，讓先行者每天早上收到為他們量身打造的導航指引，並自動歸檔進 Obsidian 知識庫。

---

## 🏗️ System Architecture · 系統架構

```
  GitHub Actions (Cron 00:23 UTC)
        │
        ▼
  ┌─────────────┐     ┌──────────────────┐     ┌────────────────┐
  │  main.py     │────▶│ Gemini API       │────▶│ Actions         │
  │  (Trigger)   │     │ (AI Generation,  │     │ artifact        │
  └─────────────┘     │ JSON + retry)    │     │ (MD + JSON)     │
        │                      │         └───────┬────────┘
        ▼                      ▼                 ▼
  Prompt Template      Bilingual Content   Obsidian_Library
  (Date + Context)     (Quote + Guidance)  (import-reports 管線)
```

系統分為三層：觸發層（GitHub Actions 排程）、生成層（Gemini 產出結構化雙語內容，503/429 指數退避重試）、儲存層（artifact → Obsidian_Library 的 `raw/reports/`）。每日 UTC 00:23（台灣時間 08:23）自動執行。

---

## 🚀 Quick Start · 快速開始

### Prerequisites · 前置需求

- Python 3.10+
- Google Gemini API key (from [AI Studio](https://aistudio.google.com/apikey))

### Local Development · 本地開發

```bash
# Clone and set up · 複製並設定
git clone https://github.com/Galen-Chu/sync-g-code.git
cd sync-g-code
python -m venv venv
source venv/bin/activate    # Windows: .\venv\Scripts\activate

# Install dependencies · 安裝依賴
pip install -r requirements.txt

# Run the navigator · 執行導航器
GEMINI_API_KEY=your_key python main.py    # Windows PowerShell: $env:GEMINI_API_KEY="your_key"; python main.py
```

輸出落在 `out/{date}_G_Code_Navigator_每日導航.md` 與同名 `.json`（UTF-8 無 BOM、LF）。

---

## ⚙️ Workflow Automation · 自動化工作流

The GitHub Actions workflow (`.github/workflows/daily_navigator.yml`) runs
automatically every day. Required repository secrets:

GitHub Actions 工作流每日自動執行，需在 repo Settings → Secrets 設定：

| Secret | Description · 說明 |
|--------|-------------|
| `GEMINI_API_KEY` | Google AI Studio API key · Gemini API 金鑰 |

Archival to Obsidian_Library needs no secret on this side — the Library repo pulls
the artifact with its own read-only PAT (`SYNC_G_CODE_TOKEN`, see its
`raw/reports/README.md` contract).

歸檔到 Obsidian_Library 不需要在本 repo 設任何 secret——由 Library 端以唯讀 PAT（`SYNC_G_CODE_TOKEN`）抓取 artifact，契約詳見該庫 `raw/reports/README.md`。

To trigger manually: Actions → Daily Spiritual Navigator → Run workflow

手動觸發：Actions → Daily Spiritual Navigator → Run workflow

---

## 📝 Generated Content Format · 生成內容格式

Each daily generation produces:

每日生成包含：

1. **Awakening Quote · 覺醒金句** — A single-line insight (bilingual · 雙語)
2. **Navigation Guidance · 導航建議** — ~100 words of practical advice for HSPs (~100 字)

The tone is deliberately **rational, technical, and grounding** — bridging
quantum mechanics, neuroscience, and ancient spiritual wisdom without
descending into vague mysticism.

語氣刻意保持理性、技術感且接地——橋接量子力學、神經科學與古老靈性智慧，但不落入虛幻神祕主義。

---

## 🔄 Related Projects · 關聯專案

Sync G-Code is part of the G-Code ecosystem · Sync G-Code 是 G-Code 生態系統的一環：
| Repository | Focus · 領域 |
|-----------|-------------|
| [spiritual-g-code](https://github.com/Galen-Chu/spiritual-g-code) | 🔮 Spiritual dashboard · 靈性儀表板 |
| [psychological-g-code](https://github.com/Galen-Chu/psychological-g-code) | 🕉️ Chakra-Kabbalah · 脈輪與卡巴拉 |
| [physiological-g-code](https://github.com/Galen-Chu/physiological-g-code) | 🧬 DNA ↔ I Ching · 基因與易經 |
| [spec-g-code](https://github.com/Galen-Chu/spec-g-code) | 📋 Specification hub · 規格中樞 |
| [skill-g-code](https://github.com/Galen-Chu/skill-g-code) | 🛸 Claude Code skills · 技能路由 |

---

## 📄 License

MIT — see [LICENSE](LICENSE).
