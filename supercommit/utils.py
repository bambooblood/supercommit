import typer
import toml, os
from rich.console import Console
from rich.spinner import Spinner
from git import GitCommandError, Repo

from supercommit.ollama import generate


pyproject = {"project": {"version": "0.2.6-alpha"}}
pyproject_path = os.path.join(os.getcwd(), "pyproject.toml")

if os.path.exists(pyproject_path):
    pyproject.update(toml.load(pyproject_path))

console = Console()

__version__ = pyproject["project"].get("version")


def version_callback(value: bool) -> None:
    if value:
        print(f"SuperCommit {__version__}")
        raise typer.Exit()


def get_repo(path: str) -> Repo:
    return Repo(path)


def get_current_branch(repo: Repo):
    return repo.active_branch.name


def stage_changes(repo: Repo):
    repo.git.add("--all")


def has_changes(repo: Repo):
    return repo.is_dirty(untracked_files=True)


def show_changes(repo: Repo):
    status = repo.git.status()
    typer.echo("📄 Status:\n")
    typer.echo(status)


def show_diff(repo: Repo, staged: bool = False):
    args = ["HEAD"]
    if staged:
        args.insert(0, "--staged")
    diff = repo.git.diff(*args)
    typer.echo("🔀 Diff with last commit:\n")
    typer.echo(diff)


def get_diff(repo: Repo, staged: bool = False) -> str:
    try:
        args = ["HEAD"]
        if staged:
            args.insert(0, "--staged")
        return repo.git.diff(*args)
    except GitCommandError as e:
        return "No diff"


def commit_changes(repo: Repo, message: str) -> None:
    try:
        commit = repo.index.commit(message)
        typer.echo(f"✅ Your changes've been committed ({commit.hexsha})")
    except GitCommandError as e:
        typer.echo(f"⚠️ Commit failed: {e}", err=True)


def push_branch(repo: Repo, branch: str) -> None:
    try:
        repo.git.push("--set-upstream", "origin", branch)
        typer.echo(f"🚀 Pushed branch {branch} to origin.")
    except GitCommandError as e:
        typer.echo(f"⚠️ Push failed: {e}", err=True)


def get_summary_prompt(diff: str):
    return f"""
    You are an AI assistant that summarizes Git diffs into bullet points.

    Given the following git diff, write a concise summary of the changes in plain English. Focus on what was changed and why (if it’s clear). Group related changes together and omit low-level syntax details.

    Format the summary as a short bullet list. Use past tense.

    Git diff:
    \"\"\"
    {diff}
    \"\"\"

    Summary:
    """


def get_commit_message_prompt(summary: str):
    return f"""
    You are an assistant that writes a single, concise Git commit message.

    Use the summary below to generate **one** short commit message in the **imperative mood** (e.g., "Add", "Fix", "Refactor"). Follow **conventional commit format** when appropriate (e.g., "feat:", "fix:", "chore:").

    Respond with **only the commit message**, nothing else.

    Summary:
    \"\"\"
    {summary}
    \"\"\"

    Commit message:
    """


def generate_commit_message(diff_text: str, config: dict) -> str:
    with console.status("Generating a meaningful commit message...", spinner="monkey"):
        model = config["model"]
        server = config["server"]
        diff = truncate(text=diff_text)

        summary_prompt = get_summary_prompt(diff=diff)

        summary = generate(prompt=summary_prompt, model=model, server=server)

        commit_message_prompt = get_commit_message_prompt(summary=summary)

        commit_message = generate(
            prompt=commit_message_prompt, model=model, server=server
        )

        return commit_message


def truncate(text: str, MAX_LINES=200):
    lines = text.splitlines()

    if len(lines) > MAX_LINES:
        trimmed = "\n".join(lines[:MAX_LINES])
        trimmed += "\n... [diff truncated]"
        typer.echo(
            f"⚠️ Large diff detected — considering only the first {str(MAX_LINES)} lines"
        )
    else:
        trimmed = text

    return trimmed
