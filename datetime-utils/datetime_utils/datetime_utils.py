"""
** DATETIME UTILS **
====================

Note: there are a few more utils about WORKING DAYS AND HOLIDAYS in `ibkr-etf-trade-ideas`.

```py
import datetime_utils

datetime_utils.now_utc()
```
"""

from datetime import date, datetime, time, timedelta, timezone, tzinfo
from zoneinfo import ZoneInfo

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "convert_all_isoformat_values_in_dict_to_datetime",
    "days_ago",
    "days_to_go",
    "is_naive",
    "iso_string_to_datetime",
    "now",
    "now_utc",
    "short_format_date",
    "shortest_format_date",
    "timestamp_to_utc_datetime",
    "utc_date_to_timestamp",
    "seconds_to_hh_mm_ss",
    "seconds_to_hh_mm",
    "parse_datetime_arg",
    "replace_timezone",
    "convert_to_timezone",
    "local_timezone",
    "date_to_datetime",
    "parse_date_arg",
]


class _DEFAULT:
    pass


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


def timestamp_to_utc_datetime(ts: int) -> datetime:
    return datetime.fromtimestamp(ts).astimezone(timezone.utc)


def utc_date_to_timestamp(d: datetime) -> int:
    return int(d.astimezone(timezone.utc).timestamp())


def iso_string_to_datetime(text: str) -> datetime:
    """
    Examples:
        iso_string_to_datetime("2024-02-06T17:20:32")
        >>> datetime.datetime(2024, 2, 6, 17, 20, 32)

        iso_string_to_datetime("2024-02-06T17:20:32+00:00")
        >>> datetime.datetime(2024, 2, 6, 17, 20, 32, tzinfo=datetime.timezone.utc)
    """
    return datetime.fromisoformat(text)


def date_to_datetime(d: date) -> datetime:
    """
    Convert a date to a datetime by adding the hour, min and secs set to 0 and the
     local timezone.
    """
    return replace_timezone(datetime.combine(d, datetime.min.time()))


def is_naive(d: datetime | time):
    # Docs: https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        return True
    return False


def short_format_date(d: datetime) -> str:
    """
    Eg. 2023-09-02 15:36:03 GMT.
    """
    return d.strftime("%Y-%m-%d %H:%M:%S %Z")


def shortest_format_date(d: datetime) -> str:
    """
    Eg. 05/01/23 08:09.
    """
    # Convert to local timezone.
    d = d.astimezone()
    return d.strftime("%d/%m/%y %H:%M")


def local_timezone() -> tzinfo:
    """
    trick: not easy to get the local timezone, so we extract it from now().
    """
    return now().tzinfo


def convert_to_timezone(d: datetime, tz: ZoneInfo | None = None) -> datetime:
    """
    Convert the given datetime to a different timezone, adjusting the date and time
     according to the offset between the orignal and the new timezone.
    The given datetime can be naive.

    Args:
        d: a datetime. Naive or not.
        tz: default: local timezone. eg. ZoneInfo("Europe/Rome")

    Example:
        d = datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("Europe/Rome"))
        r = datetime_utils.convert_to_timezone(d, ZoneInfo("America/New_York"))
        assert r == datetime(
            2022, 4, 30, 18, 15, 0, tzinfo=ZoneInfo("America/New_York")
        )
    """
    return d.astimezone(tz)


def replace_timezone(d: datetime, tz: ZoneInfo | _DEFAULT = _DEFAULT) -> datetime:
    """
    Replace the timezone in the given datetime.
    IMP: it does NOT adjust date and time according to the offset between the original
     and the new timezone.
    The given datetime can be naive.
    Note: use tz=None to make it naive.

    Args:
        d: a datetime. Naive or not.
        tz: eg. ZoneInfo("Europe/Rome"). Default: local timezone. None to make it naive.

    Example:
        d = datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("Europe/Rome"))
        r = datetime_utils.replace_timezone(d, ZoneInfo("America/New_York"))
        assert r == datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("America/New_York"))
    """
    if tz == _DEFAULT:
        # If the timezone was not given, then use the local timezone.
        # Trick: we get the local timezone with now().
        tz = local_timezone()
    # Note: use tzinfo=None to make it naive.
    return d.replace(tzinfo=tz)


def parse_date_arg(
    value: date | datetime | str | None = None,
    is_type_date_allowed: bool = True,
    is_type_datetime_allowed: bool = True,
    is_type_str_allowed: bool = True,
    is_type_none_allowed: bool = True,
) -> date | None:
    """
    Parse a date arg as string or date or datetime.
    The typical use case is the parsing of a function argument.

    Args:
        value: the arg value.
        is_type_date_allowed: True to allow a date like date(2024, 1, 6).
        is_type_datetime_allowed: True to allow a datetime like datetime(2024, 1, 6, 17, 20, tzinfo=ZoneInfo("Europe/Rome")).
        is_type_str_allowed: True to allow a string like "2024-01-01" or "2024-01-01T00:00:01+01:00".
        is_type_none_allowed: True of the args is optional, so it can be None.

    Returns: a date instance or None if is_type_none_allowed is True and value is None.

    Example:
        r = datetime_utils.parse_date_arg("2024-01-01")
        assert r == date(2024, 1, 1)
    """
    if value is None:
        if is_type_none_allowed:
            return None
        else:
            raise DateRequired(value)

    elif isinstance(value, str) and is_type_str_allowed:
        try:
            value: date = iso_string_to_datetime(value).date()
        except ValueError as exc:
            raise InvalidDate(value) from exc
        return value

    elif isinstance(value, datetime) and is_type_datetime_allowed:
        return value.date()

    elif (
        isinstance(value, date)
        # `not isinstance(value, datetime)` is required because every datetime instance
        #   is also a date instance (the opposite is not true).
        and not isinstance(value, datetime)
        and is_type_date_allowed
    ):
        return value

    raise InvalidDate(value)


def parse_datetime_arg(
    value: datetime | date | str | None = None,
    is_type_datetime_allowed: bool = True,
    is_type_date_allowed: bool = True,
    is_type_str_allowed: bool = True,
    is_type_none_allowed: bool = True,
    is_naive_allowed: bool = False,
) -> datetime | None:
    """
    Parse a datetime arg as string or datetime or date.
    The typical use case is the parsing of a function argument.

    Args:
        value: the arg value.
        is_type_datetime_allowed: True to allow a datetime like datetime(2024, 1, 6, 17, 20, tzinfo=ZoneInfo("Europe/Rome")).
        is_type_date_allowed: True to allow a date like date(2024, 1, 6).
        is_type_str_allowed: True to allow a string like "2024-01-01T00:00:01+01:00".
        is_type_none_allowed: True of the args is optional, so it can be None.
        is_naive_allowed: True to allow a naive datetime value.

    Returns: a datetime instance or None if is_type_none_allowed is True and value is None.

    Example:
        r = datetime_utils.parse_datetime_arg("2024-01-01T00:00:01+01:00")
        assert r == datetime(
            2024, 1, 1, 0, 0, 1, tzinfo=timezone(timedelta(seconds=3600))
        )
    """
    if value is None:
        if is_type_none_allowed:
            return None
        else:
            raise DatetimeRequired(value)

    elif isinstance(value, str) and is_type_str_allowed:
        try:
            value: datetime = iso_string_to_datetime(value)
        except ValueError as exc:
            raise InvalidDatetime(value) from exc
        if not is_naive_allowed and is_naive(value):
            raise NaiveDatetime(value)
        return value

    elif isinstance(value, datetime) and is_type_datetime_allowed:
        if not is_naive_allowed and is_naive(value):
            raise NaiveDatetime(value)
        return value

    elif (
        isinstance(value, date)
        # `not isinstance(value, datetime)` is required because every datetime instance
        #   is also a date instance (the opposite is not true).
        and not isinstance(value, datetime)
        and is_type_date_allowed
    ):
        return date_to_datetime(value)

    raise InvalidDatetime(value)


def days_ago(d: datetime, n_decimal_digits: int = 1):
    """
    Example:
        >>> days_ago(datetime(2023, 11, 20, 7, 0, 0, tzinfo=timezone.utc))
        4.1
        >>> days_ago(datetime(2023, 11, 20, 7, 0, 0, tzinfo=timezone.utc), n_decimal_digits=5)
        4.10828
    """
    if is_naive(d):
        raise NaiveDatetime(d)
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
        raise NaiveDatetime(d)
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


def seconds_to_hh_mm_ss(
    seconds: int | float,
    do_use_leading_zero_fill: bool = False,
    do_hide_hours_and_mins_if_zero: bool = False,
) -> str:
    """
    Convert seconds to the format h:mm:ss.

    Eg. datetime_utils.seconds_to_hh_mm_ss(5)    -> "0:00:05"
        datetime_utils.seconds_to_hh_mm_ss(
            5,
            do_use_leading_zero_fill=True)       -> "00:00:05"
        datetime_utils.seconds_to_hh_mm_ss(
            5,
            do_hide_hours_and_mins_if_zero=True) -> "5"
        datetime_utils.seconds_to_hh_mm_ss(
            5,
            do_use_leading_zero_fill=True,
            do_hide_hours_and_mins_if_zero=True) -> "05"
        datetime_utils.seconds_to_hh_mm_ss(9251445) -> "107 days, 1:50:45"
    """
    str_val = str(timedelta(seconds=seconds))

    if do_use_leading_zero_fill:
        # Possible cases:
        #  1:01:05 -> 01:01:05
        #  0:01:05 -> 00:01:05
        #  0:00:05 -> 00:00:05
        if str_val.find(":") == 1:
            str_val = "0" + str_val

    if do_hide_hours_and_mins_if_zero:
        # Possible cases:
        #  1:01:05 or 01:01:05 -> no change
        #  0:01:05 or 00:01:05 -> 01:05
        #  0:00:05 or 00:00:05 -> 05
        while str_val.startswith("0:") or str_val.startswith("00:"):
            if str_val.startswith("0:"):
                str_val = str_val[2:]
            elif str_val.startswith("00:"):
                str_val = str_val[3:]

    if not do_use_leading_zero_fill:
        # Possible cases:
        #  1:01:05 or 01:01:05 -> no change, already handled in the prev `if do_use_leading_zero_fill`.
        #  0:01:05 -> no change
        #  00:01:05 or 01:05 -> 0:01:05, 1:05
        #  0:00:05 -> no change
        #  00:00:05 or 05 -> 0:00:05, 5
        if str_val.startswith("0"):
            if str_val.find(":") == 2:
                str_val = str_val[1:]
            elif ":" not in str_val:
                str_val = str_val[1:]

    return str_val


def seconds_to_hh_mm(
    seconds: int | float,
    do_use_leading_zero_fill: bool = False,
    do_hide_hours_and_mins_if_zero: bool = False,
) -> str:
    """
    Convert seconds to the format h:mm.
    If seconds are > 30 then it rounds the min to the next one.

    Eg. datetime_utils.seconds_to_hh_mm(1045)    -> "0:17"  # Approx of "0:17:25".
        datetime_utils.seconds_to_hh_mm(1051)    -> "0:18"  # Approx of "0:17:31".
        datetime_utils.seconds_to_hh_mm(5)       -> "0:00"
        datetime_utils.seconds_to_hh_mm(
            5,
            do_use_leading_zero_fill=True)       -> "00:00"
        datetime_utils.seconds_to_hh_mm(
            5,
            do_hide_hours_and_mins_if_zero=True) -> "0"
        datetime_utils.seconds_to_hh_mm(
            5,
            do_use_leading_zero_fill=True,
            do_hide_hours_and_mins_if_zero=True) -> "00"
        datetime_utils.seconds_to_hh_mm(9251445) -> "107 days, 1:51"  # Approx of "107 days, 1:50:45".
    """
    str_val = seconds_to_hh_mm_ss(
        seconds, do_use_leading_zero_fill, do_hide_hours_and_mins_if_zero
    )
    last_col_ix = str_val.rfind(":")

    # If the seconds are > 30 then we round the min to the next one (by adding 31 secs).
    secs = int(str_val[last_col_ix + 1 :])
    if secs > 30:
        return seconds_to_hh_mm(
            seconds + 31, do_use_leading_zero_fill, do_hide_hours_and_mins_if_zero
        )

    if last_col_ix > 0:
        str_val = str_val[:last_col_ix]
    else:
        # There are only seconds.
        str_val = "0" if not do_use_leading_zero_fill else "00"
    return str_val


class BaseDatetimeUtilsException(Exception):
    pass


class DatetimeRequired(BaseDatetimeUtilsException):
    pass


class DateRequired(BaseDatetimeUtilsException):
    pass


class InvalidDatetime(BaseDatetimeUtilsException):
    def __init__(self, value):
        self.value = value


class InvalidDate(BaseDatetimeUtilsException):
    def __init__(self, value):
        self.value = value


class NaiveDatetime(BaseDatetimeUtilsException):
    def __init__(self, value):
        self.value = value
