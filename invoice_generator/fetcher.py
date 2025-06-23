from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from typing import List

from google.oauth2 import service_account
from googleapiclient.discovery import build

from .config import SERVICE_ACCOUNT_FILE

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


@dataclass
class CalendarEvent:
    summary: str
    start: dt.datetime
    end: dt.datetime


class CalendarFetcher:
    def __init__(self, calendar_id: str):
        self.calendar_id = calendar_id
        self.service = self._build_service()

    def _build_service(self):
        if not SERVICE_ACCOUNT_FILE.exists():
            raise FileNotFoundError("Service account file not found")
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        return build("calendar", "v3", credentials=creds, cache_discovery=False)

    def fetch_events(
        self, time_min: dt.datetime, time_max: dt.datetime
    ) -> List[CalendarEvent]:
        events_result = (
            self.service.events()
            .list(
                calendarId=self.calendar_id,
                timeMin=time_min.isoformat(),
                timeMax=time_max.isoformat(),
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = []
        for item in events_result.get("items", []):
            start = item["start"].get("dateTime") or item["start"].get("date")
            end = item["end"].get("dateTime") or item["end"].get("date")
            events.append(
                CalendarEvent(
                    summary=item.get("summary", ""),
                    start=dt.datetime.fromisoformat(start),
                    end=dt.datetime.fromisoformat(end),
                )
            )
        return events
