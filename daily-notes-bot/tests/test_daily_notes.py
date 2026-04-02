from datetime import date, datetime, timedelta, timezone
import asyncio
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
import unittest

from daily_notes_bot.config import Config
from daily_notes_bot.models import CaptureRequest, RouteDecision
from daily_notes_bot.services.capture_log import write_capture_log
from daily_notes_bot.services.daily_notes import (
    DEFAULT_HABITS,
    daily_note_path,
    ensure_daily_note,
    insert_task,
    update_habit_checkbox,
)
from daily_notes_bot.services.markdown import parse_sections
from daily_notes_bot.services.routing import route_capture
from daily_notes_bot.telegram.handlers import handle_message, process_message


class DailyNotesBotTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = TemporaryDirectory()
        self.vault_path = Path(self.temp_dir.name) / "vault"
        self.config = Config(
            telegram_bot_token="token",
            allowed_user_id=1,
            obsidian_vault_path=self.vault_path,
            daily_notes_dir=Path("5.Daily Notes"),
            capture_log_filename="capture-log.md",
            timezone_name="America/Sao_Paulo",
            gemini_api_key="test-key",
            gemini_model="gemini-2.5-flash",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    @property
    def sao_paulo_offset(self):
        return timezone(timedelta(hours=-3))

    def make_capture(self, text: str, hour: int = 10, minute: int = 30, source_type: str = "text") -> CaptureRequest:
        return CaptureRequest(
            timestamp=datetime(2026, 3, 30, hour, minute, tzinfo=self.sao_paulo_offset),
            raw_text=text,
            normalized_text=text,
            source_type=source_type,
        )

    def test_ensure_daily_note_creates_new_template_with_default_habits(self) -> None:
        note_path = ensure_daily_note(self.config, date(2026, 3, 30))
        content = note_path.read_text(encoding="utf-8")
        sections = parse_sections(content)

        self.assertTrue(content.startswith("# 2026-03-30\n"))
        self.assertEqual(sections["## Notes"], [])
        self.assertEqual(sections["## Today"], [])
        self.assertEqual(sections["## Scheduled"], [])
        self.assertEqual(sections["## Project Tasks"], [])
        self.assertEqual(sections["## Habits"], [f"- [ ] {habit}" for habit in DEFAULT_HABITS])

    def test_new_daily_note_does_not_carry_forward_previous_open_tasks(self) -> None:
        previous = daily_note_path(self.config, date(2026, 3, 29))
        previous.parent.mkdir(parents=True, exist_ok=True)
        previous.write_text(
            "\n".join(
                [
                    "# 2026-03-29",
                    "",
                    "## Notes",
                    "",
                    "## Today",
                    "- [ ] carry me",
                    "",
                    "## Scheduled",
                    "- [ ] 19:00 keep me",
                    "",
                    "## Project Tasks",
                    "- [ ] [[AZ-204 Dashboard]]",
                    "",
                    "## Habits",
                    "- [ ] H\u00b2O 1.5L",
                    "",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        note_path = ensure_daily_note(self.config, date(2026, 3, 30))
        sections = parse_sections(note_path.read_text(encoding="utf-8"))

        self.assertEqual(sections["## Today"], [])
        self.assertEqual(sections["## Scheduled"], [])
        self.assertEqual(sections["## Project Tasks"], [])

    def test_insert_task_places_untimed_task_in_today(self) -> None:
        note_path = ensure_daily_note(self.config, date(2026, 3, 30))

        insert_task(
            note_path,
            RouteDecision(
                target_type="task",
                target_date=date(2026, 3, 30),
                target_section="## Today",
                task_text="Review flashcards",
            ),
        )

        sections = parse_sections(note_path.read_text(encoding="utf-8"))
        self.assertEqual(sections["## Today"], ["- [ ] Review flashcards"])

    def test_insert_task_places_linked_task_in_project_tasks(self) -> None:
        note_path = ensure_daily_note(self.config, date(2026, 3, 30))

        insert_task(
            note_path,
            RouteDecision(
                target_type="task",
                target_date=date(2026, 3, 30),
                target_section="## Project Tasks",
                task_text="Review [[AZ-204 Dashboard]]",
            ),
        )

        sections = parse_sections(note_path.read_text(encoding="utf-8"))
        self.assertEqual(sections["## Project Tasks"], ["- [ ] Review [[AZ-204 Dashboard]]"])

    def test_insert_task_places_timed_task_in_scheduled(self) -> None:
        note_path = ensure_daily_note(self.config, date(2026, 3, 30))

        insert_task(
            note_path,
            RouteDecision(
                target_type="task",
                target_date=date(2026, 3, 30),
                target_section="## Scheduled",
                scheduled_time="19:00",
                task_text="Budget review with Mini",
            ),
        )

        sections = parse_sections(note_path.read_text(encoding="utf-8"))
        self.assertEqual(sections["## Scheduled"], ["- [ ] 19:00 Budget review with Mini"])

    def test_update_habit_checkbox_matches_default_h2o_label(self) -> None:
        note_path = ensure_daily_note(self.config, date(2026, 3, 30))

        updated = update_habit_checkbox(note_path, "h2o 1.5l")
        sections = parse_sections(note_path.read_text(encoding="utf-8"))

        self.assertTrue(updated)
        self.assertEqual(sections["## Habits"][0], "- [x] H\u00b2O 1.5L")

    def test_route_capture_uses_default_habit_template_when_today_note_is_missing(self) -> None:
        route = route_capture(self.make_capture("dexilant jejum"), self.config)

        self.assertEqual(route.target_type, "habit_check")
        self.assertEqual(route.target_date, date(2026, 3, 30))
        self.assertEqual(route.matched_habit_text, "Dexilant jejum")

    def test_route_capture_maps_natural_language_future_task_to_today_section(self) -> None:
        with patch(
            "daily_notes_bot.services.routing._route_with_gemini",
            return_value={
                "intent": "task",
                "task_text": "Do lab: deploy API to App Service",
                "target_date": "2026-04-08",
                "target_time": None,
            },
        ):
            route = route_capture(self.make_capture("next Wednesday do lab"), self.config)

        self.assertEqual(route.target_type, "task")
        self.assertEqual(route.target_date, date(2026, 4, 8))
        self.assertEqual(route.target_section, "## Today")
        self.assertIsNone(route.scheduled_time)
        self.assertEqual(route.task_text, "Do lab: deploy API to App Service")

    def test_route_capture_maps_timed_task_to_scheduled(self) -> None:
        with patch(
            "daily_notes_bot.services.routing._route_with_gemini",
            return_value={
                "intent": "task",
                "task_text": "Budget review with Mini",
                "target_date": "2026-04-08",
                "target_time": "19:00",
            },
        ):
            route = route_capture(self.make_capture("next Wednesday at 7pm budget review"), self.config)

        self.assertEqual(route.target_type, "task")
        self.assertEqual(route.target_section, "## Scheduled")
        self.assertEqual(route.scheduled_time, "19:00")

    def test_route_capture_preserves_wiki_links_and_routes_to_project_tasks(self) -> None:
        with patch(
            "daily_notes_bot.services.routing._route_with_gemini",
            return_value={
                "intent": "task",
                "task_text": "Review [[AZ-204 Dashboard]]",
                "target_date": "2026-04-08",
                "target_time": None,
            },
        ):
            route = route_capture(self.make_capture("review dashboard next Wednesday"), self.config)

        self.assertEqual(route.target_type, "task")
        self.assertEqual(route.target_section, "## Project Tasks")
        self.assertEqual(route.task_text, "Review [[AZ-204 Dashboard]]")

    def test_route_capture_falls_back_to_note_for_ambiguous_ai_output(self) -> None:
        with patch(
            "daily_notes_bot.services.routing._route_with_gemini",
            return_value={
                "intent": "task",
                "task_text": "Unscheduled task",
                "target_date": "not-a-date",
                "target_time": None,
            },
        ):
            route = route_capture(self.make_capture("sometime maybe do this"), self.config)

        self.assertEqual(route.target_type, "note_entry")
        self.assertEqual(route.target_date, date(2026, 3, 30))

    def test_process_message_creates_and_updates_future_daily_note(self) -> None:
        capture = self.make_capture("next Wednesday do lab")
        message = SimpleNamespace()

        with patch(
            "daily_notes_bot.telegram.handlers.normalize_capture_from_message",
            new=AsyncMock(return_value=capture),
        ), patch(
            "daily_notes_bot.telegram.handlers.route_capture",
            return_value=RouteDecision(
                target_type="task",
                target_date=date(2026, 4, 8),
                target_section="## Project Tasks",
                task_text="Do lab: deploy API to App Service for [[AZ-204 Dashboard]]",
            ),
        ):
            result = self._run_async(process_message(message, self.config))

        future_path = daily_note_path(self.config, date(2026, 4, 8))
        sections = parse_sections(future_path.read_text(encoding="utf-8"))

        self.assertEqual(result, "task")
        self.assertTrue(future_path.exists())
        self.assertEqual(
            sections["## Project Tasks"],
            ["- [ ] Do lab: deploy API to App Service for [[AZ-204 Dashboard]]"],
        )

    def test_handle_message_reads_config_from_context_application(self) -> None:
        message = SimpleNamespace(text="capture", voice=None, reply_text=AsyncMock())
        update = SimpleNamespace(
            effective_message=message,
            effective_user=SimpleNamespace(id=1),
        )
        context = SimpleNamespace(
            application=SimpleNamespace(bot_data={"config": self.config}),
        )

        with patch(
            "daily_notes_bot.telegram.handlers.process_message",
            new=AsyncMock(return_value="task"),
        ) as process_message_mock:
            self._run_async(handle_message(update, context))

        process_message_mock.assert_awaited_once_with(message, self.config)
        message.reply_text.assert_awaited_once_with("Captured to task.")

    def test_write_capture_log_prepends_newer_day(self) -> None:
        log_path = self.vault_path / "capture-log.md"
        earlier = CaptureRequest(
            timestamp=datetime(2026, 3, 29, 11, 0, tzinfo=self.sao_paulo_offset),
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

    def _run_async(self, awaitable):
        return asyncio.run(awaitable)


if __name__ == "__main__":
    unittest.main()
