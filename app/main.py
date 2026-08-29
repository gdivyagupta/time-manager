from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .agent import parse
from .db import add_log, add_plan, init_db, recent_logs, weekly_rollup, plans_for_range
from .planner import validate_no_overlap

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "user.example.json"
TEMPLATES = BASE_DIR / "app" / "templates"

app = FastAPI(title="Time Manager")
templates = Jinja2Templates(directory=str(TEMPLATES))
init_db()


def config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "config": config(),
            "logs": recent_logs(),
            "plans": plans_for_range(week_start.isoformat(), week_end.isoformat()),
            "summary": weekly_rollup(week_start.isoformat(), week_end.isoformat()),
        },
    )


@app.post("/log")
def log_time(activity: str = Form(...), hours: float = Form(...),
             category: str = Form(...), energy: str = Form(...),
             date_value: str = Form(""), notes: str = Form("")):
    if hours <= 0:
        raise ValueError("Hours must be greater than zero")
    add_log(activity, category, hours, energy, date_value or date.today().isoformat(), "manual", notes)
    return RedirectResponse("/", status_code=303)


@app.post("/plan")
def plan_block(title: str = Form(...), date_value: str = Form(...),
              start: str = Form(...), end: str = Form(...),
              category: str = Form(...), energy: str = Form(...)):
    if start >= end:
        raise ValueError("End time must be after start time")
    new_block = {"date": date_value, "start": start, "end": end, "title": title}
    existing = plans_for_range(date_value, date_value)
    conflicts = validate_no_overlap(existing + [new_block])
    if conflicts:
        raise ValueError(conflicts[0])
    add_plan(title, date_value, start, end, category, energy)
    return RedirectResponse("/", status_code=303)


@app.post("/chat")
def chat(message: str = Form(...)):
    command = parse(message)
    if command.intent == "log":
        p = command.payload
        add_log(p["activity"], p["category"], p["hours"], p["energy"], date.today().isoformat(), "chat")
        return {"message": f"Logged {p['hours']}h of {p['activity']} → {p['category']} ({p['energy']} energy)."}
    if command.intent == "weekly_summary":
        today = date.today()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        s = weekly_rollup(start.isoformat(), end.isoformat())
        lines = [f"{r['category']}: {r['hours']}h" for r in s["by_category"]]
        return {"message": "This week's logged time:\n" + ("\n".join(lines) if lines else "No logs yet.")}
    return {"message": command.response}


@app.get("/api/summary")
def api_summary():
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return weekly_rollup(start.isoformat(), end.isoformat())
