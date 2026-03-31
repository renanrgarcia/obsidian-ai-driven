from datetime import date, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from zoneinfo import ZoneInfo
import unittest

from daily_notes_bot.config import Config
from daily_notes_bot.models import CaptureRequest, RouteDecision
from daily_notes_bot.services.capture_log import write_capture_log
from daily_notes_bot.services.daily_notes import (
    daily_note_path,
    ensure_daily_note,
    insert_new_task,
    read_previous_unfinished_tasks,
    update_habit_checkbox,
)
from daily_notes_bot.services.markdown import parse_sections
from daily_notes_bot.telegram.handlers import apply_route


class DailyNotesBotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name) / "vault"
        self.config = Config(
            telegram_bot_token="token",
            allowed_user_id=1,
            obsidian_vault_path=self.vault_path,
            daily_notes_dir=Path("Daily Notes"),
            capture_log_filename="capture-log.md",
            timezone_name="America/Sao_Paulo",
            gemini_api_key=None,
            gemini_model="gemini-2.5-flash",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def make_capture(self, text: str, hour: int = 10, minute: int = 30, source_type: str = "text") -> CaptureRequest:
        return CaptureRequest(
            timestamp=datetime(2026, 3, 30, hour, minute, tzinfo=ZoneInfo(self.config.timezone_name)),
            raw_text=text,
            normalized_text=text,
            source_type=source_type,
        )

    def test_ensure_daily_note_creates_template(self) -> None:
        note_path = ensure_daily_note(self.config, date(2026, 3, 30))
        sections = parse_sections(note_path.read_text(encoding="utf-8"))

        self.assertEqual(sections["## Notes"], [])
        self.assertEqual(sections["## Tasks"], [])
        self.assertEqual(sections["## Habits"], [])

    def test_read_previous_unfinished_tasks_filters_completed_and_blank(self) -> None:
        previous = daily_note_path(self.config, date(2026, 3, 29))
        previous.parent.mkdir(parents=True, exist_ok=True)
        previous.write_text(
            "## Notes\n\n## Tasks\n- [ ] keep this\n- [x] done already\n- [ ]   \n\n## Habits\n",
            encoding="utf-8",
        )

        tasks = read_previous_unfinished_tasks(self.config, date(2026, 3, 30))
        self.assertEqual(tasks, ["- [ ] keep this"])

    def test_ensure_daily_note_carries_forward_unfinished_tasks_once(self) -> None:
        previous = daily_note_path(self.config, date(2026, 3, 29))
        previous.parent.mkdir(parents=True, exist_ok=True)
        previous.write_text(
            "## Notes\n\n## Tasks\n- [ ] carry me\n- [x] done\n\n## Habits\n",
            encoding="utf-8",
        )

        note_path = ensure_daily_note(self.config, date(2026, 3, 30))
        first_content = note_path.read_text(encoding="utf-8")
        ensure_daily_note(self.config, date(2026, 3, 30))
        second_content = note_path.read_text(encoding="utf-8")

        self.assertIn("- [ ] carry me", first_content)
        self.assertEqual(first_content, second_content)

    def test_insert_new_task_places_new_tasks_below_carried_forward_items(self) -> None:
        note_path = daily_note_path(self.config, date(2026, 3, 30))
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text(
            "## Notes\n\n## Tasks\n- [ ] carried one\n- [ ] carried two\n- [ ] older current task\n\n## Habits\n",
            encoding="utf-8",
        )

        insert_new_task(
            note_path,
            self.make_capture("new task"),
            created_today=True,
            carry_forward_count=2,
        )
        sections = parse_sections(note_path.read_text(encoding="utf-8"))

        self.assertEqual(
            sections["## Tasks"],
            [
                "- [ ] carried one",
                "- [ ] carried two",
                "- [ ] new task",
                "- [ ] older current task",
            ],
        )

    def test_apply_route_falls_back_to_note_when_habit_does_not_match(self) -> None:
        note_path = daily_note_path(self.config, date(2026, 3, 30))
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text(
            "## Notes\n\n## Tasks\n\n## Habits\n- [ ] Read\n",
            encoding="utf-8",
        )

        outcome = apply_route(
            note_path,
            self.make_capture("drink water"),
            RouteDecision(target_type="habit_check", matched_habit_text="Water"),
            created_today=False,
            carry_forward_count=0,
        )
        sections = parse_sections(note_path.read_text(encoding="utf-8"))

        self.assertEqual(outcome, "note")
        self.assertEqual(sections["## Habits"], ["- [ ] Read"])
        self.assertEqual(sections["## Notes"], ["- 10:30: drink water"])

    def test_update_habit_checkbox_marks_matching_habit(self) -> None:
        note_path = daily_note_path(self.config, date(2026, 3, 30))
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text(
            "## Notes\n\n## Tasks\n\n## Habits\n- [ ] Drink Water\n",
            encoding="utf-8",
        )

        updated = update_habit_checkbox(note_path, "Drink Water")
        sections = parse_sections(note_path.read_text(encoding="utf-8"))

        self.assertTrue(updated)
        self.assertEqual(sections["## Habits"], ["- [x] Drink Water"])

    def test_write_capture_log_inserts_newest_entry_first_for_same_day(self) -> None:
        log_path = self.vault_path / "capture-log.md"
        write_capture_log(log_path, self.make_capture("first", hour=9, minute=0))
        write_capture_log(log_path, self.make_capture("second", hour=11, minute=0))

        self.assertEqual(
            log_path.read_text(encoding="utf-8"),
            "## 2026-03-30\n- 11:00 [text] second\n- 09:00 [text] first\n",
        )

    def test_write_capture_log_prepends_newer_day(self) -> None:
        log_path = self.vault_path / "capture-log.md"
        earlier = CaptureRequest(
            timestamp=datetime(2026, 3, 29, 11, 0, tzinfo=ZoneInfo(self.config.timezone_name)),
            raw_text="older day",
            normalized_text="older day",
            source_type="text",
        )
        later = self.make_capture("newer day", hour=11, minute=0)

        write_capture_log(log_path, earlier)
        write_capture_log(log_path, later)

        self.assertEqual(
            log_path.read_text(encoding="utf-8"),
            "## 2026-03-30\n- 11:00 [text] newer day\n\n## 2026-03-29\n- 11:00 [text] older day\n",
        )


if __name__ == "__main__":
    unittest.main()
