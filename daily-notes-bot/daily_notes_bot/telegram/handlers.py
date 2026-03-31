import asyncio
import logging
from pathlib import Path

from daily_notes_bot.config import Config
from daily_notes_bot.models import CaptureRequest, RouteDecision
from daily_notes_bot.services.capture_log import write_capture_log
from daily_notes_bot.services.daily_notes import (
    daily_note_path,
    ensure_daily_note,
    insert_new_task,
    insert_note_entry,
    read_previous_unfinished_tasks,
    update_habit_checkbox,
)
from daily_notes_bot.services.routing import heuristic_route_capture
from daily_notes_bot.telegram.authorization import is_authorized_user
from daily_notes_bot.telegram.normalizer import normalize_capture_from_message


LOGGER = logging.getLogger("daily_notes_bot.telegram")


def apply_route(
    note_path: Path,
    capture: CaptureRequest,
    route: RouteDecision,
    *,
    created_today: bool,
    carry_forward_count: int,
) -> str:
    if route.target_type == "new_task":
        insert_new_task(
            note_path,
            capture,
            created_today=created_today,
            carry_forward_count=carry_forward_count,
        )
        return "task"

    if route.target_type == "habit_check" and route.matched_habit_text:
        if update_habit_checkbox(note_path, route.matched_habit_text):
            return "habit"

    insert_note_entry(note_path, capture)
    return "note"


async def process_message(message, config: Config) -> str:
    capture = await normalize_capture_from_message(message, config)
    note_path = daily_note_path(config, capture.timestamp.date())
    created_today = not note_path.exists()
    carry_forward_count = 0
    if created_today:
        carry_forward_count = len(read_previous_unfinished_tasks(config, capture.timestamp.date()))

    ensure_daily_note(config, capture.timestamp.date())
    route = heuristic_route_capture(capture.normalized_text, note_path)
    outcome = apply_route(
        note_path,
        capture,
        route,
        created_today=created_today,
        carry_forward_count=carry_forward_count,
    )
    write_capture_log(config.capture_log_path, capture)
    LOGGER.info(
        "Capture processed",
        extra={
            "outcome": outcome,
            "source_type": capture.source_type,
            "note_path": str(note_path),
        },
    )
    return outcome


async def handle_message(update, context) -> None:
    del context
    config: Config = update.application.bot_data["config"]
    message = update.effective_message
    user = update.effective_user

    if not is_authorized_user(getattr(user, "id", None), config):
        LOGGER.warning("Rejected unauthorized user", extra={"user_id": getattr(user, "id", None)})
        return

    if message is None or (not message.text and not getattr(message, "voice", None)):
        return

    try:
        outcome = await process_message(message, config)
        await message.reply_text(f"Captured to {outcome}.")
    except Exception:
        LOGGER.exception("Failed to process message")
        await message.reply_text("Capture failed. Check logs and configuration.")


async def run_bot(config: Config) -> None:
    from telegram.ext import Application, MessageHandler, filters

    application = Application.builder().token(config.telegram_bot_token).build()
    application.bot_data["config"] = config
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.VOICE, handle_message))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    LOGGER.info("Bot started")

    try:
        await asyncio.Event().wait()
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()
