# Roadmap

**Current Milestone:** Milestone 1 - Local WSL MVP
**Status:** Planning

---

## Milestone 1 - Local WSL MVP

**Goal:** Run a local bot in WSL that can accept Telegram captures, update daily notes, and mirror all captures into an audit log.
**Target:** Bot can be started in WSL from documented setup steps and perform end-to-end daily note updates for text and voice messages.

### Features

**Workspace And Runtime Bootstrap** - PLANNED

- Create Python project skeleton and dependency management
- Load configuration from `.env`
- Resolve vault paths correctly in WSL
- Provide local startup and restart instructions

**Daily Note Engine** - PLANNED

- Create missing daily note from template
- Carry forward unfinished tasks from the previous day
- Insert note entries and new tasks in the correct sections
- Update matching habit checkboxes safely

**Telegram Capture Flow** - PLANNED

- Accept messages only from one Telegram user
- Process plain text messages
- Download and transcribe voice notes
- Route captures through the daily note engine

**Capture Audit Log** - PLANNED

- Create and update `capture-log.md`
- Keep per-day sections reverse chronological
- Ensure failed transcriptions are still recorded

**WSL Operational Setup** - PLANNED

- Document Python and dependency installation in WSL
- Document environment variable setup
- Document vault path mounting and permissions expectations
- Document how to keep the bot running between terminal sessions

---

## Milestone 2 - VPS Git Hub

**Goal:** Move multi-device synchronization to a VPS-hosted primary Git remote while keeping the working vault local on each device.

### Features

**Primary Remote Migration** - PLANNED

- Point Windows and workstation vault repos to a VPS-hosted Git remote
- Keep WSL bot writing to the same local vault on the Windows machine
- Document pull/push workflow for multiple devices

**Runtime Separation** - PLANNED

- Treat the VPS as the central Git hub, not the live editable vault for every client
- Keep the bot runtime on WSL during this phase
- Document the distinction between Git remote, working clone, and runtime process

---

## Milestone 2.1 - GitHub Redundancy Mirror

**Goal:** Add off-VPS redundancy without changing the primary write path.

### Features

**VPS To GitHub Mirror** - PLANNED

- Mirror the VPS-hosted primary Git remote to a private GitHub repository every 5-15 minutes
- Treat GitHub as redundancy and disaster recovery, not the primary write target
- Document expected mirror lag and recovery workflow

---

## Milestone 3 - Dual Runtime Operations

**Goal:** Add a VPS runtime option for the bot while preserving WSL as a supported fallback and regression path.

### Features

**VPS Bot Runtime** - PLANNED

- Run the Telegram bot from a VPS working clone instead of only from WSL
- Keep the VPS bot writing through a normal working repository and pushing changes to the primary remote
- Document runtime-specific environment and operations guidance

**WSL Regression Runtime** - PLANNED

- Keep the WSL runtime documented and runnable on demand
- Use WSL as the regression and fallback path if the VPS runtime is unavailable
- Avoid coupling the codebase to VPS-only assumptions

**Verification And Tests** - PLANNED

- Add unit tests for note writing and task carry-forward
- Add integration-style tests for routed captures
- Add operator-friendly logging for failure cases
- Verify both WSL and VPS runbooks against the same behavior

**Operations Hardening** - PLANNED

- Add `systemd --user`, `tmux`, or equivalent runtime guidance where appropriate
- Add restart guidance and log inspection workflow
- Add backup and recovery notes for both WSL and VPS modes

---

## Future Considerations

- Telegram command support for status or health checks
- Additional habit matching sophistication
- Message deduplication and idempotency keys
- Git auto-sync workflow for vault changes
- Optional promotion of GitHub from mirror to alternate recovery remote
