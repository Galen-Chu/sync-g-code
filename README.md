# 🛰️ Sync G-Code: Daily Navigator

> **"Decoding Potential, Not Diagnosis."**

---

## 🧭 Project Philosophy

Sync G-Code is the technical infrastructure of the **Spiritual G-Code** brand.
It functions as an automated **Pilot's Log** — decoding daily celestial and
neuro-spiritual patterns into actionable insights for **Aetheric Pilots**
(Highly Sensitive Persons, HSPs).

The core philosophy is **rational grounding**: using engineering principles
(APIs, automation, CI/CD) to deliver spiritual guidance that is practical
and technical in tone — never vague, mystical, or "New Age fluffy."

**Key metaphors:**
- Consciousness as an **Operating System**
- Spiritual growth as **Refactoring** or **Patch Notes**
- Daily guidance as a **Navigation System**

---

## ✨ Core Features

- **Automated Daily Generation** — Gemini 1.5 Pro generates personalized spiritual content every day at 08:00 Taiwan time (00:00 UTC)
- **Bilingual Output** — every insight is generated in both English and Traditional Chinese (繁體中文)
- **Flight Log Archive** — all generated content is synced to a centralized Google Doc for long-term growth tracking
- **Serverless Architecture** — GitHub Actions handles scheduling and execution; no server to maintain
- **Manual Trigger** — `workflow_dispatch` allows on-demand generation for testing

---

## 🏗️ System Architecture

```
  GitHub Actions (Cron 00:00 UTC)
        │
        ▼
  ┌─────────────┐     ┌──────────────────┐     ┌───────────────┐
  │  main.py     │────▶│ Gemini 1.5 Pro   │────▶│  Google Docs   │
  │  (Trigger)   │     │ (AI Generation)  │     │  (Flight Log)  │
  └─────────────┘     └──────────────────┘     └────���──────────┘
        │                      │
        ▼                      ▼
  Prompt Template      Bilingual Content
  (Date + Context)     (Quote + Guidance)
```

1. **Trigger** — GitHub Actions cron schedule fires daily at 00:00 UTC
2. **Generation** — `main.py` sends a contextual prompt to Gemini 1.5 Pro
3. **Content** — The AI returns a bilingual awakening quote (~1 line) and a navigation guidance (~100 words)
4. **Storage** — Content is written to the configured Google Doc (the Pilot's Log)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Google Gemini API key (from [AI Studio](https://aistudio.google.com/apikey))
- Google Cloud Service Account (for Docs API write access)

### Local Development

```bash
# Clone and set up
git clone https://github.com/Galen-Chu/sync-g-code.git
cd sync-g-code
python -m venv venv
source venv/bin/activate    # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env        # Or create .env manually
# Edit .env with your GEMINI_API_KEY

# Run the navigator
python main.py
```

### Environment Variables

```ini
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_DOCS_ID=your_target_google_doc_id
```

### Google Cloud Setup

1. Download a Service Account JSON key from Google Cloud Console
2. Rename it to `credentials.json` and place in the project root
3. Share the target Google Doc with the Service Account email (Editor access)

---

## ⚙️ Workflow Automation

The GitHub Actions workflow (`.github/workflows/daily_navigator.yml`) runs
automatically every day. Required repository secrets:

| Secret | Description |
|--------|-------------|
| `GEMINI_API_KEY` | Google AI Studio API key |
| `GOOGLE_DOCS_ID` | Target Google Document ID |
| `GOOGLE_CREDENTIALS` | Service Account JSON (base64 encoded) |

To trigger manually: Actions → Daily Spiritual Navigator → Run workflow

---

## 📝 Generated Content Format

Each daily generation produces:

1. **Awakening Quote** — A single-line insight (bilingual)
2. **Navigation Guidance** — ~100 words of practical advice for HSPs

The tone is deliberately **rational, technical, and grounding** — bridging
quantum mechanics, neuroscience, and ancient spiritual wisdom without
descending into vague mysticism.

---

## 🔄 Related Projects

Sync G-Code is part of the G-Code ecosystem:

| Repository | Focus |
|-----------|-------|
| [spiritual-g-code](https://github.com/Galen-Chu/spiritual-g-code) | Full dashboard platform (Django) |
| [psychological-g-code](https://github.com/Galen-Chu/psychological-g-code) | Chakra-Kabbalah system |
| [physiological-g-code](https://github.com/Galen-Chu/physiological-g-code) | DNA ↔ I Ching platform |
| [spec-g-code](https://github.com/Galen-Chu/spec-g-code) | Ecosystem specification hub |
| [skill-g-code](https://github.com/Galen-Chu/skill-g-code) | Claude Code skill definitions |

---

## 📄 License

MIT — see [LICENSE](LICENSE).
