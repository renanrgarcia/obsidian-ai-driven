# Testing

## Current State

No test suite exists yet.

## Planned Strategy

### Unit Tests

- Daily note template creation
- Previous-day unfinished task carry-forward
- Task insertion ordering with carried-forward items
- Note entry insertion under `## Notes`
- Habit checkbox updates and unmatched fallback behavior
- Capture log reverse-chronological insertion

### Integration-Style Tests

- Authorized text capture end-to-end through routing and file writes
- Voice transcription success/failure handling with deterministic stubs

### Manual Verification In WSL

- Start the bot from the WSL shell using the documented setup steps.
- Send an authorized Telegram text message and confirm note update.
- Send an authorized voice note and confirm transcription handling.
- Create a new day transition scenario and confirm unfinished task rollover.

## Quality Gate

- Run tests inside WSL before declaring the first slice complete.
- Keep at least one manual checklist for startup, update handling, and file outputs.
