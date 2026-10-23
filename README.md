# AI-Agent-Python

A command-line AI coding agent built in Python. You give it a task in plain English, and it decides which tools to use to inspect, edit, and run code until the task is done.

It uses **tool calling** (function calling) through the OpenAI Python SDK, connected to **OpenRouter**, so it can run on free models with no paid API required.

> Built as part of the [Boot.dev](https://www.boot.dev) "Build an AI Agent in Python" project, a toy version of tools like Claude Code or Cursor.

## What it does

1. Receives a coding task as a command-line argument.
2. Sends the task to an LLM together with a set of tool definitions.
3. The model chooses which tool to call, the program executes it, and the result goes back to the model.
4. The loop repeats until the model gives a final answer.

### Tools available to the agent

| Tool | What it does |
| --- | --- |
| `get_files_info` | Lists files and directories, with sizes |
| `get_file_content` | Reads the contents of a file |
| `write_file` | Creates or overwrites a file |
| `run_python_file` | Executes a Python file and returns its output |

## Example

The repo includes a small calculator app (`calculator/`) that I use as a test target. I asked the agent to fix a bug in the operator precedence:

```bash
uv run main.py "run calculator/main.py with 3 + 7 * 2 and fix the bug: it should return 17, not 20"
```

The agent reads the code, finds the problem, edits the file, and runs the calculator again to verify the result, all on its own.

## Getting started

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A free [OpenRouter](https://openrouter.ai/) API key
- A Unix-like shell (bash, zsh)

### Setup

```bash
git clone https://github.com/joseequiroz26-cmd/AI-Agent-Python.git
cd AI-Agent-Python
uv sync
```

Create a `.env` file in the project root with your key:

```
OPENROUTER_API_KEY=your_key_here
```

The `.env` file is listed in `.gitignore` and should never be committed.

### Run

```bash
uv run main.py "your coding task here"
```

## Project structure

```
.
├── main.py                  # CLI entry point and agent loop
├── functions/               # Tool implementations and their schemas
├── calculator/              # Sample app the agent works on
├── test_get_files_info.py
├── test_get_file_content.py
├── test_write_file.py
├── test_run_python_file.py
└── pyproject.toml
```

## Tests

Each tool has its own test script:

```bash
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_write_file.py
uv run test_run_python_file.py
```

## Tech stack

- Python
- OpenAI Python SDK (pointed at OpenRouter)
- uv for dependency and environment management

## Limitations

- The free OpenRouter tier is rate-limited, so long tasks may hit the daily request limit.
- Free models vary in quality; the agent can fail or loop on complex tasks.
- This is a learning project: it can write files and execute code, so only run it on code you are comfortable letting it modify.

## What I learned

- How agentic tools work under the hood: the model never touches files directly, it only requests tool calls that the program executes.
- Designing tool schemas and handling function calls in an LLM loop.
- Structuring a multi-directory Python project and writing tests for each module.
