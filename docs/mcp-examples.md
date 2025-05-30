---
layout: default
title: MCP 예제 코드
---

# MCP 예제 코드

실제 Python 기반 MCP 서버와 클라이언트 예시입니다.

---

## 1. MCP 서버 간단 예제

```python
from mcp.server.stdio import StdioServer

class EchoServer(StdioServer):
    def handle_request(self, request):
        # 요청 내용을 그대로 응답
        return {"output": f"Echo: {request.get('input')}"}

if __name__ == "__main__":
    EchoServer().run()
```

---

## 2. MCP 클라이언트 예제

```python
from mcp.client.stdio import stdio_client

# MCP 서버(EchoServer)가 실행 중이어야 합니다.
with stdio_client("python3 echo_server.py") as client:
    response = client.send({"input": "Hello MCP"})
    print(response["output"])  # Echo: Hello MCP
```

---

## 3. 외부 모델(LiteLLM/OpenAI) 연동 예시

```python
import litellm

def call_openai(prompt):
    completion = litellm.completion(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion['choices'][0]['message']['content']

# MCP의 Tool로 등록 가능
```

---

## 4. 실전 활용 흐름

1. MCP 서버를 구현/실행
2. 클라이언트에서 stdio/socket/HTTP 등으로 요청
3. 서버가 적절한 LLM/툴/DB/API로 라우팅/실행
4. 결과를 클라이언트에 응답

---

## 5. 더 알아보기

- [공식 예제](https://modelcontextprotocol.io/examples)
- [OpenAI Agents SDK MCP 예제](https://openai.github.io/openai-agents-python/mcp/)

---

[🔙 개념 설명으로](mcp-concept.md)	| [메인으로](index.md)
