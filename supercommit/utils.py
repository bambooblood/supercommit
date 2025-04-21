import requests
import os

model = "gemma3:1b"
SERVER = os.getenv("SUPERCOMMIT_OLLAMA_SERVER", "http://localhost:11434")
MODEL = os.getenv("SUPERCOMMIT_OLLAMA_MODEL", model)


def ollama_generate(prompt: str) -> str:
    response = requests.post(
        f"{SERVER}/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
    )

    if response.status_code == 200:
        result = response.json()
        return result.get("response", "").strip()
    else:
        return "None"


def truncate_git_diff(diff_text: str, MAX_DIFF_LINES=200):
    trimmed = diff_text

    diff_lines = diff_text.splitlines()

    if len(diff_lines) > MAX_DIFF_LINES:
        trimmed = "\n".join(diff_lines[:MAX_DIFF_LINES])
        trimmed += "\n... [diff truncated]"

    return trimmed


def summarise_git_diff(diff_text: str) -> str:
    prompt = f"""
    You are an AI assistant that summarizes Git diffs into bullet points.

    Given the following git diff, write a concise summary of the changes in plain English. Focus on what was changed and why (if it’s clear). Group related changes together and omit low-level syntax details.

    Format the summary as a short bullet list. Use past tense.

    Git diff:
    \"\"\"
    {diff_text}
    \"\"\"

    Summary:
    """

    return ollama_generate(prompt)


def generate_commit_message(diff_text: str) -> str:
    prompt = f"""
    You are an assistant that writes a single, concise Git commit message.

    Use the summary below to generate **one** short commit message in the **imperative mood** (e.g., "Add", "Fix", "Refactor"). Follow **conventional commit format** when appropriate (e.g., "feat:", "fix:", "chore:").

    Respond with **only the commit message**, nothing else.

    Summary:
    \"\"\"
    {summarise_git_diff(diff_text)}
    \"\"\"

    Commit message:
    """

    return ollama_generate(prompt)
