import requests


def generate(prompt: str, model: str, server: str) -> str:
    response = requests.post(
        f"{server}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
    )

    # TODO: Catch potential errors

    if response.status_code == 200:
        result = response.json()
        return result.get("response", "").strip()
    else:
        return "None"
