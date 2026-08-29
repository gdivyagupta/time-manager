from __future__ import annotations

import re
from dataclasses import dataclass

CATEGORY_ALIASES = {
    "canada": "Canada Career",
    "job search": "Canada Career",
    "applications": "Canada Career",
    "career": "Canada Career",
    "ai": "AI Technical",
    "technical": "AI Technical",
    "coding": "AI Technical",
    "portfolio": "Portfolio",
    "project": "Portfolio",
    "research": "Research",
    "papers": "Research",
    "instagram": "Personal Brand",
    "linkedin": "Personal Brand",
    "content": "Personal Brand",
    "networking": "Networking",
    "tutoring": "Income",
    "tuition": "Income",
    "exercise": "Health",
    "gym": "Health",
    "recovery": "Recovery",
}

@dataclass
class Command:
    intent: str
    payload: dict
    response: str


def classify_category(text: str) -> str | None:
    low = text.lower()
    for alias, category in sorted(CATEGORY_ALIASES.items(), key=lambda x: len(x[0]), reverse=True):
        if alias in low:
            return category
    return None


def parse(text: str) -> Command:
    raw = text.strip()
    low = raw.lower()

    log_match = re.search(r"\b(?:log|record|track)\s+([0-9]+(?:\.[0-9]+)?)\s*(?:hours?|hrs?|h)\b(?:\s+of)?\s*(.*)", low)
    if log_match:
        hours = float(log_match.group(1))
        activity = log_match.group(2).strip() or "Unspecified activity"
        energy = "Medium"
        for value in ("high", "medium", "low"):
            if re.search(rf"\b{value}\s+energy\b|\b{value}\b", activity):
                energy = value.title()
                activity = re.sub(rf"\b{value}\s+energy\b|\b{value}\b", "", activity).strip()
                break
        return Command("log", {"hours": hours, "activity": activity,
                                "category": classify_category(activity) or "Maintenance",
                                "energy": energy}, "")

    if any(x in low for x in ("weekly summary", "week summary", "weekly review")):
        return Command("weekly_summary", {}, "I can summarise the week from your stored logs.")

    if any(x in low for x in ("plan my day", "what should i work on", "what should i do")):
        return Command("plan_day", {},
                       "Prioritise high-energy Canada career, AI technical, and portfolio work. "
                       "Use low-energy windows for content/admin and protect evening recovery after long commutes.")

    if "move" in low or "reschedule" in low:
        return Command("reschedule", {"text": raw},
                       "I need the source block and the new date/time to reschedule a block safely.")

    return Command("unknown", {},
                   "Try 'log 90 minutes of research medium energy', 'weekly summary', or 'plan my day'.")
