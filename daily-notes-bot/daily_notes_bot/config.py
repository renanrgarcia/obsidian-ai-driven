import os
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class Config:
    telegram_bot_token: str
    allowed_user_id: int
    obsidian_vault_path: Path
    daily_notes_dir: Path
    capture_log_filename: str
    timezone_name: str
    gemini_api_key: str | None
    gemini_model: str

    @property
    def timezone(self) -> ZoneInfo:
        return ZoneInfo(self.timezone_name)

    @property
    def daily_notes_root(self) -> Path:
        return self.obsidian_vault_path / self.daily_notes_dir

    @property
    def capture_log_path(self) -> Path:
        return self.obsidian_vault_path / self.capture_log_filename


def load_local_env_file(env_path: Path = Path(".env")) -> None:
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def load_config() -> Config:
    load_local_env_file()
    required_keys = (
        "TELEGRAM_BOT_TOKEN",
        "ALLOWED_USER_ID",
        "OBSIDIAN_VAULT_PATH",
        "DAILY_NOTES_DIR",
        "TIMEZONE",
    )

    missing = [key for key in required_keys if not os.environ.get(key)]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

    return Config(
        telegram_bot_token=os.environ["TELEGRAM_BOT_TOKEN"],
        allowed_user_id=int(os.environ["ALLOWED_USER_ID"]),
        obsidian_vault_path=Path(os.environ["OBSIDIAN_VAULT_PATH"]).expanduser(),
        daily_notes_dir=Path(os.environ["DAILY_NOTES_DIR"]),
        capture_log_filename=os.environ.get("CAPTURE_LOG_FILENAME", "capture-log.md"),
        timezone_name=os.environ["TIMEZONE"],
        gemini_api_key=os.environ.get("GEMINI_API_KEY") or None,
        gemini_model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
    )
