# smart-todo

An AI-driven todo list. The project will use AI to help turn natural-language
input into useful tasks while remaining fully usable when no LLM API key is
configured.

Phase 0 provides the Python project skeleton and developer tooling. The
generated command is currently a placeholder; todo functionality belongs to a
later phase.

## Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- `make`

## Setup

Clone the repository and install the locked development environment:

```console
git clone https://github.com/cv-gh/smart-todo-v1.git
cd smart-todo-v1
uv sync --locked --dev
```

For local configuration, copy the example file:

```console
cp .env.example .env
```

## Run

Verify the installed placeholder command:

```console
uv run smart-todo
```

The interactive application will be introduced in Phase 1.

## Test and quality checks

Run linting, formatting checks, static type checks, and tests with one command:

```console
make check
```

The individual commands are:

```console
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
```

## Configuration

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `LLM_API_KEY` | No | unset | Reserved for optional LLM integration in a later phase. |

Do not commit `.env`; it is ignored by Git. The application will work without
an LLM API key.
