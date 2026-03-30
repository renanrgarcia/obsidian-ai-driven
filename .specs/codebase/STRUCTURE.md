# Structure

**Analyzed:** 2026-03-29

## Current Repository Layout

- `README.md`
- `.spec/features/telegram-obsidian-journal/spec.md`
- `.specs/` (planned by this work for project and feature planning)

## Planned Implementation Layout

- `bot.py` - entrypoint and orchestration
- `requirements.txt` - runtime dependencies
- `.env.example` - required and optional configuration
- `.gitignore` - local environment and temp file exclusions
- `README.md` - project overview
- `SETUP.md` - WSL setup and operations guide
- `tests/` - note engine and capture flow tests

## Planned Test Layout

- `tests/test_daily_note_writer.py`
- `tests/test_capture_log.py`
- `tests/test_routing.py`
