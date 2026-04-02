# Obsidian AI Driven

**Vision:** Build a private Telegram-to-Obsidian capture bot that writes into a daily-note workflow where `5.Daily Notes` is the execution and scheduling layer.
**For:** A single personal user managing dated work from Obsidian daily notes.
**Solves:** Fast capture from Telegram into the correct daily note section without manual copy/paste or scattered task placement.

## Goals

- Create daily notes with the standard five-section template and default habits.
- Route captures into the correct day and section using a deterministic daily-note workflow.
- Support future-dated tasks by creating the matching future daily note immediately.
- Keep undated or ambiguous captures out of scheduled task sections by falling back to `## Notes`.

## Scope

**Included:**

- Current-day and future-day daily note creation
- Task placement into `## Today`, `## Scheduled`, or `## Project Tasks`
- Habit checkbox updates in `## Habits`
- Note-entry fallback into `## Notes`
- Capture-log mirroring

**Excluded:**

- Editing project, area, inbox, resource, or archive notes
- Automatic backlog synchronization outside daily notes
- Automatic rollover of unfinished tasks between days
