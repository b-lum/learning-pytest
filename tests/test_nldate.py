from datetime import date
from nldate import parse


def test_days_before_specific_date():
    assert parse("5 days before December 1st, 2025") == date(2025, 11, 26)


def test_next_tuesday():
    today = date(2026, 5, 11)  # a Monday
    assert parse("next Tuesday", today=today) == date(2026, 5, 12)


def test_in_3_days():
    today = date(2026, 5, 11)
    assert parse("in 3 days", today=today) == date(2026, 5, 14)


def test_year_and_months_after_yesterday():
    today = date(2026, 5, 11)
    assert parse("1 year and 2 months after yesterday", today=today) == date(
        2027, 7, 10
    )


def test_two_weeks_from_tomorrow():
    today = date(2026, 5, 11)
    assert parse("two weeks from tomorrow", today=today) == date(2026, 5, 26)


def test_today():
    today = date(2026, 5, 11)
    assert parse("today", today=today) == date(2026, 5, 11)


def test_tomorrow():
    today = date(2026, 5, 11)
    assert parse("tomorrow", today=today) == date(2026, 5, 12)


def test_yesterday():
    today = date(2026, 5, 11)
    assert parse("yesterday", today=today) == date(2026, 5, 10)


def test_days_after_specific_date():
    assert parse("5 days after December 1st, 2025") == date(2025, 12, 6)


def test_plain_date():
    assert parse("December 1st, 2025") == date(2025, 12, 1)
