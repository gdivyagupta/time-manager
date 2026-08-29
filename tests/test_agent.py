from app.agent import parse


def test_log_parser():
    result = parse("Log 1.5 hours of portfolio high energy")
    assert result.intent == "log"
    assert result.payload["hours"] == 1.5
    assert result.payload["category"] == "Portfolio"
    assert result.payload["energy"] == "High"


def test_weekly_summary():
    assert parse("weekly summary").intent == "weekly_summary"


def test_plan_day():
    result = parse("what should I work on?")
    assert result.intent == "plan_day"
