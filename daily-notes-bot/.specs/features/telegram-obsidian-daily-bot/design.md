# Telegram Obsidian Daily Bot Design

**Spec:** `.specs/features/telegram-obsidian-daily-bot/spec.md`

## Implementation Shape

Keep the current small module structure, but change the domain contract from a generic `Tasks` bucket to a structured daily-note routing flow that can target the current or a future daily note before any file mutation.

## Components

### Configuration Loader

- Loads vault path, daily notes directory, timezone, and Gemini credentials from environment-backed config.

### Capture Normalizer

- Converts Telegram text or voice input into `CaptureRequest`.
- Ensures timestamps are normalized to the configured timezone before routing.

### Daily-Note Router

- Checks the current daily note habits first, falling back to the default habit template when the note does not exist yet.
- Uses Gemini for non-habit captures to classify `task` vs `note_entry` and extract `task_text`, `target_date`, and `target_time`.
- Converts Gemini output into a strict `RouteDecision`.
- Falls back to `note_entry` when the response is invalid or lacks a firm day.

### Daily Note Engine

- Creates `5.Daily Notes/YYYY-MM-DD.md` on demand with the five-section template and seeded habits.
- Writes notes only to `## Notes`, `## Today`, `## Scheduled`, `## Project Tasks`, or `## Habits`.
- Does not carry forward unfinished work from previous days.

### Telegram Handler Flow

- Normalizes the capture.
- Requests a `RouteDecision`.
- Ensures the target daily note exists for `route.target_date`.
- Applies the note, task, or habit mutation.
- Mirrors the capture into `capture-log.md`.

## Data Structures

### CaptureRequest

- `timestamp`
- `raw_text`
- `normalized_text`
- `source_type`

### RouteDecision

- `target_type` (`note_entry`, `task`, `habit_check`)
- `target_date`
- `target_section` (`## Today`, `## Scheduled`, `## Project Tasks`, or `None`)
- `scheduled_time`
- `task_text`
- `matched_habit_text`

## Section Selection Rules

- `target_time` present -> `## Scheduled`
- no `target_time` and wiki link present -> `## Project Tasks`
- no `target_time` and no wiki link -> `## Today`
- invalid or no firm day -> `note_entry` in the current day `## Notes`
