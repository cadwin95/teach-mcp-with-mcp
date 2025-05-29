import os
from dotenv import load_dotenv
import litellm

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-3.5-turbo")
EMBED_MODEL = "openai/text-embedding-ada-002"

# 채팅 예제
gpt_response = litellm.completion(
    model=CHAT_MODEL,
    api_key=API_KEY,
    messages=[{"role": "user", "content": "OpenAI API로 무엇을 할 수 있나요?"}]
)
print("Chat:", gpt_response)

# 임베딩 예제
embedding = litellm.embedding(
    model=EMBED_MODEL,
    api_key=API_KEY,
    input=["OpenAI 임베딩 테스트"],
)
print("Embedding:", embedding) 