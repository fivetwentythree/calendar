from __future__ import annotations

import datetime as dt
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedEvent:
    property: str
    date: dt.date
    hours: float


EVENT_REGEX = re.compile(
    r"(?P<property>[\w\s]+)\s+(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<hours>[\d.]+)h",
    re.IGNORECASE,
)


def parse_event_title(title: str) -> Optional[ParsedEvent]:
    match = EVENT_REGEX.search(title)
    if not match:
        return None
    prop = match.group("property").strip()
    date = dt.date.fromisoformat(match.group("date"))
    hours = float(match.group("hours"))
    return ParsedEvent(property=prop, date=date, hours=hours)
