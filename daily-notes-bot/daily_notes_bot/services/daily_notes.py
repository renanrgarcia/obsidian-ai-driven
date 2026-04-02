from datetime import date
from pathlib import Path

from daily_notes_bot.config import Config
from daily_notes_bot.models import CaptureRequest, RouteDecision
from daily_notes_bot.services.markdown import TASK_PATTERN, parse_sections, render_sections
from daily_notes_bot.services.text import normalize_habit_label

DEFAULT_HABITS = (
    "H\u00b2O 1.5L",
    "H\u00b2O 3L",
    "H\u00b2O 4.5L",
    "Dexilant jejum",
    "Dexilant jantar",
    "Valsartana noite",
)

TASK_SECTIONS = {"## Today", "## Scheduled", "## Project Tasks"}


def daily_note_path(config: Config, target_date: date) -> Path:
    return config.daily_notes_root / f"{target_date.isoformat()}.md"


def build_daily_note_content(target_date: date) -> str:
    sections = {
        "## Notes": [],
        "## Today": [],
        "## Scheduled": [],
        "## Project Tasks": [],
        "## Habits": [f"- [ ] {habit}" for habit in DEFAULT_HABITS],
    }
    return render_sections(sections, title=f"# {target_date.isoformat()}")


def ensure_daily_note(config: Config, target_date: date) -> Path:
    note_path = daily_note_path(config, target_date)
    note_path.parent.mkdir(parents=True, exist_ok=True)

    if note_path.exists():
        return note_path

    note_path.write_text(build_daily_note_content(target_date), encoding="utf-8")
    return note_path


def load_note_sections(note_path: Path) -> dict[str, list[str]]:
    return parse_sections(note_path.read_text(encoding="utf-8"))


def save_note_sections(note_path: Path, sections: dict[str, list[str]]) -> None:
    note_path.write_text(render_sections(sections, title=f"# {note_path.stem}"), encoding="utf-8")


def insert_note_entry(note_path: Path, capture: CaptureRequest) -> None:
    sections = load_note_sections(note_path)
    sections["## Notes"].insert(0, f"- {capture.timestamp.strftime('%H:%M')}: {capture.normalized_text}")
    save_note_sections(note_path, sections)


def insert_task(note_path: Path, route: RouteDecision) -> None:
    if route.target_section not in TASK_SECTIONS:
        raise ValueError(f"Unsupported task section: {route.target_section}")
    if not route.task_text:
        raise ValueError("Task route requires task_text")

    sections = load_note_sections(note_path)
    new_task_line = f"- [ ] {route.task_text}"
    if route.target_section == "## Scheduled" and route.scheduled_time:
        new_task_line = f"- [ ] {route.scheduled_time} {route.task_text}"

    sections[route.target_section].append(new_task_line)
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
