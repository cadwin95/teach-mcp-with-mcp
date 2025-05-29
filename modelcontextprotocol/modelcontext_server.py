# 이 파일은 MCP(Model Context Protocol) 서버의 기본 구조와 존재 이유를 보여줍니다.
# MCP 서버는 LLM이 사용할 수 있는 툴(기능)을 외부에서 표준 방식으로 제공하기 위해 존재합니다.
# 예시: 파일 시스템, 외부 API, 데이터베이스 등 다양한 리소스를 LLM이 안전하게 활용할 수 있게 해줍니다.

from mcp.server import MCPServer, Tool, ToolCallResult

class HelloTool(Tool):
    name = "hello"
    description = "입력한 이름에 인사합니다."
    input_schema = {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}

    async def call(self, args):
        return ToolCallResult(content=f"안녕하세요, {args['name']}님!")

class MyServer(MCPServer):
    tools = [HelloTool()]

if __name__ == "__main__":
    MyServer().run() 