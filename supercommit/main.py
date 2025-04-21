import typer
from rich.console import Console
from rich.spinner import Spinner
from typing import Annotated, Optional

from supercommit.utils import generate_commit_message, version_callback
from supercommit.config import cfg
from supercommit.git import (
    get_current_branch,
    get_diff,
    get_repo,
    has_changes,
    show_changes,
    stage_changes,
    commit_changes,
    push_branch,
)

app = typer.Typer()

config = cfg


@app.command()
def run(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", "-v", help="Package version", callback=version_callback
        ),
    ] = None,
    force: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
    path: str = typer.Option(".", help="Repository path"),
):
    repo = get_repo(path)
    current_branch = get_current_branch(repo)

    if not has_changes(repo):
        typer.echo("✅ No changes to commit.")
        raise typer.Exit()

    show_changes(repo)

    if not force and not typer.confirm(
        text="Do you want to commit those changes?", default=True
    ):
        typer.echo("✅ No changes will be committed.")
        raise typer.Exit()

    diff = get_diff(repo)
    message = generate_commit_message(diff, config=config)
    typer.echo(f"📝 Suggested commit message: '{message}'")

    if not typer.confirm(text="Use this message?", default=True):
        message = typer.prompt("Enter your own commit message:")

    typer.echo(f"✍️ Commit message: '{message}'")

    stage_changes(repo)
    commit_changes(repo, message)

    typer.echo("✅ Your changes've been committed!")

    if not force and not typer.confirm(text="Push commit to remote?", default=True):
        typer.echo("✅ Commit will not be pushed to remote")
        raise typer.Exit()

    push_branch(repo, current_branch)

    typer.echo("✅ Commit pushed to remote")


def main():
    app()


if __name__ == "__main__":
    app()
