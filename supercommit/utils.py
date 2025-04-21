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


def summarise_git_diff(diff_text: str) -> str:
    prompt = f"""
    Summarize this git diff in plain English:

    {diff_text}
    """

    return ollama_generate(prompt)


def generate_commit_message(diff_text: str) -> str:
    prompt = f""""
    Generate JUST one concise conventional commit message based on this summary:

    {summarise_git_diff(diff_text)}
    """

    return ollama_generate(prompt)
