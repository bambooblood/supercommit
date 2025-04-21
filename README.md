# SuperCommit

SuperCommit is an utility that helps you quickly commiting your changes, using LLMs for auto-generating meaningful commit messages based on your changes.

## Requirements

[Ollama](https://ollama.com/) must be running. By default we use "qwen2.5-coder:0.5b"

## Usage

```bash
pip install git+https://github.com/bambooblood/supercommit.git
```

```bash
supercommit --version
```

Output:

```bash
SuperCommit 0.1.0
```

If your Ollama Server is running on a different machine or you just want to experiment with another Ollama model:

```bash
export SUPERCOMMIT_OLLAMA_SERVER=http://localhost:11434
export SUPERCOMMIT_OLLAMA_MODEL=llama3.2:1b
```

### Args

```bash
supercommit --version
```

```bash
supercommit --path path/to/your/repo
```

## Contributing

```bash
pip install -e .
```

```
supercommit
```
