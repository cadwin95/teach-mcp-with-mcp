from agents import Agent
from agents.hosted.local_shell import LocalShellTool

shell = LocalShellTool()

git_cmds = [
    "git add docs",
    "git commit -m 'auto: update docs' || echo 'no changes'",
    "git push origin gh-pages",
]

@Agent(name="builder")
async def builder(state: dict):
    """Commits + pushes docs to trigger GitHub Pages build."""
    for cmd in git_cmds:
        await shell.execute(cmd)
    return state