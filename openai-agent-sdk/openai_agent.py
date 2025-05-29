from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Answer the user's question."
)

if __name__ == "__main__":
    result = Runner.run_sync(agent, "파이썬에서 리스트를 정렬하는 방법을 알려줘.")
    print(result.final_output) 