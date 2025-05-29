from agents import Agent, Runner, function_tool

@function_tool
def hello(name: str) -> str:
    """입력한 이름에 인사합니다."""
    return f"안녕하세요, {name}!"

agent = Agent(
    name="ToolAgent",
    instructions="사용자의 요청에 따라 툴을 사용하세요.",
    tools=[hello],
)

if __name__ == "__main__":
    result = Runner.run_sync(agent, "홍길동에게 인사해줘.")
    print(result.final_output) 