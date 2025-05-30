from agents import Agent
from tools import list_files, read_file, check_freshness_and_accuracy, write_file

@Agent(name="qa")
async def qa(state: dict):
    """Runs freshness/accuracy check; fixes trivial issues automatically."""
    md_paths = await list_files.search("docs/**/*.md")
    for p in md_paths:
        md = await read_file.read(p)
        verdict = await check_freshness_and_accuracy(md, [])
        if verdict.startswith("needs_revision"):
            note = f"\n> **NOTE (auto‑qa):** {verdict.split(':',1)[1]}\n"
            await write_file.write(p, md + note, overwrite=True)
    return state