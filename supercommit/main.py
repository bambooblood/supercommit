import typer
from typing import Annotated, Optional
import requests

from supercommit.config import cfg
from supercommit.utils import (
    get_current_branch,
    get_diff,
    get_repo,
    has_changes,
    show_changes,
    stage_changes,
    commit_changes,
    push_branch,
    generate_commit_message,
    version_callback,
)

app = typer.Typer()

config = cfg


def exit(message: str, code=0):
    typer.echo(message)
    raise typer.Exit(code=code)


@app.command()
def run(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", "-v", help="Package version", callback=version_callback
        ),
    ] = None,
    force: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    path = "."
    repo = get_repo(path)
    current_branch = get_current_branch(repo)

    if not has_changes(repo):
        exit("✅ No changes to commit.")

    show_changes(repo)

    if not force and not typer.confirm(
        text="Do you want to commit those changes?", default=True
    ):
        exit("✅ No changes will be committed.")

    try:
        message = generate_commit_message(diff_text=get_diff(repo), config=config)
    except requests.ConnectionError as e:
        exit(
            f"ConnectionError: Unable to connect with Ollama server. Ensure Ollama is up and running '{cfg["model"]}' model",
            1,
        )

    typer.echo(f"📝 Suggested commit message: '{message}'")

    if not typer.confirm(text="Use this message?", default=True):
        message = typer.prompt("Enter your own commit message:")

    typer.echo(f"✍️ Commit message: '{message}'")

    stage_changes(repo)
    commit_changes(repo, message)

    if not force and not typer.confirm(text="Push commit to remote?", default=True):
        exit("✅ Commit will not be pushed to remote")

    push_branch(repo, current_branch)


def main():
    app()
