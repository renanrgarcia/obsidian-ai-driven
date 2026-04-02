# Telegram Obsidian Daily Bot Spec

**Status:** Updated

## Goal

Deliver a private Telegram-to-Obsidian flow that treats `5.Daily Notes` as the only scheduling surface, using dated daily notes for execution while keeping note routing and task placement deterministic.

## Requirements

- [TODB-01] The system must create a missing daily note at `5.Daily Notes/YYYY-MM-DD.md` with the title `# YYYY-MM-DD`.
- [TODB-02] The created daily note template must contain `## Notes`, `## Today`, `## Scheduled`, `## Project Tasks`, and `## Habits` in that order.
- [TODB-03] New daily notes must seed `## Habits` with the default checklist items for water and medication tracking.
- [TODB-04] The system must not carry unfinished tasks forward automatically from the previous day.
- [TODB-05] Every normalized capture must resolve to exactly one route kind: `note_entry`, `task`, or `habit_check`.
- [TODB-06] Habit routing must only mark an existing matching checkbox under `## Habits`; unmatched habit attempts must fall back to `note_entry`.
- [TODB-07] `note_entry` captures must be inserted at the top of the current day `## Notes` section as `- HH:MM: message text`.
- [TODB-08] For non-habit captures, the system must use Gemini to classify whether the capture is a dated task or a note entry and to extract `task_text`, `target_date`, and optional `target_time`.
- [TODB-09] If Gemini output is missing, invalid, ambiguous, or does not produce a firm target day, the capture must fall back to `note_entry` on the current day.
- [TODB-10] A task with a firm target day must create or open the matching daily note and write the task there.
- [TODB-11] A task with a firm target time must be written under `## Scheduled` as `- [ ] HH:MM task text`.
- [TODB-12] A task with a firm day but no time must be written under `## Project Tasks` when its text contains a wiki link like `[[Project Note]]`.
- [TODB-13] A task with a firm day but no time and no wiki link must be written under `## Today`.
- [TODB-14] The system must preserve user-provided wiki links verbatim when writing task text.
- [TODB-15] Every capture must still be mirrored into `capture-log.md` under the capture day header in reverse chronological order.

## Non-Goals

- Mutating `0.Inbox`, `1.Projects`, `2.Areas`, `3.Resources`, or `9.Archive`
- Maintaining parallel copies of open tasks across project notes and daily notes
- Automatic backlog cleanup or project-note synchronization
- Automatic task rollover between daily notes

## Acceptance Snapshot

- A new daily note is created with the five-section template and seeded habits.
- A capture like “next Wednesday at 7pm budget review” lands in `5.Daily Notes/2026-04-08.md` under `## Scheduled`.
- A capture like “review [[AZ-204 Dashboard]] next Wednesday” lands in the matching future note under `## Project Tasks`.
- A capture that does not resolve to a firm dated task lands in the current day `## Notes`.
