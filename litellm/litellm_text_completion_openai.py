import os
from dotenv import load_dotenv
import litellm

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo-instruct")

response = litellm.completion(
    model=MODEL,
    api_key=API_KEY,
    messages=[
        {"role": "user", "content": "파이썬으로 Hello World 출력하는 코드를 알려줘."}
    ]
)

print(response) 