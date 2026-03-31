from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CaptureRequest:
    timestamp: datetime
    raw_text: str
    normalized_text: str
    source_type: str


@dataclass(frozen=True)
class RouteDecision:
    target_type: str
    matched_habit_text: str | None = None
