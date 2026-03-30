# Obsidian AI Driven

**Vision:** Build a private Telegram-to-Obsidian capture bot that can reliably turn text and voice messages into structured daily note updates inside your personal vault, starting with a simple local WSL deployment and evolving into a VPS-capable architecture without losing the local fallback path.
**For:** A single personal user managing notes, tasks, and habits in Obsidian.
**Solves:** Fast capture from Telegram into Obsidian without manual copy/paste, while preserving structure, history, and low-friction local operation.

## Goals

- Deliver a working v1 bot that accepts messages from one authorized Telegram user and writes them into the correct sections of the daily note template in WSL with repeatable local startup steps.
- Preserve every capture in an audit log and keep daily note updates deterministic enough to trust for everyday personal use.
- Keep the codebase small and understandable so future deployment to a VPS is an incremental operational step rather than a rewrite.
- Preserve WSL as a documented fallback and regression runtime even after a future VPS deployment exists.

## Tech Stack

**Core:**

- Framework: `python-telegram-bot` with long polling
- Language: Python 3.13 target, Python 3.11+ compatibility floor
- Runtime: WSL2 Linux environment on a Windows host in v1, with a future VPS runtime option
- Package management: `uv` with `pyproject.toml` and `uv.lock`
- Storage: Obsidian vault files on disk

**Key dependencies:**

- `python-telegram-bot`
- `google-genai`
- `python-dotenv`
- Python standard library (`pathlib`, `logging`, `tempfile`, `zoneinfo`)

## Secrets Strategy

- V1 local WSL: `.env` is acceptable as a local-only convenience layer because the machine is both the dev box and the runtime.
- V2 VPS Git hub: keep bot secrets off the VPS Git host if it is only serving as the primary Git remote.
- V2.1 GitHub mirror: use repository-managed secrets or a dedicated deploy key for mirror automation, not a checked-in credential file.
- V3 VPS bot runtime: prefer host-managed secret injection; free options come first, such as a root-owned env file outside the repo or `pass` + GPG, with managed secret stores as a later upgrade path.

## Scope

**v1 includes:**

- Telegram text and voice capture for one authorized user
- Daily note creation from a fixed template containing `Notes`, `Tasks`, and `Habits`
- AI routing of captures into note entries, new tasks, or habit completion updates
- Carry-forward of unfinished tasks from the previous day when creating a new note
- Reverse-chronological `capture-log.md` audit trail
- Setup instructions for running continuously inside WSL
- Deployment planning for a later VPS-hosted Git remote and mirrored backup topology
- Documentation that keeps both WSL and VPS runtime paths available on demand

**Explicitly out of scope:**

- Multi-user support or group chats
- Photos, files, stickers, or edited-message reconciliation
- Rich Obsidian plugin integration or direct API integration
- Cloud deployment automation in v1
- Habit creation from free-form messages

## Constraints

- Timeline: Optimize for first usable version before adding polish or automation.
- Technical: Must work well in WSL2 with a filesystem-backed Obsidian vault and minimal moving parts, and must remain portable to a VPS-hosted runtime later.
- Security: Keep the runtime configuration environment-based so secrets can move from local `.env` to host-managed injection without code-path churn.
- Resources: Personal project, first WSL deployment, so setup and recovery steps must stay simple.
