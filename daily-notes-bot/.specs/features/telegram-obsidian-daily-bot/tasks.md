# Telegram Obsidian Daily Bot Tasks

**Design:** `.specs/features/telegram-obsidian-daily-bot/design.md`
**Status:** Updated

## Execution Plan

### T1: Replace The Daily Note Template And Section Model

**What:** Update the markdown section contract and note-creation helpers to use `Notes`, `Today`, `Scheduled`, `Project Tasks`, and `Habits` with seeded default habits and no rollover.
**Done when:** New notes render with the new title and sections, task writes are section-aware, and no carry-forward behavior remains.

### T2: Introduce Structured Daily-Note Routing

**What:** Expand `RouteDecision` and replace the old heuristic `Tasks` routing with habit matching plus Gemini-based extraction of task text, day, and time.
**Done when:** Routing can return `note_entry`, `task`, or `habit_check`, future dates are supported, and invalid AI output falls back safely to `note_entry`.

### T3: Wire Telegram Processing To Future Daily Notes

**What:** Change the handler flow so note creation and mutation use `route.target_date` instead of always writing to the capture day note.
**Done when:** A dated task can create and update a future note while ordinary notes still land on the current day.

### T4: Rewrite Verification Coverage

**What:** Replace the old `## Tasks` and rollover tests with coverage for the new template, seeded habits, future-note writes, section selection, and AI fallback behavior.
**Done when:** Tests cover untimed tasks, timed tasks, wiki-linked tasks, future notes, ambiguous AI output, and habit matching against the default checklist.

### T5: Refresh Spec And Project State

**What:** Update the feature spec and project state docs so they describe the new daily-note workflow instead of the old `Tasks`/carry-forward model.
**Done when:** `.specs` consistently describes daily-note-only scheduling and no longer documents automatic task rollover.
