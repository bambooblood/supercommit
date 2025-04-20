from typing import Annotated, Optional
import typer
from git import Repo, GitCommandError
from datetime import datetime

from supercommit.utils import generate_commit_message_with_ollama

app = typer.Typer()

__version__ = "0.1.0"


def version_callback(value: bool):
    if value:
        print(f"supercommit: v{__version__}")
        raise typer.Exit()


def get_current_branch(repo):
    return repo.active_branch.name


def create_new_branch(repo):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    new_branch = f"work-{timestamp}"
    repo.git.checkout("-b", new_branch)
    typer.echo(f"🔀 Switched to new branch: {new_branch}")
    return new_branch


def stage_changes(repo):
    repo.git.add("--all")


def has_changes(repo):
    return repo.is_dirty(untracked_files=True)


def show_diff(repo):
    diff = repo.git.diff("HEAD")
    typer.echo("📄 Diff with last commit:\n")
    typer.echo(diff)


def generate_commit_message(repo):
    diff = repo.git.diff("HEAD")
    if not diff.strip():
        return "Update without code changes"
    return generate_commit_message_with_ollama(diff)


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
        Optional[bool], typer.Option("--version", callback=version_callback)
    ] = None,
    path=".",
):
    repo = Repo(path)
    current_branch = get_current_branch(repo)
    if current_branch in ["main", "master"]:
        if typer.confirm(
            text=f"You are in {current_branch}, do you want to automatically create a new branch?",
            default=True,
        ):
            current_branch = create_new_branch(repo)

    if not has_changes(repo):
        typer.echo("✅ No changes to commit.")
        raise typer.Exit()

    stage_changes(repo)
    # show_diff(repo)

    message = generate_commit_message(repo)
    typer.echo(f"📝 Suggested commit message:\n{message}")

    if not typer.confirm(text="Use this message?", default=True):
        message = typer.prompt("Enter your own commit message")

    typer.echo(f"✍️ Commit message: {message}")

    commit_changes(repo, message)

    if typer.confirm(text="Push commit?", default=True):
        push_branch(repo, current_branch)


def main():
    app()


if __name__ == "__main__":
    app()
