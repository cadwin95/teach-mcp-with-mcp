"""
MCP 교육 자료 자동 업데이트 통합 Agent Runner
각 agent들을 순차적으로 실행하여 docs/ 폴더의 교육 자료를 체계적으로 업데이트합니다.
"""

import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import argparse

# Agent imports
from agents import Agent, Runner
from agents.directory_agent import directory_audit
from agents.gap_agent import gap_analysis  
from agents.writer_agent import writer
from agents.qa_agent import qa
from agents.builder_agent import builder

# Tool imports
from tools import (
    web_search,
    list_files,
    read_file,
    write_file,
    check_freshness_and_accuracy,
    extract_metadata,
    detect_knowledge_gaps,
    generate_summary_report
)

# Constants
DOCS_DIR = Path("docs")
MCP_TOPICS = [
    "MCP 개념",
    "MCP 서버",
    "MCP 클라이언트", 
    "MCP 툴과 리소스",
    "MCP 프롬프트",
    "MCP 실전 예제",
    "LiteLLM 연동",
    "OpenAI Agents SDK 연동"
]

class MCPEducationRunner:
    """MCP 교육 자료 업데이트를 위한 통합 Runner"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.state = {
            "topic": "MCP (Model Context Protocol)",
            "docs_dir": str(DOCS_DIR),
            "timestamp": datetime.now().isoformat(),
            "existing_docs": [],
            "doc_meta": {},
            "todo": [],
            "updates": [],
            "errors": []
        }
    
    async def run_pipeline(self, target_file: str = None) -> Dict[str, Any]:
        """전체 파이프라인 실행"""
        try:
            print("🚀 MCP 교육 자료 업데이트 파이프라인 시작...")
            print(f"   모드: {'체크 전용 (Dry Run)' if self.dry_run else '실제 업데이트'}")
            
            # 1단계: 디렉토리 감사 - 현재 문서 상태 파악
            print("\n📂 1단계: 문서 디렉토리 스캔 중...")
            self.state = await directory_audit(self.state)
            print(f"   발견된 문서: {len(self.state['existing_docs'])}개")
            
            # 2단계: 웹 리서치 - 최신 MCP 정보 수집
            print("\n🔍 2단계: 최신 MCP 정보 웹 리서치...")
            await self._research_latest_info()
            
            # 3단계: 갭 분석 - 누락된 문서 확인
            print("\n📊 3단계: 교육 자료 갭 분석...")
            self.state = await gap_analysis(self.state)
            print(f"   생성 필요 문서: {len(self.state['todo'])}개")
            
            # 4단계: 콘텐츠 업데이트 - 기존 문서 개선
            print("\n✏️ 4단계: 기존 문서 콘텐츠 업데이트...")
            await self._update_existing_docs(target_file)
            
            # 5단계: 새 문서 작성 - 누락된 주제 추가
            if not self.dry_run and self.state['todo']:
                print("\n📝 5단계: 새로운 문서 작성...")
                self.state = await writer(self.state)
                print(f"   작성된 문서: {len(self.state['todo'])}개")
            
            # 6단계: 품질 보증 - 전체 문서 검증
            print("\n✅ 6단계: 품질 보증 검사...")
            self.state = await qa(self.state)
            
            # 7단계: 빌드 & 배포 (Git 커밋)
            if not self.dry_run and self.state.get('updates'):
                print("\n🏗️ 7단계: GitHub Pages 빌드 & 배포...")
                self.state = await builder(self.state)
            
            # 최종 리포트 생성
            return self._generate_final_report()
            
        except Exception as e:
            print(f"\n❌ 파이프라인 실행 중 오류 발생: {str(e)}")
            self.state['errors'].append(str(e))
            return self._generate_final_report()
    
    async def _research_latest_info(self):
        """최신 MCP 정보 웹 리서치"""
        research_queries = [
            "Model Context Protocol latest updates 2025",
            "MCP server client tutorial examples",
            "Anthropic MCP documentation guide"
        ]
        
        research_results = []
        for query in research_queries:
            try:
                result = await web_search(query)
                research_results.extend(result[:3])  # 상위 3개 결과만
            except Exception as e:
                print(f"   ⚠️ 리서치 실패: {query} - {str(e)}")
        
        self.state['research_results'] = research_results
        print(f"   수집된 리서치 결과: {len(research_results)}개")
    
    async def _update_existing_docs(self, target_file: str = None):
        """기존 문서 업데이트"""
        files_to_update = []
        
        if target_file:
            # 특정 파일만 업데이트
            if Path(target_file).exists():
                files_to_update = [target_file]
            else:
                print(f"   ⚠️ 대상 파일을 찾을 수 없음: {target_file}")
                return
        else:
            # 모든 마크다운 파일 업데이트
            files_to_update = self.state['existing_docs']
        
        for file_path in files_to_update:
            try:
                # 파일 읽기
                content = await read_file(file_path)
                
                # 메타데이터 추출
                metadata = extract_metadata(file_path)
                
                # 지식 갭 확인
                knowledge_gaps = detect_knowledge_gaps(content, "MCP")
                
                # 신선도 및 정확성 체크
                freshness_check = check_freshness_and_accuracy(
                    content, 
                    self.state.get('research_results', [])
                )
                
                # 업데이트 필요 여부 판단
                needs_update = (
                    freshness_check.startswith("needs_revision") or
                    len(knowledge_gaps) > 0 or
                    "2024" not in content  # 예시: 오래된 연도 체크
                )
                
                if needs_update:
                    if not self.dry_run:
                        # 실제 업데이트 수행
                        updated_content = await self._enhance_content(
                            file_path, content, knowledge_gaps
                        )
                        await write_file(file_path, updated_content, overwrite=True)
                        
                    self.state['updates'].append({
                        'file': file_path,
                        'status': 'updated' if not self.dry_run else 'needs_update',
                        'gaps': knowledge_gaps,
                        'freshness': freshness_check
                    })
                    
                print(f"   {'✅' if not needs_update else '🔄'} {Path(file_path).name}")
                
            except Exception as e:
                print(f"   ❌ {Path(file_path).name} - 오류: {str(e)}")
                self.state['errors'].append(f"{file_path}: {str(e)}")
    
    async def _enhance_content(self, file_path: str, content: str, gaps: List[str]) -> str:
        """콘텐츠 개선 로직"""
        enhanced = content
        
        # 날짜 업데이트
        today = datetime.now().strftime("%Y-%m-%d")
        if "Last updated:" in enhanced:
            enhanced = enhanced.replace(
                enhanced[enhanced.find("Last updated:"):enhanced.find("\n", enhanced.find("Last updated:"))],
                f"Last updated: {today}"
            )
        else:
            enhanced += f"\n\n---\n\nLast updated: {today}\n"
        
        # 누락된 섹션 추가
        if gaps and "implementation example" in gaps:
            example_section = """
## 구현 예제

```python
# MCP 서버 기본 구현
from mcp.server import MCPServer, Tool

class MyMCPServer(MCPServer):
    tools = [
        # 여기에 툴 정의
    ]
    
    async def handle_request(self, request):
        # 요청 처리 로직
        pass

if __name__ == "__main__":
    MyMCPServer().run()
```
"""
            enhanced = enhanced.replace("## ", example_section + "\n## ", 1)
        
        return enhanced
    
    def _generate_final_report(self) -> Dict[str, Any]:
        """최종 리포트 생성"""
        total_docs = len(self.state['existing_docs'])
        updated_docs = len([u for u in self.state['updates'] if u['status'] == 'updated'])
        needs_update = len([u for u in self.state['updates'] if u['status'] == 'needs_update'])
        new_docs = len(self.state['todo'])
        errors = len(self.state['errors'])
        
        print("\n" + "="*60)
        print("📋 MCP 교육 자료 업데이트 완료 리포트")
        print("="*60)
        print(f"총 문서 수: {total_docs}")
        print(f"업데이트된 문서: {updated_docs}")
        print(f"업데이트 필요 문서: {needs_update}")
        print(f"새로 생성된 문서: {new_docs}")
        print(f"오류 발생: {errors}")
        print(f"실행 시간: {self.state['timestamp']}")
        print("="*60)
        
        return {
            "status": "success" if errors == 0 else "partial_success",
            "summary": {
                "total_docs": total_docs,
                "updated": updated_docs,
                "needs_update": needs_update,
                "new_docs": new_docs,
                "errors": errors
            },
            "details": {
                "updates": self.state['updates'],
                "todos": self.state['todo'],
                "errors": self.state['errors']
            },
            "timestamp": self.state['timestamp']
        }


async def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description="MCP 교육 자료 자동 업데이트 시스템"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="실제 업데이트 없이 체크만 수행"
    )
    parser.add_argument(
        "--target",
        type=str,
        help="특정 파일만 업데이트 (예: docs/mcp-concept.md)"
    )
    
    args = parser.parse_args()
    
    # Runner 실행
    runner = MCPEducationRunner(dry_run=args.dry_run)
    result = await runner.run_pipeline(target_file=args.target)
    
    # 결과 반환
    return result


if __name__ == "__main__":
    # 이벤트 루프 실행
    result = asyncio.run(main())
    
    # 종료 코드 설정
    exit(0 if result['status'] == 'success' else 1)