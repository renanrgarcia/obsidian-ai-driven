from datetime import date, timedelta
from pathlib import Path

from daily_notes_bot.config import Config
from daily_notes_bot.models import CaptureRequest
from daily_notes_bot.services.markdown import TASK_PATTERN, parse_sections, render_sections
from daily_notes_bot.services.text import normalize_habit_label


def daily_note_path(config: Config, target_date: date) -> Path:
    return config.daily_notes_root / f"{target_date.isoformat()}.md"


def read_previous_unfinished_tasks(config: Config, target_date: date) -> list[str]:
    previous_path = daily_note_path(config, target_date - timedelta(days=1))
    if not previous_path.exists():
        return []

    sections = parse_sections(previous_path.read_text(encoding="utf-8"))
    unfinished_tasks: list[str] = []
    for line in sections["## Tasks"]:
        match = TASK_PATTERN.match(line)
        if not match:
            continue
        if match.group("done").lower() == "x":
            continue
        if not match.group("body").strip():
            continue
        unfinished_tasks.append(line)

    return unfinished_tasks


def build_daily_note_content(carry_forward_tasks: list[str]) -> str:
    sections = {
        "## Notes": [],
        "## Tasks": list(carry_forward_tasks),
        "## Habits": [],
    }
    return render_sections(sections)


def ensure_daily_note(config: Config, target_date: date) -> Path:
    note_path = daily_note_path(config, target_date)
    note_path.parent.mkdir(parents=True, exist_ok=True)

    if note_path.exists():
        return note_path

    carry_forward_tasks = read_previous_unfinished_tasks(config, target_date)
    note_path.write_text(build_daily_note_content(carry_forward_tasks), encoding="utf-8")
    return note_path


def load_note_sections(note_path: Path) -> dict[str, list[str]]:
    return parse_sections(note_path.read_text(encoding="utf-8"))


def save_note_sections(note_path: Path, sections: dict[str, list[str]]) -> None:
    note_path.write_text(render_sections(sections), encoding="utf-8")


def insert_note_entry(note_path: Path, capture: CaptureRequest) -> None:
    sections = load_note_sections(note_path)
    sections["## Notes"].insert(0, f"- {capture.timestamp.strftime('%H:%M')}: {capture.normalized_text}")
    save_note_sections(note_path, sections)


def insert_new_task(
    note_path: Path,
    capture: CaptureRequest,
    *,
    created_today: bool,
    carry_forward_count: int = 0,
) -> None:
    sections = load_note_sections(note_path)
    new_task_line = f"- [ ] {capture.normalized_text}"

    insertion_index = 0
    if created_today:
        insertion_index = min(carry_forward_count, len(sections["## Tasks"]))

    sections["## Tasks"].insert(insertion_index, new_task_line)
    save_note_sections(note_path, sections)


def update_habit_checkbox(note_path: Path, matched_habit_text: str) -> bool:
    sections = load_note_sections(note_path)
    target_label = normalize_habit_label(matched_habit_text)

    for index, line in enumerate(sections["## Habits"]):
        match = TASK_PATTERN.match(line)
        if not match:
            continue

        habit_body = match.group("body").strip()
        if normalize_habit_label(habit_body) != target_label:
            continue

        sections["## Habits"][index] = f"- [x] {habit_body}"
        save_note_sections(note_path, sections)
        return True

    return False
