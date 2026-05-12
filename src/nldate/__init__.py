import re
from datetime import date

from dateutil import parser
from dateutil.relativedelta import relativedelta

WORD_TO_NUM = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}

DAYS_OF_WEEK = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def _apply_delta(
    reference: date, matches: list[tuple[str, str]], multiplier: int
) -> date:
    delta = relativedelta()
    for num_str, unit in matches:
        num = int(num_str)
        if unit in ("day", "days"):
            delta += relativedelta(days=num * multiplier)
        elif unit in ("week", "weeks"):
            delta += relativedelta(weeks=num * multiplier)
        elif unit in ("month", "months"):
            delta += relativedelta(months=num * multiplier)
        else:
            delta += relativedelta(years=num * multiplier)
    return reference + delta


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    s_lower = s.lower()  # add this

    multiplier = 1
    if "before" in s_lower or "ago" in s_lower:
        multiplier = -1

    s_normalized = s_lower  # use s_lower here
    for word, num in WORD_TO_NUM.items():
        s_normalized = re.sub(
            rf"\b{word}\b", str(num), s_normalized, flags=re.IGNORECASE
        )

    matches = re.findall(r"(\d+)\s+(days?|weeks?|months?|years?)", s_normalized)

    months = {
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    }

    has_specific_date = any(month in s_lower for month in months) or bool(
        re.search(r"\b\d{4}\b", s)
    )

    if has_specific_date:
        date_match = re.search(r"(before|after)(.*)", s_lower, re.IGNORECASE)
        if date_match:
            date_str = date_match.group(2).strip()
        else:
            date_str = s_lower
        reference_date = parser.parse(date_str).date()

        if matches:
            new_date = _apply_delta(reference_date, matches, multiplier)
        else:
            new_date = reference_date

    else:
        if "day after tomorrow" in s_lower:
            reference = today + relativedelta(days=2)
        elif "day before yesterday" in s_lower:
            reference = today + relativedelta(days=-2)
        elif "yesterday" in s_lower:
            reference = today + relativedelta(days=-1)
        elif "tomorrow" in s_lower:
            reference = today + relativedelta(days=1)
        elif "next" in s_lower:
            day_match = re.search(r"next (\w+)", s_lower)
            target_day = DAYS_OF_WEEK[day_match.group(1)]  # type: ignore
            days_ahead = target_day - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return today + relativedelta(days=days_ahead)
        elif "last" in s_lower:
            day_match = re.search(r"last (\w+)", s_lower)
            target_day = DAYS_OF_WEEK[day_match.group(1)]  # type: ignore
            days_behind = today.weekday() - target_day
            if days_behind <= 0:
                days_behind += 7
            return today + relativedelta(days=-days_behind)
        else:
            reference = today

        if matches:
            new_date = _apply_delta(reference, matches, multiplier)
        else:
            new_date = reference

    return new_date
