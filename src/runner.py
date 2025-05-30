"""
Runner script for the MCP educational materials multi-agent system.
"""

import asyncio
import argparse
from pathlib import Path
from teach_mcp_agent import run_mcp_education_system

async def main(args):
    """Main entry point for running the system."""
    print("=" * 60)
    print(f"Starting MCP Educational Materials Multi-Agent System")
    print("=" * 60)
    
    if args.check_only:
        print("Running in check-only mode (no updates will be applied)")
    
    if args.target:
        print(f"Processing target file: {args.target}")
    
    # Pass the arguments to the multi-agent system
    result = await run_mcp_education_system(
        check_only=args.check_only,
        target_file=args.target
    )
    
    print("\nSummary:")
    if result["status"] == "success":
        summary = result["summary"]
        print(f"✅ Successfully processed {summary['total_files']} files")
        
        if args.check_only:
            needs_update = sum(1 for r in result["results"] if r.get("needs_update", False))
            print(f"📋 Files needing updates: {needs_update}")
        else:
            print(f"🔄 Files updated: {summary['updated']}")
            print(f"✓ Files not needing updates: {summary['no_update_needed']}")
            print(f"⚠️ Files failing quality check: {summary['update_failed']}")
    else:
        print(f"❌ Error: {result.get('message', 'Unknown error')}")
    
    print("=" * 60)
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the MCP educational materials multi-agent system")
    parser.add_argument("--check-only", action="store_true", help="Only check documents without updating them")
    parser.add_argument("--target", type=str, help="Process a specific markdown file")
    args = parser.parse_args()
    
    asyncio.run(main(args))