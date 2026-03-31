# Telegram Obsidian Daily Bot Tasks

**Design:** `.specs/features/telegram-obsidian-daily-bot/design.md`
**Status:** Draft

---

## Execution Plan

### Phase 1: Foundation (Sequential)

T1 -> T2 -> T3

### Phase 2: Core Implementation (Mostly Sequential For First Slice)

T3 -> T4 -> T5 -> T6 -> T7

### Phase 3: Verification And WSL Operations

T7 -> T8 -> T9

---

## Task Breakdown

### T1: Create Python Project Bootstrap

**What:** Create `pyproject.toml`, `uv.lock`, `.env.example`, `.gitignore`, and a minimal `README.md` update that states the project purpose.
**Where:** `pyproject.toml`, `uv.lock`, `.env.example`, `.gitignore`, `README.md`
**Depends on:** None
**Requirement:** [TODB-01], [TODB-16], [TODB-19]

**Tools:**

- MCP: filesystem
- Skill: NONE

**Done when:**

- [ ] Runtime dependencies are declared
- [ ] Dependency installation is reproducible through `uv`
- [ ] Required environment variables are documented
- [ ] Temp files and virtualenv folders are ignored

---

### T2: Write WSL Setup Guide

**What:** Create `SETUP.md` with first-time-friendly WSL instructions for `uv` installation, Python installation, environment variables, vault path selection, and manual startup.
**Where:** `SETUP.md`
**Depends on:** T1
**Requirement:** [TODB-16], [TODB-18], [TODB-19]

**Tools:**

- MCP: filesystem
- Skill: NONE

**Done when:**

- [ ] A first-time WSL user can follow the steps without guessing missing commands
- [ ] The guide explains the Windows path to WSL path conversion model
- [ ] The guide includes concrete `uv sync` and `uv run` commands
- [ ] The guide makes clear that WSL remains a supported fallback even after future VPS work

---

### T3: Implement Config And Entrypoint Skeleton

**What:** Create `bot.py` with config loading, logging setup, and Telegram app startup skeleton.
**Where:** `bot.py`
**Depends on:** T1
**Requirement:** [TODB-01], [TODB-02]

**Tools:**

- MCP: filesystem
- Skill: NONE

**Done when:**

- [ ] Startup validates required env vars
- [ ] Telegram app can initialize without business logic errors
- [ ] Unauthorized users are rejected by a dedicated function

---

### T4: Implement Daily Note Engine

**What:** Add note template creation, section parsing, note insertion, and unfinished-task carry-forward logic.
**Where:** `bot.py` or extracted helper module if needed
**Depends on:** T3
**Requirement:** [TODB-03], [TODB-04], [TODB-05], [TODB-06], [TODB-09], [TODB-10], [TODB-11], [TODB-12]

**Tools:**

- MCP: filesystem
- Skill: NONE

**Done when:**

- [ ] Missing notes are created correctly
- [ ] Unfinished tasks are copied only on note creation
- [ ] Notes, tasks, and habits sections mutate without corrupting the file

---

### T5: Implement Capture Log Writer

**What:** Add `capture-log.md` creation and reverse-chronological insertion by day.
**Where:** `bot.py` or extracted helper module if needed
**Depends on:** T4
**Requirement:** [TODB-13]

**Tools:**

- MCP: filesystem
- Skill: NONE

**Done when:**

- [ ] New daily headers are created when missing
- [ ] New entries appear at the top of the correct day section
- [ ] Older sections remain intact

---

### T6: Implement AI Routing And Voice Transcription Integration

**What:** Add Gemini-backed routing and transcription with safe fallback behavior.
**Where:** `bot.py` or extracted helper module if needed
**Depends on:** T4
**Requirement:** [TODB-07], [TODB-08], [TODB-14], [TODB-15]

**Tools:**

- MCP: context7, filesystem
- Skill: NONE

**Done when:**

- [ ] Text captures route to structured decisions
- [ ] Voice notes are transcribed into normalized text
- [ ] Routing or transcription failures fall back safely without data loss

---

### T7: Connect Telegram Handlers To Domain Flow

**What:** Wire text and voice handlers so authorized Telegram updates execute the full normalize -> route -> note write -> capture log flow.
**Where:** `bot.py`
**Depends on:** T5, T6
**Requirement:** [TODB-02] through [TODB-15]

**Tools:**

- MCP: filesystem
- Skill: NONE

**Done when:**

- [ ] Authorized text messages update the vault
- [ ] Authorized voice notes follow the same pipeline
- [ ] Unsupported messages are ignored cleanly

---

### T8: Add Tests For Note Engine And Logging

**What:** Create a test suite for note creation, task carry-forward, section mutation, and capture-log behavior.
**Where:** `tests/`
**Depends on:** T5
**Requirement:** [TODB-03] through [TODB-13]

**Tools:**

- MCP: filesystem
- Skill: NONE

**Done when:**

- [ ] Daily note creation and rollover cases are covered
- [ ] Capture log insertion is covered
- [ ] Tests run locally in WSL

---

### T9: Verify Manual WSL Runbook

**What:** Perform and document the manual WSL verification flow for environment setup, startup, and live Telegram capture checks.
**Where:** `SETUP.md` and final verification notes
**Depends on:** T2, T7, T8
**Requirement:** [TODB-16], [TODB-18], [TODB-19]

**Tools:**

- MCP: filesystem
- Skill: NONE

**Done when:**

- [ ] Startup commands are validated in WSL
- [ ] The verification checklist covers text, voice, and note rollover
- [ ] Common first-time failure modes are documented

---

### T10: Document Future VPS And Mirror Topology

**What:** Document the later-phase deployment model covering VPS-hosted primary Git, GitHub mirroring, retained WSL runtime fallback, and the secrets-management strategy for each phase.
**Where:** `SETUP.md` or a dedicated deployment document
**Depends on:** T2
**Requirement:** [TODB-17], [TODB-18], [TODB-19]

**Tools:**

- MCP: filesystem
- Skill: NONE

**Done when:**

- [ ] The docs explain the difference between the primary VPS Git remote, GitHub redundancy mirror, and local working vaults
- [ ] The docs explain that the VPS bot runtime is additive, not a forced replacement for WSL
- [ ] The docs give a clear rollback path from VPS runtime to WSL runtime
- [ ] The docs recommend a free-first secrets approach for each deployment phase
