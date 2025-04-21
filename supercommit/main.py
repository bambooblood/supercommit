import typer
from rich.console import Console
from rich.spinner import Spinner
from git import Repo, GitCommandError
from typing import Annotated, Optional

from supercommit.utils import generate_commit_message

app = typer.Typer()
console = Console()

__version__ = "0.1.0-alpha"


def version_callback(value: bool):
    if value:
        print(f"SuperCommit {__version__}")
        raise typer.Exit()


def get_current_branch(repo):
    return repo.active_branch.name


def stage_changes(repo):
    repo.git.add("--all")


def has_changes(repo):
    return repo.is_dirty(untracked_files=True)


def show_changes(repo):
    status = repo.git.status()
    typer.echo("📄 Status:\n")
    typer.echo(status)


def show_diff(repo):
    diff = repo.git.diff("HEAD")
    typer.echo("🔀 Diff with last commit:\n")
    typer.echo(diff)


def get_commit_message(repo):
    # TODO: Handle potential unexistent ref. Example, first commit
    diff = repo.git.diff("HEAD")
    if not diff.strip():
        return "Update without code changes"
    # TODO: Handle potential too large payload and avoid LLM context window broken down
    with console.status("Generating a meaningful commit message...", spinner="monkey"):
        return generate_commit_message(diff)


def commit_changes(repo, message):
    repo.index.commit(message)


def push_branch(repo, branch):
    try:
        repo.git.push("--set-upstream", "origin", branch)
        typer.echo(f"🚀 Pushed branch {branch} to origin.")
    except GitCommandError as e:
        typer.echo(f"⚠️ Push failed: {e}", err=True)


@app.command()
def run(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version, -v", help="Package version", callback=version_callback
        ),
    ] = None,
    force: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
    path: str = typer.Option(".", help="Repository path"),
):
    repo = Repo(path)
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

    stage_changes(repo)

    message = get_commit_message(repo)
    typer.echo(f"📝 Suggested commit message: '{message}'")

    if not force and not typer.confirm(text="Use this message?", default=True):
        message = typer.prompt("Enter your own commit message:")

    typer.echo(f"✍️ Commit message: '{message}'")

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
