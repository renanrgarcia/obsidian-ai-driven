# Telegram Obsidian Daily Bot Spec

**Status:** Draft
**Source:** Adapted from `.spec/features/telegram-obsidian-journal/spec.md`

## Goal

Deliver the first working slice of a private Telegram bot that runs in WSL, updates an Obsidian daily note with `Notes`, `Tasks`, and `Habits`, and keeps an audit log of all captures.

## Requirements

- [TODB-01] The system must run locally inside WSL2 using Python 3.13 as the default target, with Python 3.11+ compatibility, and Telegram long polling.
- [TODB-02] The system must process messages only from the configured `ALLOWED_USER_ID`.
- [TODB-03] The system must create the current daily note from the configured template shape when the file does not exist.
- [TODB-04] The created daily note template must contain `## Notes`, `## Tasks`, and `## Habits` sections only.
- [TODB-05] When creating a new daily note, the system must carry forward unchecked tasks from the previous calendar day's `## Tasks` section.
- [TODB-06] Completed tasks and empty placeholder task lines must not be carried forward.
- [TODB-07] Every normalized capture must be routed to exactly one of: `note_entry`, `new_task`, or `habit_check`.
- [TODB-08] Ambiguous routing results must fall back to `note_entry`.
- [TODB-09] `note_entry` captures must be inserted at the top of the `## Notes` section as `- HH:MM: message text`.
- [TODB-10] `new_task` captures must be inserted into `## Tasks` as unchecked checkbox items below carried-forward tasks and above older current-day tasks.
- [TODB-11] `habit_check` captures must update only an existing matching habit item under `## Habits`.
- [TODB-12] If no existing habit matches confidently, the capture must fall back to `note_entry`.
- [TODB-13] Every capture must also be mirrored into `capture-log.md` under the correct day header in reverse chronological order.
- [TODB-14] Voice notes must be downloaded, transcribed, and handled as normalized text captures.
- [TODB-15] Voice transcription failures must still write `[Voice note - transcription failed]` to the daily note target and capture log.
- [TODB-16] The project must provide first-time-friendly WSL setup instructions, including `uv` installation, Python installation, environment setup, vault path configuration, and a repeatable startup command.
- [TODB-17] The project documentation must define a phased deployment model: v1 local WSL runtime, v2 VPS-hosted primary Git remote, v2.1 GitHub mirroring, and v3 optional VPS bot runtime.
- [TODB-18] The WSL runtime must remain documented and runnable as a supported fallback and regression path even after a VPS runtime is introduced.
- [TODB-19] The project documentation must define a phased secrets-management strategy that keeps `.env` local to development and prefers host-managed or repository-managed secret injection for later hosted phases.

## Non-Goals

- Multi-user support
- Group chats
- New habit creation from free-form captures
- Production VPS deployment in the first slice
- Replacing WSL entirely in future phases

## Acceptance Snapshot

- A first-time WSL user can install dependencies, set env vars, start the bot, and see a Telegram text message appear in the correct daily note section.
- A new day note is created automatically with unfinished tasks copied from the prior day.
- A voice note failure does not lose the capture.
