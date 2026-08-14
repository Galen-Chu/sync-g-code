# 🛰️ Sync G-Code: Daily Navigator
> **"Decoding Potential, Not Diagnosis."**

This project is the foundational "Technical Infrastructure" for the **Spiritual G-Code** brand. It functions as an automated "Pilot’s Log" (飛行日誌), decoding daily celestial and neuro-spiritual patterns into actionable insights for "Aetheric Pilots" (Highly Sensitive Persons/HSPs).

## 🎯 Project Goals (專案目標)
- **Automated Insights**: Daily generation of spiritual guidance using Gemini API.
- **Systematic Logging**: Syncing all insights to a centralized Google Doc for long-term growth tracking.
- **Technical Grounding**: Utilizing GitHub Actions for serverless, scheduled execution (CI/CD).

## 🏗️ System Architecture (系統架構)
1. **Trigger**: GitHub Actions (Cron schedule at 00:00 UTC).
2. **Brain**: Python script calling Gemini-1.5-Pro.
3. **Knowledge Base**: Integrated astrology data and traditional almanac (農民曆) logic.
4. **Storage**: Google Docs API (The Permanent Log).

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **Orchestration**: GitHub Actions
- **AI**: Google Generative AI (Gemini)
- **Integration**: Google Cloud SDK (Docs API)
