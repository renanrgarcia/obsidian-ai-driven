# Telegram Obsidian Daily Bot Design

**Spec:** `.specs/features/telegram-obsidian-daily-bot/spec.md`

## Implementation Shape

Start with a single `bot.py` file, but enforce internal separation with small functions and typed helper structures.

## Components

### 1. Configuration Loader

- Reads required env vars from the process environment and can optionally hydrate them from `.env` in local WSL development.
- Resolves WSL-friendly filesystem paths.
- Validates required configuration on startup.

### 2. Telegram Entrypoint

- Registers text and voice handlers.
- Rejects unauthorized users early.
- Delegates business logic to helper functions.

### 3. Capture Normalizer

- Converts Telegram updates into a normalized capture object.
- Downloads voice notes to a temp path when needed.
- Invokes transcription for voice messages.

### 4. AI Router

- Receives normalized text.
- Returns a strict structured route: target type plus optional habit label.
- Defaults to `note_entry` on parse or confidence failure.

### 5. Daily Note Engine

- Computes note path from local date in the configured timezone.
- Creates missing notes from the template.
- Copies unfinished tasks from the previous day when creating a new note.
- Applies `Notes`, `Tasks`, or `Habits` mutations safely.

### 6. Capture Log Writer

- Ensures `capture-log.md` exists.
- Inserts entries under the correct date header in reverse chronological order.

## Data Structures

### CaptureRequest

- `timestamp`
- `raw_text`
- `normalized_text`
- `source_type` (`text` or `voice`)

### RouteDecision

- `target_type` (`note_entry`, `new_task`, `habit_check`)
- `matched_habit_text` (optional)

## Sequence

1. Telegram update arrives.
2. Authorization passes.
3. Update is normalized into `CaptureRequest`.
4. Voice input is transcribed if needed.
5. AI router returns `RouteDecision`.
6. Daily note engine ensures today's note exists and rolls unfinished tasks forward if needed.
7. Daily note engine applies the routed mutation.
8. Capture log writer mirrors the capture.
9. Handler logs the outcome.

## WSL Deployment Approach

- Keep the Obsidian vault on an accessible path that WSL can read and write.
- Run the bot manually first from a WSL shell using `uv`.
- After manual verification, optionally add a `systemd --user` service or `tmux`-based background run.

## Multi-Phase Deployment Approach

### V1

- Windows Obsidian and the WSL bot share the same local vault.
- Git synchronization can stay on the current simple remote.
- Secrets stay local and may be loaded from `.env`.

### V2

- The primary Git remote moves to a VPS-hosted Git repository.
- Each device still uses its own local working clone.
- The WSL bot continues to run locally and write to the local vault.
- The VPS Git host should avoid storing bot runtime secrets because it is not yet an application host.

### V2.1

- The VPS-hosted Git remote mirrors to a private GitHub repository every 5-15 minutes.
- GitHub serves as redundancy, not the primary write target.
- Mirror credentials should be isolated from bot runtime credentials.

### V3

- A VPS runtime for the bot is added using a working clone on the VPS.
- The WSL runtime remains documented and runnable for regression and fallback use.
- Runtime secrets should move to host-managed injection rather than a repo-local `.env`.

## Why This Shape Fits A First WSL Deployment

- One runtime process is easier to start, stop, and troubleshoot.
- File-backed storage avoids database setup.
- Manual startup plus clear docs lowers operational risk while you learn the environment.
