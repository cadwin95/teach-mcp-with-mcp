from agents import Agent

@Agent(name="gap_analysis")
async def gap_analysis(state: dict):
    """Determines which docs are missing for the given topic."""
    topic = state["topic"].lower()
    existing = [m.lower() for m in state["doc_meta"].values()]
    if topic not in existing:
        state.setdefault("todo", []).append({
            "filename": f"{topic.replace(' ', '-')}.md",
            "title": state["topic"],
        })
    return state