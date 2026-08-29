from __future__ import annotations

import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

BASE_DIR = Path(__file__).resolve().parent.parent
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
CREDENTIALS_FILE = Path(os.getenv("GOOGLE_CREDENTIALS_FILE", BASE_DIR / "credentials.json"))
TOKEN_FILE = Path(os.getenv("GOOGLE_TOKEN_FILE", BASE_DIR / "token.json"))
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "primary")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")


def authorize():
    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(
            "Google OAuth credentials.json is missing. Calendar integration is optional; "
            "add OAuth desktop credentials to enable it."
        )
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN_FILE.write_text(creds.to_json())
    return creds


def credentials():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if not creds or not creds.valid:
        creds = authorize()
    return creds


def service():
    return build("calendar", "v3", credentials=credentials())


def upcoming_events(days: int = 7) -> list[dict]:
    from datetime import datetime, timedelta
    now = datetime.now().astimezone()
    end = now + timedelta(days=days)
    response = service().events().list(
        calendarId=CALENDAR_ID,
        timeMin=now.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    return response.get("items", [])


def create_planned_event(title: str, start_iso: str, end_iso: str,
                         category: str, description: str = "") -> dict:
    event = {
        "summary": f"[TM] {title}",
        "description": f"Time Manager | category={category}\n{description}".strip(),
        "start": {"dateTime": start_iso, "timeZone": TIMEZONE},
        "end": {"dateTime": end_iso, "timeZone": TIMEZONE},
        "extendedProperties": {"private": {"time_manager": "true", "category": category}},
    }
    return service().events().insert(calendarId=CALENDAR_ID, body=event).execute()
