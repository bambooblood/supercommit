import toml, os, argparse

cfg = {"provider": "ollama", "server": "http://localhost:11434", "model": "gemma3:1b"}

user_cfg_path = os.path.expanduser("~/.config/supercommit.toml")

if os.path.exists(user_cfg_path):
    cfg.update(toml.load(user_cfg_path))

repo_cfg_path = os.path.join(os.getcwd(), "supercommit.toml")

if os.path.exists(repo_cfg_path):
    cfg.update(toml.load(repo_cfg_path))

if os.getenv("SUPERCOMMIT_OLLAMA_SERVER"):
    cfg["server"] = os.getenv("SUPERCOMMIT_OLLAMA_SERVER")

if os.getenv("SUPERCOMMIT_OLLAMA_MODEL"):
    cfg["model"] = os.getenv("SUPERCOMMIT_OLLAMA_MODEL")

# TODO: argparse
