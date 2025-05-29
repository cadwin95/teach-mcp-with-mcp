# 이 파일은 MCP 클라이언트의 기본 구조와 존재 이유를 보여줍니다.
# MCP 클라이언트는 LLM 또는 사용자 앱이 MCP 서버에 연결해 툴 목록을 조회하고, 툴을 호출할 수 있게 해줍니다.
# 예시: 서버에 등록된 툴을 자동으로 탐색하고, 원하는 기능을 실행할 수 있습니다.

import asyncio
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

async def main():
    params = StdioServerParameters(command="python", args=["modelcontext_server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("서버 툴 목록:", [t.name for t in tools.tools])
            # 첫 번째 툴 호출 예시
            if tools.tools:
                result = await session.call_tool(tools.tools[0].name, {"name": "홍길동"})
                print("툴 호출 결과:", result.content)

if __name__ == "__main__":
    asyncio.run(main()) 