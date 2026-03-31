from daily_notes_bot.config import Config


def is_authorized_user(user_id: int | None, config: Config) -> bool:
    return user_id == config.allowed_user_id
