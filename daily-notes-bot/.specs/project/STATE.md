# State

## Current Focus

- Adapt daily-note processing to the new five-section workflow.
- Keep daily notes as the only scheduling surface handled by the bot.

## Decisions

- Daily notes use `# YYYY-MM-DD` plus `## Notes`, `## Today`, `## Scheduled`, `## Project Tasks`, and `## Habits`.
- New daily notes start clean except for the default habits checklist.
- Unfinished tasks do not roll forward automatically.
- Habit matching remains a same-day action against the current daily note habits.
- Non-habit captures use Gemini to decide whether they are firm dated tasks or simple note entries.
- A timed task goes to `## Scheduled`.
- An untimed task with a wiki link goes to `## Project Tasks`.
- An untimed task without a wiki link goes to `## Today`.
- If routing is ambiguous or no firm day is found, the capture falls back to the current day `## Notes`.

## Assumptions

- The bot only mutates daily notes and the capture log.
- Users provide any desired wiki links directly in the task text.
- A task without a firm day should not be written into a daily-task section.

## Next Actions

- Keep test coverage centered on note creation, route conversion, and future-note writes.
- Leave PARA note management outside daily notes for a later phase, if needed.
