# 이 파일은 MCP에서 툴(Tool)의 개념과 사용법을 보여줍니다.
# 툴은 LLM이 외부 기능(API, 파일, DB 등)을 안전하게 호출할 수 있도록 표준화된 인터페이스를 제공합니다.
# MCP 서버에 툴을 등록하면, 클라이언트가 툴 목록을 조회하고, 원하는 툴을 호출할 수 있습니다.

from mcp.server import Tool, ToolCallResult

class AddTool(Tool):
    name = "add"
    description = "두 숫자를 더합니다."
    input_schema = {
        "type": "object",
        "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
        "required": ["a", "b"]
    }
    async def call(self, args):
        result = args["a"] + args["b"]
        return ToolCallResult(content=str(result))

# 서버에서 tools = [AddTool()] 형태로 등록하면 클라이언트가 "add" 툴을 사용할 수 있습니다. 