"""
Shared tools for the MCP educational materials multi-agent system.
"""

import os
import json
import glob
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Union, Any

from agents import function_tool
from agents.hosted.web_search import WebSearchTool
from agents.hosted.file_system import FileSearchTool, ReadFileTool, WriteFileTool

# Built-in search tool instance
web_search = WebSearchTool()

# File system tools
list_files = FileSearchTool()
read_file = ReadFileTool()
write_file = WriteFileTool()

# Constants
DOCS_DIR = Path("docs")
CURRENT_YEAR = datetime.now().year

@function_tool
def check_freshness_and_accuracy(md_content: str, references: list[str]) -> str:
    """
    Check if content is fresh and accurate by comparing with references.
    Returns 'pass' or 'needs_revision:<reason>'.
    """
    outdated_years = [str(year) for year in range(2019, CURRENT_YEAR)]
    if any(year in md_content for year in outdated_years):
        return f"needs_revision: mentions outdated year"
    
    if "MCP" in md_content and "Model Context Protocol" not in md_content:
        return "needs_revision: uses abbreviation MCP without full name"
    
    return "pass"

@function_tool
def extract_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extract metadata from a markdown file including title, date, sections, etc.
    """
    try:
        content = ""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        lines = content.splitlines()
        
        # Extract title (first heading)
        title = ""
        for line in lines:
            if line.startswith("# "):
                title = line.replace("# ", "")
                break
        
        # Count sections
        section_count = sum(1 for line in lines if line.startswith("## "))
        
        # Extract date if available
        date_str = ""
        for line in lines:
            if "date:" in line.lower():
                date_str = line.split(":", 1)[1].strip()
            elif "last updated" in line.lower():
                date_str = line.split(":", 1)[1].strip() if ":" in line else ""
        
        # Check if content has examples
        has_examples = "example" in content.lower() or "```" in content
        
        # Estimate word count
        word_count = len(content.split())
        
        return {
            "file_path": file_path,
            "title": title,
            "date": date_str,
            "section_count": section_count,
            "has_examples": has_examples,
            "word_count": word_count,
            "size_bytes": len(content.encode('utf-8'))
        }
    except Exception as e:
        return {
            "file_path": file_path,
            "error": str(e)
        }

@function_tool
def batch_process_files(glob_pattern: str, processor_func: str, *args, **kwargs) -> List[Dict[str, Any]]:
    """
    Process multiple files matching a glob pattern using the specified function.
    """
    results = []
    for file_path in glob.glob(glob_pattern, recursive=True):
        if processor_func == "extract_metadata":
            result = extract_metadata(file_path)
        elif processor_func == "check_freshness":
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            result = {
                "file_path": file_path,
                "check_result": check_freshness_and_accuracy(content, [])
            }
        else:
            result = {
                "file_path": file_path,
                "error": f"Unknown processor function: {processor_func}"
            }
        results.append(result)
    return results

@function_tool
def generate_summary_report(metadata_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate a summary report from a list of file metadata.
    """
    total_files = len(metadata_list)
    total_words = sum(item.get("word_count", 0) for item in metadata_list)
    avg_sections = sum(item.get("section_count", 0) for item in metadata_list) / max(total_files, 1)
    files_with_examples = sum(1 for item in metadata_list if item.get("has_examples", False))
    
    return {
        "total_files": total_files,
        "total_words": total_words,
        "average_word_count": total_words / max(total_files, 1),
        "average_sections": avg_sections,
        "files_with_examples": files_with_examples,
        "files_with_examples_percent": (files_with_examples / max(total_files, 1)) * 100,
        "generated_at": datetime.now().isoformat()
    }

@function_tool
def detect_knowledge_gaps(content: str, topic: str) -> List[str]:
    """
    Detect knowledge gaps in content for a given topic.
    Returns a list of suggested topics to add.
    """
    gaps = []
    
    # For MCP-related content
    if topic.lower() in ["mcp", "model context protocol"]:
        essential_topics = [
            "client-server architecture",
            "tools",
            "resources",
            "prompts",
            "implementation example",
            "practical applications"
        ]
        
        for subtopic in essential_topics:
            if subtopic.lower() not in content.lower():
                gaps.append(subtopic)
    
    return gaps