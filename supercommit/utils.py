import requests
import os

# model = "llama3.2:1b"
model = "gemma3:1b"
SERVER = os.getenv("SUPERCOMMIT_OLLAMA_SERVER", "http://localhost:11434")
MODEL = os.getenv("SUPERCOMMIT_OLLAMA_MODEL", model)


def generate_commit_message_with_ollama(diff_text: str) -> str:
    summary_prompt = f"""
    You're a Senior Software Developer.

    [TASK]
    Your task is to understand the given git diff and generate a brief summary explaining what have been changed.
    
    [GIT DIFF]
    {diff_text}
    """

    response = requests.post(
        f"{SERVER}/api/generate",
        json={"model": MODEL, "prompt": summary_prompt, "stream": False},
    )

    changes = "None"

    if response.status_code == 200:
        result = response.json()
        changes = result.get("response", "").strip()

    prompt = f""""
    You are a Senior Software Developer.
    
    [EXPLAINED CHANGES]
    {changes}

    [YOUR TASK]
    Your task is to generate a CONCISE commit message briefly explaining the changes implemented on the codebase.

    [OUTPUT]
    - ONLY 1 commit message in 1 sentence following SEMANTIC COMMIT format.
    - Respond ONLY with the suggested message. You MUST avoid any other kind of comments.

    [EXAMPLE]
    chore: add image drawing functionality based on text input
    """

    response = requests.post(
        f"{SERVER}/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
    )

    if response.status_code == 200:
        result = response.json()
        return result.get("response", "").strip()
    else:
        return "None"
