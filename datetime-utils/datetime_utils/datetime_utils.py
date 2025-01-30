from datetime import datetime, time, timezone


def now_utc() -> datetime:
    """
    Time in UTC, timezone-aware.
    """
    return datetime.now(tz=timezone.utc)


def now() -> datetime:
    """
    Time in the current timezone, timezone-aware.
    """
    return datetime.now().astimezone()


def timestamp_to_utc_date(ts: int) -> datetime:
    return datetime.fromtimestamp(ts).astimezone(timezone.utc)


def utc_date_to_timestamp(date: datetime) -> int:
    return int(date.astimezone(timezone.utc).timestamp())


def iso_string_to_date(text: str) -> datetime:
    """
    Examples:
        iso_string_to_date("2024-02-06T17:20:32")
        >>> datetime.datetime(2024, 2, 6, 17, 20, 32)

        iso_string_to_date("2024-02-06T17:20:32Z")
        >>> datetime.datetime(2024, 2, 6, 17, 20, 32, tzinfo=datetime.timezone.utc)
    """
    return datetime.fromisoformat(text)


def is_naive(d: datetime | time):
    # Docs: https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        return True
    return False
