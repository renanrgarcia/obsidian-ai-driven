# Architecture

**Pattern:** Pre-implementation project with planned single-process application architecture.

## High-Level Structure

The repository currently contains only a README and a feature specification. The initial implementation should use a thin event-loop entrypoint and a small set of pure file-writing helpers so the Telegram-specific pieces remain replaceable later.

Planned flow:

1. Telegram handler receives a message.
2. Authorization layer checks `ALLOWED_USER_ID`.
3. Voice messages are transcribed when needed.
4. AI router classifies the normalized capture.
5. Daily note engine ensures the daily note exists and updates `Notes`, `Tasks`, or `Habits`.
6. Capture log writer mirrors the capture into `capture-log.md`.
7. Structured logs capture success or failure.

## Identified Patterns

### Specification-First Planning

**Location:** `.spec/` and planned `.specs/`
**Purpose:** Define behavior before code exists.
**Implementation:** Markdown specifications and project planning documents.
**Example:** `.spec/features/telegram-obsidian-journal/spec.md`

### Thin Entrypoint, Focused Helpers

**Location:** Planned for `bot.py`
**Purpose:** Keep Telegram runtime concerns separate from note-writing logic.
**Implementation:** One startup file calling pure helper functions for note creation, routing, task carry-forward, and capture logging.
**Example:** Planned, not yet implemented.

## Data Flow

### Capture Processing

Telegram update -> authorization -> optional transcription -> AI routing -> daily note write -> capture log write -> response/logging

### Daily Note Creation

Incoming capture -> compute today's note path -> create from template if missing -> inspect previous day's tasks -> copy unchecked tasks -> apply routed update -> save file

## Code Organization

**Approach:** Start monolithic for speed, structured internally for later extraction.

**Structure:**

- Current: README + feature spec only
- Planned: `bot.py`, `requirements.txt`, `.env.example`, `README.md`, `SETUP.md`, `tests/`

**Module boundaries:**

- Entry/runtime: Telegram polling startup
- Domain logic: routing, note mutation, task carry-forward
- Integration logic: Gemini transcription, filesystem I/O
