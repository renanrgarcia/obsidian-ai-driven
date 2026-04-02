from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class CaptureRequest:
    timestamp: datetime
    raw_text: str
    normalized_text: str
    source_type: str


@dataclass(frozen=True)
class RouteDecision:
    target_type: str
    target_date: date
    target_section: str | None = None
    scheduled_time: str | None = None
    task_text: str | None = None
    matched_habit_text: str | None = None
