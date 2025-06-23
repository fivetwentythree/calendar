from __future__ import annotations

import calendar
import datetime as dt
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from .parser import ParsedEvent
from .config import config


@dataclass
class InvoiceItem:
    property: str
    month: str
    hours: float
    rate: float
    total: float


class Aggregator:
    def __init__(self, events: Iterable[ParsedEvent]):
        self.events = events

    def group_by_property_month(self) -> List[InvoiceItem]:
        grouped: Dict[Tuple[str, str], float] = defaultdict(float)
        for event in self.events:
            month = event.date.strftime("%Y-%m")
            key = (event.property, month)
            grouped[key] += event.hours
        items = []
        for (prop, month), hours in grouped.items():
            rate = config.rate_table.get(prop, 0)
            total = hours * rate
            items.append(InvoiceItem(prop, month, hours, rate, total))
        return items
