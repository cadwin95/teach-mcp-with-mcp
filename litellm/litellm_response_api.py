import os
from dotenv import load_dotenv
import litellm

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-3.5-turbo")

response, headers = litellm.completion(
    model=MODEL,
    api_key=API_KEY,
    messages=[{"role": "user", "content": "Response API로 헤더를 받아와줘."}],
    return_response_headers=True
)

print("Response:", response)
print("Headers:", headers) 