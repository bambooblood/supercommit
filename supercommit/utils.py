import typer
from rich.console import Console
from rich.spinner import Spinner

from supercommit.ollama import generate

console = Console()

__version__ = "0.1.0-alpha"


def version_callback(value: bool):
    if value:
        print(f"SuperCommit {__version__}")
        raise typer.Exit()


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
