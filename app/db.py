from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "data" / "time_manager.db"))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS time_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  activity TEXT NOT NULL,
  category TEXT NOT NULL,
  hours REAL NOT NULL CHECK(hours > 0),
  energy TEXT NOT NULL,
  date TEXT,
  source TEXT NOT NULL DEFAULT 'manual',
  notes TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS plans (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  date TEXT NOT NULL,
  start TEXT NOT NULL,
  end TEXT NOT NULL,
  category TEXT NOT NULL,
  energy TEXT NOT NULL,
  source TEXT NOT NULL DEFAULT 'manual',
  calendar_event_id TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_logs_date ON time_logs(date);
CREATE INDEX IF NOT EXISTS idx_plans_date ON plans(date);
"""


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA)


def add_log(activity: str, category: str, hours: float, energy: str,
            date: str | None = None, source: str = "manual", notes: str = "") -> int:
    with connect() as conn:
        cur = conn.execute(
            """INSERT INTO time_logs(activity,category,hours,energy,date,source,notes)
               VALUES(?,?,?,?,?,?,?)""",
            (activity, category, hours, energy, date, source, notes),
        )
        return int(cur.lastrowid)


def add_plan(title: str, date: str, start: str, end: str, category: str,
             energy: str, source: str = "manual") -> int:
    with connect() as conn:
        cur = conn.execute(
            """INSERT INTO plans(title,date,start,end,category,energy,source)
               VALUES(?,?,?,?,?,?,?)""",
            (title, date, start, end, category, energy, source),
        )
        return int(cur.lastrowid)


def recent_logs(limit: int = 50) -> list[dict[str, Any]]:
    with connect() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM time_logs ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()]


def plans_for_range(start_date: str, end_date: str) -> list[dict[str, Any]]:
    with connect() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM plans WHERE date BETWEEN ? AND ? ORDER BY date,start",
            (start_date, end_date),
        ).fetchall()]


def weekly_rollup(start_date: str, end_date: str) -> dict[str, Any]:
    with connect() as conn:
        rows = [dict(r) for r in conn.execute(
            """SELECT category, ROUND(SUM(hours),2) hours
               FROM time_logs WHERE date BETWEEN ? AND ?
               GROUP BY category ORDER BY hours DESC""",
            (start_date, end_date),
        ).fetchall()]
        total = conn.execute(
            "SELECT COALESCE(SUM(hours),0) FROM time_logs WHERE date BETWEEN ? AND ?",
            (start_date, end_date),
        ).fetchone()[0]
    return {"total_hours": round(float(total), 2), "by_category": rows}
