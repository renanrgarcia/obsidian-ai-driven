import asyncio

from daily_notes_bot.config import load_config
from daily_notes_bot.logging_setup import configure_logging
from daily_notes_bot.telegram.handlers import run_bot


def main() -> None:
    configure_logging()
    config = load_config()
    config.obsidian_vault_path.mkdir(parents=True, exist_ok=True)
    config.daily_notes_root.mkdir(parents=True, exist_ok=True)
    asyncio.run(run_bot(config))
