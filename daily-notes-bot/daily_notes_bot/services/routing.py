import json
import logging
import re
from datetime import date
from pathlib import Path

from daily_notes_bot.config import Config
from daily_notes_bot.models import CaptureRequest, RouteDecision
from daily_notes_bot.services.daily_notes import DEFAULT_HABITS, daily_note_path, load_note_sections
from daily_notes_bot.services.markdown import TASK_PATTERN
from daily_notes_bot.services.text import normalize_habit_label, normalize_text

LOGGER = logging.getLogger("daily_notes_bot.routing")
WIKI_LINK_PATTERN = re.compile(r"\[\[[^\]]+\]\]")
TIME_PATTERN = re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")


def _default_habit_lines() -> list[str]:
    return [f"- [ ] {habit}" for habit in DEFAULT_HABITS]


def _load_habit_lines(note_path: Path) -> list[str]:
    if not note_path.exists():
        return _default_habit_lines()
    return load_note_sections(note_path)["## Habits"]


def _match_habit_route(text: str, note_path: Path, target_date: date) -> RouteDecision | None:
    normalized_text = normalize_text(text).lower()
    normalized_label = normalize_habit_label(normalized_text)

    for line in _load_habit_lines(note_path):
        match = TASK_PATTERN.match(line)
        if not match:
            continue

        habit_body = match.group("body").strip()
        habit_label = normalize_habit_label(habit_body)
        if habit_label and habit_label in normalized_label:
            return RouteDecision(
                target_type="habit_check",
                target_date=target_date,
                matched_habit_text=habit_body,
            )

    return None


def _fallback_note_entry(target_date: date) -> RouteDecision:
    return RouteDecision(target_type="note_entry", target_date=target_date)


def _extract_json_payload(text: str) -> dict[str, object] | None:
    candidate = text.strip()
    if candidate.startswith("```"):
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", candidate, re.DOTALL)
        if match:
            candidate = match.group(1)

    try:
        payload = json.loads(candidate)
    except json.JSONDecodeError:
        return None

    return payload if isinstance(payload, dict) else None


def _route_with_gemini(text: str, target_date: date, config: Config) -> dict[str, object] | None:
    if not config.gemini_api_key:
        return None

    try:
        from google import genai  # type: ignore
    except ImportError:
        LOGGER.warning("google-genai is not installed; using routing fallback")
        return None

    prompt = f"""
You classify Telegram captures for an Obsidian daily-note workflow.
Today in the user's local timezone is {target_date.isoformat()}.

Return only JSON with this exact shape:
{{
  "intent": "task" | "note_entry",
  "task_text": string | null,
  "target_date": "YYYY-MM-DD" | null,
  "target_time": "HH:MM" | null
}}

Rules:
- Use "task" only when the text clearly commits work to a specific day.
- For same-day tasks, set target_date to {target_date.isoformat()}.
- For dated future tasks, resolve relative dates using the provided local date.
- Use target_time only for firm scheduled times.
- Preserve any wiki links exactly as written.
- If the text is only a note/capture or the day is not firm, use "note_entry" and null dates/times.

Text: {text}
""".strip()

    try:
        client = genai.Client(api_key=config.gemini_api_key)
        response = client.models.generate_content(
            model=config.gemini_model,
            contents=[prompt],
        )
    except Exception:
        LOGGER.exception("Gemini routing failed")
        return None

    return _extract_json_payload(getattr(response, "text", "") or "")


def route_capture(capture: CaptureRequest, config: Config) -> RouteDecision:
    target_date = capture.timestamp.date()
    note_path = daily_note_path(config, target_date)
    habit_route = _match_habit_route(capture.normalized_text, note_path, target_date)
    if habit_route:
        return habit_route

    payload = _route_with_gemini(capture.normalized_text, target_date, config)
    if not payload:
        return _fallback_note_entry(target_date)

    intent = payload.get("intent")
    if intent == "note_entry":
        return _fallback_note_entry(target_date)
    if intent != "task":
        return _fallback_note_entry(target_date)

    task_text = normalize_text(str(payload.get("task_text") or ""))
    target_date_text = payload.get("target_date")
    target_time_text = normalize_text(str(payload.get("target_time") or ""))

    if not task_text or not isinstance(target_date_text, str):
        return _fallback_note_entry(target_date)

    try:
        resolved_target_date = date.fromisoformat(target_date_text)
    except ValueError:
        return _fallback_note_entry(target_date)

    scheduled_time = None
    if target_time_text:
        if not TIME_PATTERN.match(target_time_text):
            return _fallback_note_entry(target_date)
        scheduled_time = target_time_text

    if scheduled_time:
        target_section = "## Scheduled"
    elif WIKI_LINK_PATTERN.search(task_text):
        target_section = "## Project Tasks"
    else:
        target_section = "## Today"

    return RouteDecision(
        target_type="task",
        target_date=resolved_target_date,
        target_section=target_section,
        scheduled_time=scheduled_time,
        task_text=task_text,
    )
