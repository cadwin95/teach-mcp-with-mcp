import os
from dotenv import load_dotenv
import litellm

load_dotenv()
API_BASE = "http://localhost:4000"  # 필요시 .env에서 불러오도록 수정 가능
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "openai/mistral")

response = litellm.completion(
    model=MODEL,  # .env에서 불러온 모델명 사용
    api_key=API_KEY,
    api_base=API_BASE,
    messages=[
        {"role": "user", "content": "안녕! 오늘 날씨 어때?"}
    ],
)

print(response) 