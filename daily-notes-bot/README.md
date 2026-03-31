# daily-notes-bot

Telegram-to-Obsidian bot for updating daily notes and mirroring captures into `capture-log.md`.

## What This Project Contains

- `daily_notes_bot/`: Python package
- `tests/`: automated tests
- `SETUP.md`: WSL setup and runtime workflow
- `.specs/`: project and feature planning docs

## Development Clone vs Runtime Clone

This project is intended to exist in two WSL locations at the same time.

### Development clone

Path:

```text
~/projects/obsidian-ai-driven/daily-notes-bot
```

Use it for:

- coding
- tests
- commits
- working on `develop`

### Runtime clone

Path:

```text
~/apps/obsidian-ai-driven/daily-notes-bot
```

Use it for:

- manual runtime validation
- production-like execution
- staying on `main`

### Runtime virtual environment

Path:

```text
~/apps/venvs/daily-notes-bot
```

This keeps the runtime Python environment outside the repo, which is closer to how a VPS setup should look.

### Runtime env file

Path:

```text
~/apps/env/daily-notes-bot.env
```

Keep secrets there instead of inside the repo.

## Branch Expectations

- Development clone: `develop`
- Runtime clone: `main`

If `develop` does not exist yet, create it from `main`:

```bash
git switch main
git switch -c develop
```

## uv Workflow

### `uv venv`

Creates a virtual environment.

Example:

```bash
uv venv ~/apps/venvs/daily-notes-bot
```

### `uv lock`

Resolves dependencies and writes `uv.lock`.

### `uv sync`

Installs exactly what is declared by `uv.lock`.

### `uv sync --extra dev`

Installs the locked dependencies plus the `dev` dependency group, such as `pytest`.

### `uv sync --active`

Installs dependencies into the currently activated virtual environment. This is the right command when the virtual environment lives outside the project directory.

### `uv run daily-notes-bot`

Runs the app entrypoint defined in `pyproject.toml`.

## `pyproject.toml` and `uv.lock`

### `pyproject.toml`

The project definition file. It declares:

- project metadata
- Python version requirements
- runtime dependencies
- dev dependencies
- tool settings

### `uv.lock`

The lockfile. It pins the exact dependency versions that should be installed, so environments are reproducible.

## Recommended Commands

Development clone:

```bash
cd ~/projects/obsidian-ai-driven/daily-notes-bot
uv sync --extra dev
pytest
```

Runtime clone:

```bash
source ~/apps/venvs/daily-notes-bot/bin/activate
cd ~/apps/obsidian-ai-driven/daily-notes-bot
uv sync --active
set -a
source ~/apps/env/daily-notes-bot.env
set +a
uv run daily-notes-bot
```

See [SETUP.md](/C:/Users/renan/.codex/worktrees/60a2/obsidian-ai-driven/daily-notes-bot/SETUP.md) for the full WSL setup workflow.
