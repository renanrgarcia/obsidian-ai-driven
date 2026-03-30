# State

## Current Focus

- Create the first implementation slice for a local WSL-based Telegram-to-Obsidian bot.
- Keep the first release simple enough for a first-time WSL deployment.

## Decisions

- Use Python 3.11+ with `python-telegram-bot` and Gemini-based transcription.
- Keep v1 as a single-process long-polling bot running in WSL2.
- In v1, Windows Obsidian and the WSL bot share the same local vault via the WSL-mounted Windows path.
- Daily notes use `Notes`, `Tasks`, and `Habits` sections only.
- General captures route to `Notes`; actionable items route to `Tasks`; habit completions update existing habit checkboxes.
- When a daily note is created, unfinished tasks from the previous day are carried forward.
- Every capture is mirrored into `capture-log.md` regardless of routing outcome.
- In v2, the primary Git remote moves to the VPS, but working vaults remain local to each device.
- In v2.1, the VPS-hosted Git remote is mirrored to a private GitHub repository every 5-15 minutes for redundancy.
- In v3, the bot may run on the VPS, but the WSL runtime remains documented and supported for regression testing and fallback operation.

## Assumptions

- The Obsidian vault is reachable from WSL through a Linux path such as `/mnt/c/...` or a native Linux path.
- The project will begin with a single `bot.py` file before later modularization.
- The user needs explicit WSL setup and run instructions because this is their first deployment in that environment.
- A future VPS deployment will use a working clone for runtime file edits rather than editing a bare Git repo directly.

## Blockers

- No application code exists yet.
- No dependency manifest or setup files exist yet.
- Final WSL vault path and Python toolchain choice are not yet committed in code.

## Next Actions

- Implement project bootstrap files and dependency configuration.
- Build the daily note engine before Telegram handler complexity grows.
- Add a minimal WSL operations guide as part of the first functional slice.
- Keep future deployment docs structured so the VPS path adds to the WSL path instead of replacing it.

## Deferred Ideas

- `systemd` service automation after the bot works manually.
- Modularizing into `telegram`, `transcription`, and `journal` packages after the first slice is stable.
- CI automation after local reliability is proven.
- Automated VPS-to-GitHub mirror health checks.

## Preferences

- Prefer concrete operational instructions over abstract deployment advice.
