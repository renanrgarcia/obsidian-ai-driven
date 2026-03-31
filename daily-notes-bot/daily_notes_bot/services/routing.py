from pathlib import Path

from daily_notes_bot.models import RouteDecision
from daily_notes_bot.services.daily_notes import load_note_sections
from daily_notes_bot.services.markdown import TASK_PATTERN
from daily_notes_bot.services.text import normalize_habit_label, normalize_text


def heuristic_route_capture(text: str, note_path: Path) -> RouteDecision:
    normalized_text = normalize_text(text).lower()
    sections = load_note_sections(note_path)
    normalized_label = normalize_habit_label(normalized_text)

    if normalized_text.startswith(("todo ", "task ", "- [ ] ")):
        return RouteDecision(target_type="new_task")

    for line in sections["## Habits"]:
        match = TASK_PATTERN.match(line)
        if not match:
            continue

        habit_body = match.group("body").strip()
        habit_label = normalize_habit_label(habit_body)
        if habit_label and habit_label in normalized_label:
            return RouteDecision(target_type="habit_check", matched_habit_text=habit_body)

    return RouteDecision(target_type="note_entry")
