from pathlib import Path
from tempfile import NamedTemporaryFile

from daily_notes_bot.config import Config
from daily_notes_bot.models import CaptureRequest
from daily_notes_bot.services.text import normalize_text
from daily_notes_bot.services.transcription import (
    VOICE_TRANSCRIPTION_FAILURE_TEXT,
    transcribe_voice_file,
)


async def normalize_capture_from_message(message, config: Config) -> CaptureRequest:
    timestamp = message.date.astimezone(config.timezone)

    if message.text:
        normalized_text = normalize_text(message.text)
        return CaptureRequest(
            timestamp=timestamp,
            raw_text=message.text,
            normalized_text=normalized_text,
            source_type="text",
        )

    if getattr(message, "voice", None):
        telegram_file = await message.voice.get_file()
        with NamedTemporaryFile(delete=False, suffix=".ogg") as temp_file:
            temp_path = Path(temp_file.name)

        try:
            await telegram_file.download_to_drive(custom_path=str(temp_path))
            transcription = await transcribe_voice_file(config, temp_path)
            return CaptureRequest(
                timestamp=timestamp,
                raw_text="[voice note]",
                normalized_text=normalize_text(transcription) or VOICE_TRANSCRIPTION_FAILURE_TEXT,
                source_type="voice",
            )
        finally:
            temp_path.unlink(missing_ok=True)

    raise ValueError("Unsupported message type")
