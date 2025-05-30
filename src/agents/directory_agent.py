from agents import Agent
from tools import list_files, read_file

@Agent(name="directory_audit")
async def directory_audit(state: dict):
    """Scans docs/ tree and gathers meta info."""
    files = await list_files.search("docs/**/*.md")
    state["existing_docs"] = files
    # simple metadata (first heading) for gap analysis
    meta = {}
    for path in files:
        content = await read_file.read(path)
        first_line = content.split("\n", 1)[0].lstrip("# ")
        meta[path] = first_line
    state["doc_meta"] = meta
    return state