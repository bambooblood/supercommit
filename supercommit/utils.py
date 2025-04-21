import requests
import os

model = "llama3.2:1b"
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
    You're a Senior Software Developer.

    [TASK]
    Your task is to understand the given git diff and generate a brief summary explaining what have been changed.
    
    [GIT DIFF]
    {diff_text}
    """

    return ollama_generate(prompt)


def generate_commit_message(diff_text: str) -> str:
    prompt = f""""
    You are a Senior Software Developer.
    
    [EXPLAINED CHANGES]
    {summarise_git_diff(diff_text)}

    [YOUR TASK]
    Your task is to generate a CONCISE commit message briefly explaining the changes implemented on the codebase.

    [OUTPUT]
    - ONLY 1 commit message in 1 sentence following SEMANTIC COMMIT format.
    - Respond ONLY with the suggested message. You MUST avoid any other kind of comments.

    [EXAMPLE]
    chore: add image drawing functionality based on text input
    """

    return ollama_generate(prompt)
