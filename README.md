# SuperCommit

SuperCommit is an utility that helps you quickly commiting your changes, using LLMs for auto-generating meaningful commit messages based on your changes.

## Requirements

[Ollama](https://ollama.com/) must be running. By default we use ""gemma3:latest""

## Usage

```bash
pip install git+https://github.com/bambooblood/supercommit.git
```

```bash
supercommit --version
#[Output] SuperCommit 1.0.0
```

Try it in your repo! Make some changes and let the magic of supercommit commit it for you:

```bash
supercommit -y
```

`-y` command will try to commit all changes and push it to remote, but it will ask for your confirmation about the generated commit message.

### Config

If your Ollama Server is running on a different machine or you just want to experiment with another Ollama model:

```bash
export SUPERCOMMIT_OLLAMA_SERVER=http://localhost:11434
export SUPERCOMMIT_OLLAMA_MODEL=llama3.2:1b
```

Or you can create a `~/.config/supercommit.toml` file:

```toml
# ~/.config/supercommit.toml

# Which model to use for commit‑message generation
provider = "ollama"
server = "http://localhost:11434"
model = "gemma3:latest"

# Commit‑message style
[conventional]
enabled = true
types = ["feat","fix","docs","chore"]

# Gitmoji support
[gitmoji]
enabled = true
```

### Args

```bash
supercommit --version
```

```bash
supercommit --yes
```

## Development

```bash
pip install -e .
```
