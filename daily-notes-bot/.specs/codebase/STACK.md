# Tech Stack

**Analyzed:** 2026-03-30

## Core

- Framework: Not implemented yet; target framework is `python-telegram-bot`
- Language: Not implemented yet; target language is Python 3.13
- Runtime: WSL2 Linux environment expected
- Package manager: Not implemented yet; target toolchain is `uv` with `pyproject.toml` and `uv.lock`

## Frontend

- Not applicable

## Backend

- API Style: Not applicable; Telegram bot with long polling
- Database: None; filesystem-backed Obsidian vault
- Authentication: Telegram user ID allowlist

## Testing

- Unit: Not implemented yet
- Integration: Not implemented yet
- E2E: Not implemented yet

## External Services

- Messaging: Telegram Bot API
- AI: Google Gemini API for audio transcription and capture routing
- Filesystem: Obsidian vault directory

## Development Tools

- Source control: Git
- Environment and secrets management: process environment as the runtime contract, with optional `.env` loading for local WSL development only

## Recommended Baseline

- Default Python target: `3.13`
- Minimum compatibility floor: `3.11`
- Project metadata and dependencies: `pyproject.toml`
- Locked dependency resolution: `uv.lock`
- Common commands: `uv sync`, `uv run`, `uv python install 3.13`
