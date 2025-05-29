import asyncio
import os
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async def main():
    path = os.path.dirname(os.path.abspath(__file__))
    async with MCPServerStdio(params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", path],
    }) as mcp_server:
        agent = Agent(
            name="MCPAgent",
            instructions="파일 시스템 MCP 툴을 사용하세요.",
            mcp_servers=[mcp_server],
        )
        result = await Runner.run(agent, "이 폴더에 있는 파일 목록을 보여줘.")
        print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main()) 