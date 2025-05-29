from __future__ import annotations

import asyncio
from dotenv import load_dotenv
import os

from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel

@function_tool
def get_weather(city: str):
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."


async def main(model: str, api_key: str):
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=LitellmModel(model=model, api_key=api_key),
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)


if __name__ == "__main__":
    # Load environment variables from .env
    print(os.getcwd())
    print("Files in current directory:")
    for file in os.listdir():
        print(f"- {file}")
    load_dotenv()
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=False)
    args = parser.parse_args()

    model = args.model or os.environ.get("OPENAI_MODEL")
    if not model:
        raise ValueError("Model name not set via --model argument or OPENAI_MODEL in environment variables or .env file.")

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment variables or .env file.")

    asyncio.run(main(model, api_key))