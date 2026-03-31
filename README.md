# obsidian-ai-driven

Umbrella repository for Obsidian-related automation projects.

## Projects

### `daily-notes-bot`

Private Telegram-to-Obsidian bot that writes captures into daily notes and mirrors them into `capture-log.md`.

- App docs: [daily-notes-bot/README.md](/C:/Users/renan/.codex/worktrees/60a2/obsidian-ai-driven/daily-notes-bot/README.md)
- WSL setup: [daily-notes-bot/SETUP.md](/C:/Users/renan/.codex/worktrees/60a2/obsidian-ai-driven/daily-notes-bot/SETUP.md)

## Repository Shape

Each project in this umbrella repo lives in its own top-level subdirectory.

```text
obsidian-ai-driven/
  README.md
  daily-notes-bot/
  future-project/
```

## WSL Runtime Model

Development clones and runtime clones are intentionally separate.

```text
~/projects/
  obsidian-ai-driven/
    daily-notes-bot/   # development clone, branch: develop

~/apps/
  obsidian-ai-driven/
    daily-notes-bot/   # runtime clone, branch: main
  venvs/
    daily-notes-bot/
  env/
    daily-notes-bot.env
```

## Branch Responsibilities

- `develop`: active development branch in `~/projects/obsidian-ai-driven/...`
- `main`: runtime and deployment branch in `~/apps/obsidian-ai-driven/...`

If `develop` does not exist yet, create it from `main` in the development clone.
