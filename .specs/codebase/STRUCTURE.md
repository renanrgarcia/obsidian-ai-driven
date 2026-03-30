# Structure

**Analyzed:** 2026-03-30

## Current Repository Layout

- `README.md`
- `.spec/features/telegram-obsidian-journal/spec.md`
- `.specs/` (planned by this work for project and feature planning)

## Planned Implementation Layout

- `bot.py` - entrypoint and orchestration
- `pyproject.toml` - project metadata and runtime dependencies
- `uv.lock` - locked dependency graph for reproducible installs
- `.env.example` - required and optional configuration
- `.gitignore` - local environment and temp file exclusions
- `README.md` - project overview
- `SETUP.md` - WSL setup and operations guide
- `tests/` - note engine and capture flow tests

## Planned Test Layout

- `tests/test_daily_note_writer.py`
- `tests/test_capture_log.py`
- `tests/test_routing.py`
