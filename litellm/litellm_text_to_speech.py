import os
from dotenv import load_dotenv
import litellm

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "tts-1")

# 텍스트를 음성으로 변환
response = litellm.text_to_speech(
    model=MODEL,
    api_key=API_KEY,
    input="안녕하세요, LiteLLM Text-to-Speech 예제입니다.",
    voice="alloy"
)

# 음성 파일로 저장
with open("output.mp3", "wb") as f:
    f.write(response)

print("음성 파일이 output.mp3로 저장되었습니다.") 