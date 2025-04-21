import requests
import os

model = "llama3.2:1b"
# model = "qwen2.5:0.5b"
SERVER = os.getenv("SUPERCOMMIT_OLLAMA_SERVER", "http://localhost:11434")
MODEL = os.getenv("SUPERCOMMIT_OLLAMA_MODEL", model)


def generate_commit_message_with_ollama(diff_text: str) -> str:
    prompt = f""""
    You are a Senior Software Engineer.
    
    [CHANGES ON CODEBASE]
    {diff_text}

    [YOUR TASK]
    Your task is to generate a CONCISE and SUMMARISED commit message explaining the implemented changes on the codebase.

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
