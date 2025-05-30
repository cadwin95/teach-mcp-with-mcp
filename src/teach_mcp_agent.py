"""
Multi-agent system for reviewing and updating MCP educational materials.
"""

import os
from datetime import datetime
from pathlib import Path

# Import agent and tool infrastructure
from agent import Agent, function_tool
from tools import web_search, list_files, read_file, write_file, check_freshness_and_accuracy
from agents.code_example_agent import code_example_agent, generate_complete_mcp_example

# Constants
DOCS_DIR = Path("docs")
MCP_KEYWORDS = ["Model Context Protocol", "MCP", "function calling", "tool usage", "AI context"]
CURRENT_YEAR = datetime.now().year

# 1. Enhanced tools for specialized tasks

@function_tool
def analyze_content_freshness(content: str, topic: str) -> dict:
    """
    Analyzes content for freshness and relevance to the given topic.
    Returns a detailed analysis with confidence scores and suggested improvements.
    """
    analysis = {
        "is_outdated": False,
        "confidence": 0.0,
        "missing_topics": [],
        "suggested_updates": [],
        "overall_quality": 0.0
    }
    
    # Check for outdated years
    outdated_years = [str(year) for year in range(2019, CURRENT_YEAR)]
    for year in outdated_years:
        if year in content:
            analysis["is_outdated"] = True
            analysis["suggested_updates"].append(f"Update references to year {year}")
            analysis["confidence"] = 0.8
    
    # Check for topic coverage
    if topic.lower() == "mcp" or topic.lower() == "model context protocol":
        expected_subtopics = ["server", "client", "tools", "resources", "prompts"]
        for subtopic in expected_subtopics:
            if subtopic.lower() not in content.lower():
                analysis["missing_topics"].append(subtopic)
                analysis["confidence"] = max(analysis["confidence"], 0.7)
    
    # Assess overall quality (placeholder for more sophisticated analysis)
    word_count = len(content.split())
    if word_count < 300:
        analysis["overall_quality"] = 0.4
        analysis["suggested_updates"].append("Expand content with more details")
    elif word_count < 600:
        analysis["overall_quality"] = 0.6
    else:
        analysis["overall_quality"] = 0.8
    
    return analysis

@function_tool
def generate_educational_content(topic: str, current_content: str, web_research_results: list) -> dict:
    """
    Generates educational content based on topic, existing content, and web research.
    Returns structured educational material with multiple components.
    """
    # This would be implemented with an actual LLM call in production
    # Here we're creating a simplified placeholder
    
    # Extract key information from web research
    key_points = []
    latest_developments = []
    examples = []
    
    for result in web_research_results:
        if "latest" in result.lower() or "new" in result.lower():
            latest_developments.append(result)
        if "example" in result.lower():
            examples.append(result)
        if any(keyword in result.lower() for keyword in ["important", "key", "essential"]):
            key_points.append(result)
    
    # Create the educational content components
    intro = f"# {topic}\n\nThis guide provides up-to-date information about {topic}, including concepts, examples, and best practices.\n\n"
    
    concepts_section = "## Key Concepts\n\n"
    concepts_section += "- " + "\n- ".join(key_points[:3] if key_points else ["[Placeholder for key concept]"])
    concepts_section += "\n\n"
    
    examples_section = "## Examples\n\n"
    examples_section += "- " + "\n- ".join(examples[:2] if examples else ["[Placeholder for example]"])
    examples_section += "\n\n"
    
    practice_section = "## Best Practices\n\n"
    practice_section += "1. " + "\n2. ".join(latest_developments[:3] if latest_developments else ["[Placeholder for best practice]"])
    practice_section += "\n\n"
    
    quiz_section = "## Check Your Understanding\n\n"
    quiz_section += "1. What is the primary purpose of MCP?\n"
    quiz_section += "2. How does MCP differ from traditional function calling?\n"
    quiz_section += "3. What are the main components of an MCP implementation?\n\n"
    
    resources_section = "## Additional Resources\n\n"
    resources_section += "- [MCP Official Documentation](https://modelcontextprotocol.io/introduction)\n"
    resources_section += "- [MCP GitHub Repository](https://github.com/modelcontextprotocol)\n\n"
    
    conclusion = f"---\n\nLast updated: {datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    # Combine all sections
    full_content = intro + concepts_section + examples_section + practice_section + quiz_section + resources_section + conclusion
    
    # Also provide structured components for targeted updates
    return {
        "full_content": full_content,
        "components": {
            "intro": intro,
            "concepts": concepts_section,
            "examples": examples_section,
            "practices": practice_section,
            "quiz": quiz_section,
            "resources": resources_section,
            "conclusion": conclusion
        }
    }

@function_tool
def evaluate_educational_quality(content: str) -> dict:
    """
    Evaluates the quality of educational content using pedagogical principles.
    Returns a detailed assessment with scores and improvement suggestions.
    """
    evaluation = {
        "clarity_score": 0.0,
        "comprehensiveness_score": 0.0, 
        "engagement_score": 0.0,
        "accuracy_score": 0.0,
        "suggestions": []
    }
    
    # Simple heuristics for evaluation (would be more sophisticated with LLM)
    paragraphs = content.split("\n\n")
    
    # Clarity assessment
    avg_sentence_length = sum(len(p.split()) for p in paragraphs) / max(len(paragraphs), 1)
    if avg_sentence_length > 25:
        evaluation["clarity_score"] = 0.5
        evaluation["suggestions"].append("Simplify sentences for better readability")
    else:
        evaluation["clarity_score"] = 0.8
    
    # Comprehensiveness assessment
    heading_count = content.count("\n## ")
    if heading_count < 3:
        evaluation["comprehensiveness_score"] = 0.4
        evaluation["suggestions"].append("Add more sections to cover the topic comprehensively")
    else:
        evaluation["comprehensiveness_score"] = 0.7
    
    # Engagement assessment
    if "?" in content and (content.count("-") > 5 or content.count("1.") > 0):
        evaluation["engagement_score"] = 0.7
    else:
        evaluation["engagement_score"] = 0.4
        evaluation["suggestions"].append("Add questions or interactive elements")
    
    # Accuracy assessment (would require LLM verification)
    if "MCP" in content and "Model Context Protocol" in content:
        evaluation["accuracy_score"] = 0.7
    else:
        evaluation["accuracy_score"] = 0.5
        evaluation["suggestions"].append("Verify technical accuracy of content")
    
    return evaluation

@function_tool
def insert_code_examples(content: str, topic: str) -> str:
    """
    Insert appropriate code examples into educational content based on the topic.
    """
    # Check if the content already has code examples
    if "```python" in content or "```typescript" in content:
        return content  # Already has code examples
    
    # Generate a complete MCP example
    example = generate_complete_mcp_example()
    
    # Find the right place to insert examples (after the Examples section)
    if "## Examples" in content:
        parts = content.split("## Examples", 1)
        examples_section = parts[1].split("##", 1)
        
        # Create the code example content
        code_content = "\n\n### Complete MCP Example\n\n"
        code_content += example["explanation"] + "\n\n"
        code_content += "#### Server Code (Python)\n\n```python\n" + example["server_code"] + "\n```\n\n"
        code_content += "#### Client Code (Python)\n\n```python\n" + example["client_code"] + "\n```\n\n"
        
        # Insert the code examples
        updated_content = parts[0] + "## Examples" + examples_section[0] + code_content + "##" + examples_section[1]
        return updated_content
    
    # If no Examples section, add one
    return content + "\n\n## Code Examples\n\n" + "### Complete MCP Example\n\n" + example["explanation"] + "\n\n" + "#### Server Code (Python)\n\n```python\n" + example["server_code"] + "\n```\n\n" + "#### Client Code (Python)\n\n```python\n" + example["client_code"] + "\n```\n\n"

# 2. Specialized agents for educational content management

# Web Research Agent
web_research_agent = Agent(
    name="WebResearchAgent",
    instructions="""
    Research the latest information about MCP (Model Context Protocol).
    Search for up-to-date documentation, examples, best practices, and recent developments.
    Focus on official sources like modelcontextprotocol.io and trusted tech blogs.
    Summarize findings with key points, examples, and recent updates.
    """,
    tools=[web_search]
)

# Content Review Agent
content_review_agent = Agent(
    name="ContentReviewAgent",
    instructions="""
    Review MCP educational materials for accuracy, freshness, and quality.
    Identify outdated information, gaps in coverage, and areas for improvement.
    Analyze each document for technical accuracy and educational effectiveness.
    Provide specific recommendations for updates and enhancements.
    """,
    tools=[read_file, list_files, analyze_content_freshness, check_freshness_and_accuracy]
)

# Content Update Agent
content_update_agent = Agent(
    name="ContentUpdateAgent",
    instructions="""
    Update MCP educational materials based on review findings and web research.
    Generate new content for identified gaps and outdated sections.
    Maintain consistent style and formatting across all documents.
    Ensure all content is accurate, up-to-date, and pedagogically sound.
    """,
    tools=[read_file, write_file, generate_educational_content, insert_code_examples]
)

# Quality Assurance Agent
quality_assurance_agent = Agent(
    name="QualityAssuranceAgent",
    instructions="""
    Evaluate the quality of MCP educational materials.
    Assess clarity, comprehensiveness, engagement, and accuracy.
    Ensure consistent terminology and formatting.
    Provide improvement recommendations for enhanced learning outcomes.
    """,
    tools=[read_file, evaluate_educational_quality]
)

# Orchestrator Agent
orchestrator_agent = Agent(
    name="OrchestratorAgent",
    instructions="""
    Coordinate the review and update process for MCP educational materials.
    Manage the workflow from content review to final quality assurance.
    Ensure all materials are thoroughly reviewed and updated.
    Prioritize updates based on content freshness and importance.
    """,
    tools=[
        list_files,
        read_file,
        write_file,
        web_research_agent.as_tool(
            tool_name="research_mcp",
            tool_description="Research the latest information about MCP from the web"
        ),
        content_review_agent.as_tool(
            tool_name="review_content",
            tool_description="Review MCP educational materials for accuracy and quality"
        ),
        content_update_agent.as_tool(
            tool_name="update_content",
            tool_description="Update MCP educational materials based on review and research"
        ),
        quality_assurance_agent.as_tool(
            tool_name="assess_quality",
            tool_description="Evaluate the quality of MCP educational materials"
        ),
        code_example_agent.as_tool(
            tool_name="generate_code_examples",
            tool_description="Generate code examples for MCP concepts"
        )
    ]
)

# Main workflow implementation
async def review_and_update_docs(check_only=False, target_file=None):
    """Main workflow to review and update educational materials."""
    # 1. Get list of markdown files to process
    if target_file:
        if os.path.exists(target_file) and target_file.endswith('.md'):
            md_files = [target_file]
        else:
            raise ValueError(f"Target file {target_file} does not exist or is not a markdown file")
    else:
        md_files = await list_files.search("docs/**/*.md")
    
    print(f"Found {len(md_files)} markdown files to process")
    
    results = []
    
    for file_path in md_files:
        print(f"Processing {file_path}...")
        
        # 2. Read the current content
        content = await read_file.read(file_path)
        filename = Path(file_path).name
        topic = filename.replace('.md', '').replace('-', ' ').title()
        
        # 3. Research latest information about the topic
        print(f"Researching information about {topic}...")
        research_results = await web_research_agent.invoke({
            "topic": topic,
            "query": f"latest {topic} MCP Model Context Protocol information"
        })
        
        # 4. Review the current content
        print(f"Reviewing content of {file_path}...")
        review_results = await content_review_agent.invoke({
            "file_path": file_path,
            "content": content,
            "topic": topic
        })
        
        needs_update = review_results.get("needs_update", False) or review_results.get("is_outdated", False)
        
        # In check-only mode, just report findings without updating
        if check_only:
            result = {
                "file_path": file_path,
                "needs_update": needs_update,
                "review_findings": review_results
            }
            results.append(result)
            continue
        
        # 5. Update the content if needed
        if needs_update:
            print(f"Updating content of {file_path}...")
            update_results = await content_update_agent.invoke({
                "file_path": file_path,
                "current_content": content,
                "topic": topic,
                "review_findings": review_results,
                "research_results": research_results
            })
            
            # 6. Generate code examples if appropriate
            if "mcp" in topic.lower() or "model context protocol" in topic.lower():
                print(f"Adding code examples to {file_path}...")
                updated_content = await insert_code_examples(update_results.get("updated_content", content), topic)
            else:
                updated_content = update_results.get("updated_content", content)
            
            # 7. Assess the quality of the updated content
            print(f"Assessing quality of updated content for {file_path}...")
            quality_results = await quality_assurance_agent.invoke({
                "file_path": file_path,
                "content": updated_content
            })
            
            # 8. Write the final content if it passes quality thresholds
            overall_score = quality_results.get("overall_score", 0)
            if overall_score >= 0.7:
                print(f"Writing updated content to {file_path}...")
                await write_file.write(
                    file_path,
                    updated_content,
                    overwrite=True
                )
                result = {
                    "file_path": file_path,
                    "status": "updated",
                    "quality_score": overall_score
                }
            else:
                result = {
                    "file_path": file_path,
                    "status": "update_failed_quality_check",
                    "quality_score": overall_score
                }
        else:
            result = {
                "file_path": file_path,
                "status": "no_update_needed"
            }
        
        results.append(result)
    
    return results

# Entry point for running the multi-agent system
async def run_mcp_education_system(check_only=False, target_file=None):
    """Run the MCP education system to review and update docs."""
    try:
        results = await review_and_update_docs(check_only, target_file)
        
        # Format results for display
        summary = {
            "total_files": len(results),
            "updated": sum(1 for r in results if r.get("status") == "updated"),
            "no_update_needed": sum(1 for r in results if r.get("status") == "no_update_needed"),
            "update_failed": sum(1 for r in results if r.get("status") == "update_failed_quality_check"),
            "checked_only": check_only
        }
        
        print("\n=== MCP Education System Results ===")
        print(f"Total files processed: {summary['total_files']}")
        if check_only:
            needs_update = sum(1 for r in results if r.get("needs_update", False))
            print(f"Files needing updates: {needs_update}")
        else:
            print(f"Files updated: {summary['updated']}")
            print(f"Files not needing updates: {summary['no_update_needed']}")
            print(f"Files failing quality check: {summary['update_failed']}")
        print("===================================")
        
        return {
            "status": "success", 
            "results": results,
            "summary": summary
        }
    except Exception as e:
        print(f"Error running MCP education system: {e}")
        return {"status": "error", "message": str(e)}

# If running as a script
if __name__ == "__main__":
    import asyncio
    
    # Run the multi-agent system
    asyncio.run(run_mcp_education_system()) 