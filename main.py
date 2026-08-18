import os
from datetime import datetime

from google import genai

# 設定 Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("環境變數 GEMINI_API_KEY 未設定，請檢查 GitHub Actions 的 secret")
client = genai.Client(api_key=api_key)

# gemini-1.5-pro 已下線（API 回傳 404），此處需使用現行支援的模型
MODEL = "gemini-3.6-flash"

def generate_spiritual_content():
    # 這裡未來可以加入抓取星象/農民曆的 API 邏輯
    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
    今天是 {today}。
    你是一位「Spiritual G-Code」導航員，擅長結合量子力學、神經科學與古老靈性智慧。
    請根據今天的能量特質（包含當前春季的律動），為「先行者」提供：
    1. 一句覺醒金句 (Bilingual: English & Traditional Chinese)。
    2. 一段約 100 字的今日導航建議，幫助高敏感族群將感知轉化為力量。
    請注意語氣要理性、具有技術感且接地氣，避免過度虛幻的詞彙。
    """

    response = client.models.generate_content(model=MODEL, contents=prompt)
    return response.text

def main():
    print("正在解碼今日 G-Code...")
    content = generate_spiritual_content()
    print("生成內容：\n", content)

    # TODO: 實作寫入 Google Docs 的邏輯
    # write_to_google_doc(content)

if __name__ == "__main__":
    main()
