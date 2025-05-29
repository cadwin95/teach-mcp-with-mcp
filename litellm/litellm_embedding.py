import os
from dotenv import load_dotenv
import litellm

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("OPENAI_EMBED_MODEL", "openai/text-embedding-ada-002")

response = litellm.embedding(
    model=EMBED_MODEL,
    api_key=API_KEY,
    input=["임베딩 테스트 문장입니다."]
)

print("임베딩 결과:", response) 