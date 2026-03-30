# Integrations

## Planned External Integrations

### Telegram Bot API

- Purpose: Receive text and voice captures from one authorized user
- Interface: `python-telegram-bot` long polling
- Risk: Authorization mistakes or unsupported update types

### Google Gemini API

- Purpose: Transcribe voice notes and classify capture routing
- Interface: `google-genai`
- Risk: Response shape drift, network failures, and cost/latency concerns

### Obsidian Vault Filesystem

- Purpose: Persist daily notes and capture log
- Interface: Direct file reads/writes via Python filesystem APIs
- Risk: Path mismatches between Windows and WSL, concurrent manual edits

## Local Environment Dependencies

- WSL2 Linux distro with Python 3.11+
- Vault path visible from WSL
- Environment variables loaded from `.env`
