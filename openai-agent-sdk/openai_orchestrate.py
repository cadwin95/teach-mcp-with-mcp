from agents import Agent, Runner
import asyncio

spanish_agent = Agent(
    name="SpanishAgent",
    instructions="Translate the user's message to Spanish."
)
french_agent = Agent(
    name="FrenchAgent",
    instructions="Translate the user's message to French."
)

orchestrator = Agent(
    name="Orchestrator",
    instructions="사용자의 요청에 따라 번역 툴을 사용하세요.",
    tools=[
        spanish_agent.as_tool(tool_name="to_spanish", tool_description="스페인어로 번역"),
        french_agent.as_tool(tool_name="to_french", tool_description="프랑스어로 번역"),
    ],
)

if __name__ == "__main__":
    result = Runner.run_sync(orchestrator, "'안녕하세요'를 스페인어와 프랑스어로 번역해줘.")
    print(result.final_output) 