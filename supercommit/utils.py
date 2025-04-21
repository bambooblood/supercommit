from supercommit.ollama import generate
from supercommit.config import cfg


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


def generate_commit_message(diff_text: str, config=cfg) -> str:
    model = config["model"]
    server = config["server"]

    summary_prompt = get_summary_prompt(diff=diff_text)

    summary = generate(prompt=summary_prompt, model=model, server=server)

    commit_message_prompt = get_commit_message_prompt(summary=summary)

    commit_message = generate(prompt=commit_message_prompt, model=model, server=server)

    return commit_message
