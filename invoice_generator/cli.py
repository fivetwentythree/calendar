from __future__ import annotations

import argparse
import datetime as dt
from typing import List

from .fetcher import CalendarFetcher
from .parser import parse_event_title
from .aggregator import Aggregator
from .invoice import InvoiceRenderer


def run(calendar_id: str, month: str):
    start = dt.datetime.fromisoformat(month + "-01")
    end = (start + dt.timedelta(days=32)).replace(day=1)

    fetcher = CalendarFetcher(calendar_id)
    events = fetcher.fetch_events(start, end)

    parsed = []
    for ev in events:
        result = parse_event_title(ev.summary)
        if result:
            parsed.append(result)

    aggregator = Aggregator(parsed)
    items = aggregator.group_by_property_month()

    renderer = InvoiceRenderer()
    renderer.render_invoices(items)


def main():
    parser = argparse.ArgumentParser(description="AI Invoice Generator")
    parser.add_argument("calendar_id", help="Google Calendar ID")
    parser.add_argument("month", help="Month in YYYY-MM format")
    args = parser.parse_args()
    run(args.calendar_id, args.month)


if __name__ == "__main__":
    main()
