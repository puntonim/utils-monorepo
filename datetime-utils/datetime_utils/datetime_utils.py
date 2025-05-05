"""
** DATETIME UTILS **
====================

Note: there are a few more utils about WORKING DAYS AND HOLIDAYS in `ibkr-etf-trade-ideas`.

```py
import datetime_utils

datetime_utils.now_utc()
```
"""

from datetime import datetime, time, timezone

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "convert_all_isoformat_values_in_dict_to_datetime",
    "days_ago",
    "days_to_go",
    "is_naive",
    "iso_string_to_date",
    "minpkm_base10_to_base60",
    "mps_to_minpkm",
    "now",
    "now_utc",
    "short_format_date",
    "shortest_format_date",
    "timestamp_to_utc_date",
    "utc_date_to_timestamp",
]


SECS_IN_1_DAY = 60 * 60 * 24


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


def short_format_date(date: datetime):
    """
    Eg. 2023-09-02 15:36:03 GMT.
    """
    return date.strftime("%Y-%m-%d %H:%M:%S %Z")


def shortest_format_date(date: datetime):
    """
    Eg. 05/01/23 08:09.
    """
    # Convert to local timezone.
    date = date.astimezone()
    return date.strftime("%d/%m/%y %H:%M")


def days_ago(d: datetime, n_decimal_digits: int = 1):
    """
    Example:
        >>> days_ago(datetime(2023, 11, 20, 7, 0, 0, tzinfo=timezone.utc))
        4.1
        >>> days_ago(datetime(2023, 11, 20, 7, 0, 0, tzinfo=timezone.utc), n_decimal_digits=5)
        4.10828
    """
    if is_naive(d):
        raise TypeError("Naive datetime not supported")
    return round((now_utc() - d).total_seconds() / SECS_IN_1_DAY, n_decimal_digits)


def days_to_go(d: datetime, n_decimal_digits: int = 1):
    """
    Example:
        >>> days_to_go(datetime(2023, 11, 20, 7, 0, 0, tzinfo=timezone.utc))
        4.1
        >>> days_to_go(datetime(2023, 11, 20, 7, 0, 0, tzinfo=timezone.utc), n_decimal_digits=5)
        4.10828
    """
    if is_naive(d):
        raise TypeError("Naive datetime not supported")
    return round((d - now_utc()).total_seconds() / SECS_IN_1_DAY, n_decimal_digits)


def convert_all_isoformat_values_in_dict_to_datetime(data: dict):
    """
    Given a dict like:
        {
            "symbol": "LIT",
            "price": 34.5,
            "buy_date": "2022-01-19T00:00:00+00:00",
        }
     it converts "buy_date" to a datetime instance.

    Note: it tries to convert all values (the key name does not matter).
    """
    for k, v in data.items():
        # Do recurse inside dicts.
        if isinstance(v, dict):
            data[k] = convert_all_isoformat_values_in_dict_to_datetime(v)
            continue
        # Do recurse inside lists.
        if isinstance(v, list):
            v_converted = list()
            for item in v:
                v_converted.append(
                    convert_all_isoformat_values_in_dict_to_datetime(item)
                )
            data[k] = v_converted
            continue
        # Try to convert to datetime.
        try:
            data[k] = datetime.fromisoformat(v)
        except (TypeError, ValueError) as exc:
            pass
    return data


def minpkm_base10_to_base60(x: float) -> str:
    """
    Eg. 5.05 min/km -> 5:03 min/km.
        minpkm_base10_to_base60(5.05) -> "5:03".
    """
    int_val = floor(x)
    dec_val = x - int_val
    return f"{int_val}:{round(dec_val * 60):02d}"


def mps_to_minpkm(x: float) -> float:
    """
    Eg. 3.3 m/s -> 5.05 min/km.
        mps_to_minpkm(3.3) -> 5.05
    Note that 5.05 min/km could then be converted to base60 to 5:03 min/km.
    """
    return 60 / (x * 3.6)
