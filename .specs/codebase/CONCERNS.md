# Concerns

## Immediate Risks

- WSL path confusion is likely because this is the first deployment in that environment.
- AI routing and habit matching can produce ambiguous results if the prompt contract is not strict.
- File-section updates can become fragile if implemented as naive string concatenation.
- Voice transcription adds an external dependency before the text flow is proven.

## Recommended Mitigations

- Document an explicit example vault path for WSL, such as `/mnt/c/Users/<user>/ObsidianVault`.
- Implement deterministic section parsing for `Notes`, `Tasks`, and `Habits`.
- Build and verify text capture flow before enabling voice notes in daily use.
- Stub or isolate Gemini integrations so file-writing behavior can be tested without network calls.
- Keep startup manual first; only add background service automation after manual operation is reliable.

## Fragile Areas To Revisit

- Section parsing when note templates drift from the expected headings
- Day rollover logic near timezone boundaries
- Habit semantic matching confidence thresholds
