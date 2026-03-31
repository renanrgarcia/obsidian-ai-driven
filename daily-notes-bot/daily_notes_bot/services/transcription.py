import logging
from pathlib import Path

from daily_notes_bot.config import Config
from daily_notes_bot.services.text import normalize_text


LOGGER = logging.getLogger("daily_notes_bot.transcription")
VOICE_TRANSCRIPTION_FAILURE_TEXT = "[Voice note - transcription failed]"


async def transcribe_voice_file(config: Config, voice_path: Path) -> str:
    if not config.gemini_api_key:
        return VOICE_TRANSCRIPTION_FAILURE_TEXT

    try:
        from google import genai  # type: ignore
    except ImportError:
        LOGGER.warning("google-genai is not installed; using voice transcription fallback")
        return VOICE_TRANSCRIPTION_FAILURE_TEXT

    try:
        client = genai.Client(api_key=config.gemini_api_key)
        uploaded = client.files.upload(file=str(voice_path))
        response = client.models.generate_content(
            model=config.gemini_model,
            contents=[
                "Transcribe this voice note into plain text. Return only the transcription.",
                uploaded,
            ],
        )
        text = normalize_text(getattr(response, "text", "") or "")
        return text or VOICE_TRANSCRIPTION_FAILURE_TEXT
    except Exception:
        LOGGER.exception("Voice transcription failed")
        return VOICE_TRANSCRIPTION_FAILURE_TEXT
