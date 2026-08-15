# Local AI Code Reviewer

A fully offline, zero-cost AI code review tool. Runs entirely on your own machine using [Ollama](https://ollama.com) and a local LLM (Qwen2.5 7B) — no API keys, no internet required after setup, no per-request cost.

## What it does

Point it at any codebase and it reviews each file for:
- Bugs
- Security vulnerabilities (hardcoded secrets, unsafe patterns, etc.)
- Bad practices
- Readability issues

Outputs a structured Markdown report with severity-ranked findings and suggestions per file.

## Why local, not an API

- **Zero cost** — no OpenAI/Anthropic API billing, runs on your own GPU
- **Privacy** — your code never leaves your machine, useful for proprietary/sensitive codebases
- **No rate limits** — review as many files as you want

## Tech stack

- Python
- [Ollama](https://ollama.com) running `qwen2.5:7b` locally
- No cloud dependencies

## Setup

```bash
pip install ollama
ollama pull qwen2.5:7b
```

## Usage

```bash
python reviewer.py path/to/your/project
```

Generates `review_report.md` with findings for every code file in the folder.

## Sample output

See [`sample_report.md`](./sample_report.md) — a real review run against a production React/Supabase codebase.

## Roadmap

- [ ] Support for more languages/extensions
- [ ] Severity-based exit codes for CI/CD integration
- [ ] HTML report export
