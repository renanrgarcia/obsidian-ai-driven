# Conventions

## Current State

The codebase has no implementation files yet, so conventions are inferred from the repository instructions and existing specification work.

## Naming And Style

- Use English for identifiers, comments, and commit messages.
- Prefer clear, descriptive names over abbreviations.
- Keep functions small and responsibility-focused.
- Preserve existing behavior unless a spec explicitly changes it.

## Structural Conventions

- Keep Telegram handlers thin.
- Keep daily-note mutation logic isolated from transport concerns.
- Avoid leaking implementation details into higher-level flow control.
- Add comments only when reasoning is non-obvious.

## Quality Conventions

- Add tests alongside behavior changes where feasible.
- Verify build and tests before considering a task complete.
- Favor deterministic file mutations over brittle string hacks.
- Use structured logging with contextual fields.

## Operational Conventions

- Document WSL setup steps in plain language.
- Prefer simple manual startup before adding service automation.
- Keep paths configurable through environment variables.
