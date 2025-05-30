from datetime import date
from textwrap import dedent
from agents import Agent
from tools import write_file

@Agent(name="writer")
async def writer(state: dict):
    """Generates new Markdown files listed in state['todo']."""
    for item in state.get("todo", []):
        filename = f"docs/{item['filename']}"
        md = dedent(f"""
        ---
        title: {item['title']}
        date: {date.today()}
        ---

        # {item['title']}
        
        _이 페이지는 자동 생성되었습니다. 아래는 주요 학습 포인트입니다._
        
        1. 정의
        2. 핵심 특징
        3. 예제 코드
        
        ```python
        print('Hello, {item['title']}')
        ```
        
        > 더 상세 내용은 추후 업데이트 예정입니다.
        """)
        await write_file.write(filename, md, overwrite=False)
    return state