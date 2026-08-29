from __future__ import annotations

from dataclasses import dataclass
from datetime import date, time, timedelta

@dataclass(frozen=True)
class Window:
    day: str
    start: str
    end: str
    energy: str
    mode: str
    note: str = ""

# These are reusable examples rather than hard-coded personal rules.
DEFAULT_WINDOW_RULES = {
    "high": {"Canada Career", "AI Technical", "Portfolio", "Research", "Networking"},
    "medium": {"Personal Brand", "Income", "Planning"},
    "low": {"Recovery", "Maintenance"},
}


def category_energy_score(category: str, energy: str) -> int:
    if category in DEFAULT_WINDOW_RULES.get(energy.lower(), set()):
        return 3
    return 1


def recommend_category(available_energy: str, candidates: list[dict]) -> list[dict]:
    """Return candidates ranked by fit to the available energy."""
    scored = []
    for candidate in candidates:
        score = category_energy_score(candidate["category"], available_energy)
        score += int(candidate.get("priority", 3))
        scored.append({**candidate, "fit_score": score})
    return sorted(scored, key=lambda x: x["fit_score"], reverse=True)


def validate_no_overlap(blocks: list[dict]) -> list[str]:
    """Detect same-day overlapping proposed blocks."""
    errors = []
    by_day: dict[str, list[dict]] = {}
    for block in blocks:
        by_day.setdefault(block["date"], []).append(block)
    for day, items in by_day.items():
        items = sorted(items, key=lambda x: x["start"])
        for left, right in zip(items, items[1:]):
            if left["end"] > right["start"]:
                errors.append(f"Overlap on {day}: {left['title']} / {right['title']}")
    return errors
