import os
from dotenv import load_dotenv
import asyncio
from litellm.mcp import MCPClient

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-3.5-turbo")

async def main():
    async with MCPClient("ws://localhost:8080") as mcp:
        response = await mcp.completion(
            model=MODEL,
            api_key=API_KEY,
            messages=[{"role": "user", "content": "MCP로 LLM 호출 예제 보여줘."}]
        )
        print(response)

if __name__ == "__main__":
    asyncio.run(main()) 