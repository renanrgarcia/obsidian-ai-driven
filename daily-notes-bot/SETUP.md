# daily-notes-bot WSL Setup

This document describes the intended WSL layout for development and runtime. The goal is to make WSL look closer to a future VPS layout while keeping the Obsidian vault local.

## Target WSL Layout

```text
~/projects/
  obsidian-ai-driven/   # umbrella repo clone, branch: develop

env/
  daily-notes-bot.dev.env

~/apps/
  obsidian-ai-driven/   # umbrella repo clone, branch: main
  venvs/
    daily-notes-bot/
  env/
    daily-notes-bot.env
```

## Why This Layout

- `~/projects/...` is for coding and test work.
- `~/projects/env/...` keeps development secrets outside the repo.
- `~/apps/...` is for runtime execution.
- `~/apps/venvs/...` keeps the runtime Python environment outside the repo.
- `~/apps/env/...` keeps runtime secrets outside the repo.
- Runtime paths live in the Linux filesystem instead of `/mnt/c/...`, which is closer to how a VPS should behave.

The Obsidian vault can still stay on the Windows side and be accessed through a WSL path such as `/mnt/c/...`.

## 1. Install Python and uv in WSL

Inside WSL:

```bash
sudo apt update
sudo apt install -y python3.13 python3.13-venv python3-pip curl
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv --version
python3.13 --version
```

If your distro does not offer `python3.13`, Python 3.11+ is acceptable.

## 2. Create the Folder Structure

```bash
mkdir -p ~/projects/obsidian-ai-driven
mkdir -p ~/projects/env
mkdir -p ~/apps/venvs
mkdir -p ~/apps/env
```

## 3. Clone the Repository Twice

Repository URL:

```text
https://github.com/renanrgarcia/obsidian-ai-driven.git
```

### Development clone

```bash
cd ~/projects
git clone https://github.com/renanrgarcia/obsidian-ai-driven.git
cd obsidian-ai-driven
```

Switch to `develop`. If it does not exist yet, create it from `main`:

```bash
git switch develop || git switch -c develop main
```

### Runtime clone

```bash
cd ~/apps
git clone https://github.com/renanrgarcia/obsidian-ai-driven.git
cd obsidian-ai-driven
git switch main
```

## 4. Create the Runtime Virtual Environment

```bash
uv venv ~/apps/venvs/daily-notes-bot
```

## 5. Prepare the Development Clone

```bash
cd ~/projects/obsidian-ai-driven/daily-notes-bot
uv sync --extra dev
pytest
```

This clone is for editing, testing, and validating changes before they go to production.

## 6. Create the Development Env File

Development env file:

```text
~/projects/env/daily-notes-bot.dev.env
```

Create and secure it:

```bash
mkdir -p ~/projects/env
cp ~/projects/obsidian-ai-driven/daily-notes-bot/.env.example ~/projects/env/daily-notes-bot.dev.env
chmod 600 ~/projects/env/daily-notes-bot.dev.env
```

Edit it with your local values:

```bash
nano ~/projects/env/daily-notes-bot.dev.env
```

## 7. Up and Run Development First

Start from the development clone on `develop`:

```bash
cd ~/projects/obsidian-ai-driven/daily-notes-bot
git switch develop
uv sync --extra dev
pytest
```

Then load the development env file and run the bot:

```bash
cd ~/projects/obsidian-ai-driven/daily-notes-bot
set -a
source ~/projects/env/daily-notes-bot.dev.env
set +a
uv run daily-notes-bot
```

Troubleshooting:

- If `source` prints `: command not found`, the env file likely has Windows line endings. Fix it with `sed -i 's/\r$//' ~/projects/env/daily-notes-bot.dev.env`.
- Each env line must use `KEY=value` with no spaces around `=`.
- Verify the file loaded correctly with `echo "$DAILY_NOTES_DIR"` after `source`.

Use this flow while coding, testing, committing, and pushing from `develop`.

## 8. Prepare the Runtime Clone

```bash
source ~/apps/venvs/daily-notes-bot/bin/activate
cd ~/apps/obsidian-ai-driven/daily-notes-bot
uv sync --active
```

Use `--active` because the virtual environment lives outside the repo.

## 9. Create the Runtime Env File

Runtime env file:

```text
~/apps/env/daily-notes-bot.env
```

Create and secure it:

```bash
mkdir -p ~/apps/env
cp ~/apps/obsidian-ai-driven/daily-notes-bot/.env.example ~/apps/env/daily-notes-bot.env
chmod 600 ~/apps/env/daily-notes-bot.env
```

Edit it with your production values:

```bash
nano ~/apps/env/daily-notes-bot.env
```

`chmod 600` means only the file owner can read or change it.

Required values:

- `TELEGRAM_BOT_TOKEN`: Telegram BotFather token from `@BotFather`
- `ALLOWED_USER_ID`: your personal Telegram numeric user id
- `OBSIDIAN_VAULT_PATH`: WSL path to your vault root
- `DAILY_NOTES_DIR`: relative path inside the vault
- `TIMEZONE`: local timezone such as `America/Sao_Paulo`

Optional values:

- `CAPTURE_LOG_FILENAME`
- `GEMINI_API_KEY`
- `GEMINI_MODEL`

If the production env file was edited from Windows, normalize line endings before sourcing it:

```bash
sed -i 's/\r$//' ~/apps/env/daily-notes-bot.env
```

## 10. Up and Run Production

First make sure the tested changes are already promoted from `develop` to `main`.

Update the runtime clone and dependencies:

```bash
source ~/apps/venvs/daily-notes-bot/bin/activate
cd ~/apps/obsidian-ai-driven/daily-notes-bot
git switch main
git pull
uv sync --active
```

Then load the runtime env file and start the bot:

```bash
source ~/apps/venvs/daily-notes-bot/bin/activate
cd ~/apps/obsidian-ai-driven/daily-notes-bot
set -a
source ~/apps/env/daily-notes-bot.env
set +a
uv run daily-notes-bot
```

## 11. Development Workflow

Development clone:

```bash
cd ~/projects/obsidian-ai-driven/daily-notes-bot
git switch develop
uv sync --extra dev
pytest
```

Then commit and push from that clone.

Promote tested changes from `develop` to `main` through your normal Git flow.

## 12. Manual Deployment Workflow

Runtime clone:

```bash
source ~/apps/venvs/daily-notes-bot/bin/activate
cd ~/apps/obsidian-ai-driven/daily-notes-bot
git switch main
git pull
uv sync --active
```

Then load the runtime env file and start the bot:

```bash
set -a
source ~/apps/env/daily-notes-bot.env
set +a
uv run daily-notes-bot
```

## 13. Obsidian Vault Path

If your vault is still on Windows, use the WSL-mounted path.

Windows path:

```text
C:\Users\your-user\Documents\ObsidianVault
```

WSL path:

```text
/mnt/c/Users/your-user/Documents/ObsidianVault
```

## 14. What Is Deferred

These are intentionally not part of this phase:

- auto-deploy
- `systemd --user` service files
- VPS secret management beyond host env files
- GitHub Actions deployment automation
