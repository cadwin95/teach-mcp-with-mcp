# 이 파일은 MCP에서 리소스(resource)의 개념과 존재 이유를 설명합니다.
# 리소스는 툴이 접근하는 실제 데이터(파일, DB, API 등)를 추상화한 객체입니다.
# 툴은 리소스를 통해 외부 데이터에 안전하게 접근하며, 리소스는 권한/경로/타입 등을 관리합니다.

class FileResource:
    """파일 시스템의 특정 파일을 리소스로 추상화한 예시 클래스"""
    def __init__(self, path):
        self.path = path
    def read(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            return f.read()
    def write(self, content):
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(content)

# 실제 MCP 툴에서 FileResource를 활용해 파일 읽기/쓰기 기능을 안전하게 제공할 수 있습니다. 