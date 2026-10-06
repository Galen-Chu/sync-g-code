import json
import os
import sys
import time
import zoneinfo
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import errors as genai_errors
from google.genai import types

# gemini-1.5-pro 已下線（API 回傳 404），此處需使用現行支援的模型
MODEL = "gemini-3.6-flash"
# 檔名日期對齊台灣日曆天（Actions runner 是 UTC，跨日會差一天）
TZ = zoneinfo.ZoneInfo("Asia/Taipei")

# 輸出契約：Obsidian_Library 的 raw/reports/ 檔名規則
# {date}_{Stream}_{標題}.md / .json，日期取自檔名前綴（非 artifact created_at）
STREAM = "G_Code_Navigator"
TITLE = "每日導航"
OUT_DIR = Path(__file__).resolve().parent / "out"

# 暫時性錯誤（模型高負載 503／限流 429 等）指數退避重試；
# 免費層尖峰時段可能連續滿載數分鐘（實測 2026-10-06 連 5 次全 503、
# 持續超過 2 分 40 秒），重試視窗拉長到約 17 分鐘
RETRYABLE_CODES = {429, 500, 502, 503, 504}
MAX_ATTEMPTS = 6
BACKOFF_BASE_SECONDS = 60
BACKOFF_MAX_SECONDS = 300

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "quote_en": {"type": "string", "description": "Awakening quote in English, one line"},
        "quote_zh": {"type": "string", "description": "覺醒金句，繁體中文，一行"},
        "guidance": {"type": "string", "description": "今日導航建議，繁體中文，約 100 字"},
    },
    "required": ["quote_en", "quote_zh", "guidance"],
}


def season_of(today: str) -> str:
    month = int(today[5:7])
    if 3 <= month <= 5:
        return "春"
    if 6 <= month <= 8:
        return "夏"
    if 9 <= month <= 11:
        return "秋"
    return "冬"


def build_prompt(today: str) -> str:
    return f"""
    今天是 {today}。
    你是一位「Spiritual G-Code」導航員，擅長結合量子力學、神經科學與古老靈性智慧。
    請根據今天的能量特質（包含當前{season_of(today)}季的律動），為「先行者」提供：
    1. 一句覺醒金句 (Bilingual: English & Traditional Chinese)。
    2. 一段約 100 字的今日導航建議，幫助高敏感族群將感知轉化為力量。
    請注意語氣要理性、具有技術感且接地氣，避免過度虛幻的詞彙。
    """


def generate_spiritual_content(client: genai.Client, today: str) -> dict:
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=RESPONSE_SCHEMA,
    )
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = client.models.generate_content(
                model=MODEL, contents=build_prompt(today), config=config
            )
            data = json.loads(response.text)
            missing = [k for k in RESPONSE_SCHEMA["required"] if not data.get(k)]
            if missing:
                raise ValueError(f"回應缺少欄位：{', '.join(missing)}")
            usage = getattr(response, "usage_metadata", None)
            if usage:
                print(
                    f"Token 用量：prompt={getattr(usage, 'prompt_token_count', '?')} "
                    f"output={getattr(usage, 'candidates_token_count', '?')} "
                    f"total={getattr(usage, 'total_token_count', '?')}"
                )
            return data
        except genai_errors.APIError as e:
            code = getattr(e, "code", None)
            if code not in RETRYABLE_CODES or attempt == MAX_ATTEMPTS:
                print(
                    f"Gemini API 重試 {MAX_ATTEMPTS - 1} 次後仍失敗"
                    f"（HTTP {code}），當日內容缺文；"
                    "可稍後手動 dispatch 補產（artifact 保留 14 天，"
                    "Library 端隔日 backfill 會自動入庫）。",
                    file=sys.stderr,
                )
                raise
            wait = min(BACKOFF_BASE_SECONDS * (2 ** (attempt - 1)),
                       BACKOFF_MAX_SECONDS)
            print(
                f"Gemini API 暫時性錯誤（HTTP {code}），"
                f"{wait} 秒後重試（{attempt}/{MAX_ATTEMPTS - 1} 次重試）…",
                file=sys.stderr,
            )
            time.sleep(wait)


def render_markdown(today: str, data: dict) -> str:
    return f"""---
created: {today}
tags:
  - g-code-navigator
  - daily-report
status: generated
---

# G-Code Navigator 每日導航 ({today})

> {data["quote_en"]}
> {data["quote_zh"]}

## 今日導航建議

{data["guidance"]}
"""


def render_json(today: str, data: dict) -> str:
    payload = {
        "meta": {
            "schema_version": 1,
            "report_id": "gcode-navigator",
            "date": today,
            "generated_at": datetime.now(TZ).isoformat(timespec="seconds"),
            "producer": "sync-g-code",
            "source_chain": "gemini",
            "model": MODEL,
        },
        "quote": {"en": data["quote_en"], "zh": data["quote_zh"]},
        "guidance": data["guidance"],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def write_files(today: str, data: dict) -> list:
    OUT_DIR.mkdir(exist_ok=True)
    stem = f"{today}_{STREAM}_{TITLE}"
    files = []
    for suffix, text in ((".md", render_markdown(today, data)),
                         (".json", render_json(today, data))):
        path = OUT_DIR / (stem + suffix)
        # 契約：UTF-8 無 BOM、LF 換行
        path.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))
        files.append(path)
    return files


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("環境變數 GEMINI_API_KEY 未設定，請檢查 GitHub Actions 的 secret")
    client = genai.Client(api_key=api_key)

    today = datetime.now(TZ).strftime("%Y-%m-%d")
    print("正在解碼今日 G-Code...")
    data = generate_spiritual_content(client, today)
    print(render_markdown(today, data))
    for path in write_files(today, data):
        print(f"已輸出：{path}")


if __name__ == "__main__":
    main()
