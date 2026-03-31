# Integrations

## Planned External Integrations

### Telegram Bot API

- Purpose: Receive text and voice captures from one authorized user
- Interface: `python-telegram-bot` long polling
- Risk: Authorization mistakes or unsupported update types

### Google Gemini API

- Purpose: Transcribe voice notes and classify capture routing
- Interface: `google-genai`
- Risk: Response shape drift, network failures, and cost/latency concerns

### Obsidian Vault Filesystem

- Purpose: Persist daily notes and capture log
- Interface: Direct file reads/writes via Python filesystem APIs
- Risk: Path mismatches between Windows and WSL, concurrent manual edits

## Local Environment Dependencies

- WSL2 Linux distro with Python 3.13 preferred, Python 3.11+ compatible
- Vault path visible from WSL
- Project bootstrapped and executed through `uv`
- Runtime configuration supplied through environment variables, optionally populated from `.env` in local WSL development

## Secrets Strategy By Version

### V1 Local WSL MVP

- Recommended: local `.env` file plus strict `.gitignore`
- Why: free, simple, and sufficient for a single-user local machine
- Hardening: restrict file permissions where practical and keep the runtime contract environment-variable based so later migrations do not change code paths

### V2 VPS Git Hub

- Recommended: no application secrets required on the VPS Git host if it remains a bare or central Git remote only
- Why: the safest secret is the one that is not present on that machine
- Hardening: prefer SSH keys with passphrases for Git access and keep bot API keys off the Git hub host

### V2.1 GitHub Redundancy Mirror

- Recommended: GitHub Actions repository secrets if the mirror is automated through GitHub, or a dedicated deploy key if mirroring is push-based from the VPS
- Why: both options are free on a private repository and avoid committing credentials
- Hardening: use a dedicated mirror credential with the smallest possible repository scope

### V3 VPS Bot Runtime

- Recommended free baseline: `systemd` `EnvironmentFile=` or a root-owned app env file outside the repository
- More secure free option: `pass` with GPG-encrypted secrets loaded into the environment at service start
- Best paid-hosted option if later needed: a managed secret store such as Azure Key Vault, AWS Systems Manager Parameter Store, or Google Secret Manager
