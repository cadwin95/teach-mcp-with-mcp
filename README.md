# MCP Educational Materials Multi-Agent System

A powerful multi-agent system for automatically reviewing, updating, and improving educational materials about the Model Context Protocol (MCP).

## Overview

This system uses a coordinated team of specialized AI agents to ensure your MCP educational materials are:

- Up-to-date with the latest information
- Technically accurate
- Pedagogically sound
- Rich with examples and practical applications

## System Architecture

The system is built around these specialized agents:

1. **WebResearchAgent**: Finds the latest MCP information from the web
2. **ContentReviewAgent**: Identifies outdated content and areas for improvement
3. **ContentUpdateAgent**: Updates content based on research and review findings
4. **QualityAssuranceAgent**: Ensures updated content meets quality standards
5. **CodeExampleAgent**: Generates up-to-date code examples for MCP
6. **OrchestratorAgent**: Coordinates all agents in a cohesive workflow

## Features

- **Automated Web Research**: Finds and synthesizes the latest MCP information
- **Content Freshness Analysis**: Identifies outdated information and references
- **Knowledge Gap Detection**: Identifies missing topics that should be covered
- **Educational Quality Evaluation**: Scores content based on pedagogical principles
- **Code Example Generation**: Creates high-quality MCP code examples in multiple languages
- **Quality Assurance**: Ensures updates meet educational standards before publication

## Usage

### Prerequisites

- Python 3.8+
- Required Python packages (install with `pip install -r requirements.txt`)

### Basic Usage

To review and update all MCP documents in the `docs/` directory:

```bash
python src/runner.py
```

### Check-Only Mode

To check documents without making any changes (dry run):

```bash
python src/runner.py --check-only
```

### Target Specific File

To process a specific file:

```bash
python src/runner.py --target docs/mcp-concept.md
```

## Example Workflow

1. The system scans all markdown files in the `docs/` directory
2. For each file, it:
   - Researches the latest information about the topic
   - Reviews the current content for accuracy and freshness
   - Updates content with new information
   - Adds code examples where appropriate
   - Evaluates the quality of the updated content
   - Writes the improved content back to the file if it passes quality thresholds

## Extending the System

The modular agent-based architecture makes it easy to extend the system:

- Add new specialized agents by creating new files in `src/agents/`
- Define new tools in `src/tools.py`
- Update the orchestrator in `src/teach_mcp_agent.py` to incorporate new agents

## License

MIT

---

Built with ❤️ for MCP education
