from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

import datetime_utils
from datetime_utils import datetime_testutils
from datetime_utils.datetime_utils import (
    DateRequired,
    DatetimeRequired,
    InvalidDate,
    InvalidDatetime,
    NaiveDatetime,
)


class TestNowUtc:
    def test_happy_flow(self):
        d = datetime_utils.now_utc()
        assert d.tzinfo == timezone.utc


class TestIsNaive:
    def test_happy_flow(self):
        assert not datetime_utils.is_naive(datetime_utils.now_utc())


class TestDaysAgo:
    @datetime_testutils.freeze_time(datetime(2022, 1, 23, 22, 15, 0).astimezone())
    def test_happy_flow(self):
        d = datetime(2022, 1, 21, 20, 33, 0).astimezone()
        assert datetime_utils.days_ago(d) == 2.1

    @datetime_testutils.freeze_time(datetime(2022, 1, 23, 22, 15, 0).astimezone())
    def test_negative(self):
        d = datetime(2022, 1, 25, 20, 33, 0).astimezone()
        assert datetime_utils.days_ago(d) == -1.9


class TestDaysToGo:
    @datetime_testutils.freeze_time(datetime(2022, 3, 5, 22, 15, 0).astimezone())
    def test_happy_flow(self):
        d = datetime(2022, 3, 7, 2, 33, 0).astimezone()
        assert datetime_utils.days_to_go(d) == 1.2

    @datetime_testutils.freeze_time(datetime(2022, 3, 23, 22, 15, 0).astimezone())
    def test_negative(self):
        d = datetime(2020, 3, 3, 23, 59, 0).astimezone()
        assert datetime_utils.days_to_go(d) == -749.9


class TestSecondsToHhMmSs:
    def test_happy_flow(self):
        assert datetime_utils.seconds_to_hh_mm_ss(1045) == "0:17:25"

    def test_1_digit(self):
        s = 5
        assert datetime_utils.seconds_to_hh_mm_ss(s) == "0:00:05"
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_use_leading_zero_fill=True)
            == "00:00:05"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_hide_hours_and_mins_if_zero=True)
            == "5"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "05"
        )

    def test_2_digits(self):
        s = 55
        assert datetime_utils.seconds_to_hh_mm_ss(s) == "0:00:55"
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_use_leading_zero_fill=True)
            == "00:00:55"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_hide_hours_and_mins_if_zero=True)
            == "55"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "55"
        )

    def test_3_digits(self):
        s = 65
        assert datetime_utils.seconds_to_hh_mm_ss(s) == "0:01:05"
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_use_leading_zero_fill=True)
            == "00:01:05"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_hide_hours_and_mins_if_zero=True)
            == "1:05"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "01:05"
        )

    def test_4_digits(self):
        s = 665
        assert datetime_utils.seconds_to_hh_mm_ss(s) == "0:11:05"
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_use_leading_zero_fill=True)
            == "00:11:05"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_hide_hours_and_mins_if_zero=True)
            == "11:05"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "11:05"
        )

    def test_5_digits(self):
        s = 3665
        assert datetime_utils.seconds_to_hh_mm_ss(s) == "1:01:05"
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_use_leading_zero_fill=True)
            == "01:01:05"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_hide_hours_and_mins_if_zero=True)
            == "1:01:05"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "01:01:05"
        )

    def test_6_digits(self):
        s = 36065
        assert datetime_utils.seconds_to_hh_mm_ss(s) == "10:01:05"
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_use_leading_zero_fill=True)
            == "10:01:05"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(s, do_hide_hours_and_mins_if_zero=True)
            == "10:01:05"
        )
        assert (
            datetime_utils.seconds_to_hh_mm_ss(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "10:01:05"
        )

    def test_long(self):
        assert datetime_utils.seconds_to_hh_mm_ss(9251445) == "107 days, 1:50:45"


class TestSecondsToHhMm:
    def test_happy_flow(self):
        assert datetime_utils.seconds_to_hh_mm(1045) == "0:17"  # Approx of "0:17:25".

    def test_rounding(self):
        assert datetime_utils.seconds_to_hh_mm(1050) == "0:17"  # Approx of "0:17:30".
        assert datetime_utils.seconds_to_hh_mm(1051) == "0:18"  # Approx of "0:17:31".
        assert datetime_utils.seconds_to_hh_mm(1079) == "0:18"  # Approx of "0:17:59".
        assert datetime_utils.seconds_to_hh_mm(1080) == "0:18"  # Approx of "0:18:00".

    def test_1_digit(self):
        s = 5
        assert datetime_utils.seconds_to_hh_mm(s) == "0:00"
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_use_leading_zero_fill=True) == "00:00"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_hide_hours_and_mins_if_zero=True)
            == "0"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "00"
        )

    def test_2_digits_and_rounding(self):
        s = 25
        assert datetime_utils.seconds_to_hh_mm(s) == "0:00"
        assert datetime_utils.seconds_to_hh_mm(s + 10) == "0:01"
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_use_leading_zero_fill=True) == "00:00"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(s + 10, do_use_leading_zero_fill=True)
            == "00:01"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_hide_hours_and_mins_if_zero=True)
            == "0"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(s + 10, do_hide_hours_and_mins_if_zero=True)
            == "1"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "00"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(
                s + 10,
                do_use_leading_zero_fill=True,
                do_hide_hours_and_mins_if_zero=True,
            )
            == "01"
        )

    def test_3_digits(self):
        s = 65
        assert datetime_utils.seconds_to_hh_mm(s) == "0:01"
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_use_leading_zero_fill=True) == "00:01"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_hide_hours_and_mins_if_zero=True)
            == "1"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "01"
        )

    def test_4_digits(self):
        s = 665
        assert datetime_utils.seconds_to_hh_mm(s) == "0:11"
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_use_leading_zero_fill=True) == "00:11"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_hide_hours_and_mins_if_zero=True)
            == "11"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "11"
        )

    def test_5_digits(self):
        s = 3665
        assert datetime_utils.seconds_to_hh_mm(s) == "1:01"
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_use_leading_zero_fill=True) == "01:01"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_hide_hours_and_mins_if_zero=True)
            == "1:01"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "01:01"
        )

    def test_6_digits_and_rounding(self):
        s = 36065
        assert datetime_utils.seconds_to_hh_mm(s) == "10:01"  # Approx of "10:01:05".
        assert (
            datetime_utils.seconds_to_hh_mm(s + 30) == "10:02"  # Approx of "10:01:35".
        )
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_use_leading_zero_fill=True) == "10:01"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(s + 30, do_use_leading_zero_fill=True)
            == "10:02"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(s, do_hide_hours_and_mins_if_zero=True)
            == "10:01"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(s + 30, do_hide_hours_and_mins_if_zero=True)
            == "10:02"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(
                s, do_use_leading_zero_fill=True, do_hide_hours_and_mins_if_zero=True
            )
            == "10:01"
        )
        assert (
            datetime_utils.seconds_to_hh_mm(
                s + 30,
                do_use_leading_zero_fill=True,
                do_hide_hours_and_mins_if_zero=True,
            )
            == "10:02"
        )

    def test_long(self):
        assert (
            datetime_utils.seconds_to_hh_mm(9251445) == "107 days, 1:51"
        )  # Approx of "107 days, 1:50:45".


class TestReplaceTimezone:
    def test_happy_flow(self):
        d = datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("Europe/Rome"))
        r = datetime_utils.replace_timezone(d, ZoneInfo("America/New_York"))
        assert r == datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("America/New_York"))

    def test_naive_input(self):
        d = datetime(2022, 5, 1, 0, 15, 0)
        r = datetime_utils.replace_timezone(d, ZoneInfo("America/New_York"))
        assert r == datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("America/New_York"))

    def test_naive_output(self):
        d = datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("Europe/Rome"))
        r = datetime_utils.replace_timezone(d, tz=None)
        assert datetime_utils.is_naive(r)

    def test_default_timezone(self):
        d = datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("America/New_York"))
        r = datetime_utils.replace_timezone(d)
        # Note: this test only works when run in Europe/Rome.
        assert r == datetime(2022, 5, 1, 0, 15, 0, tzinfo=datetime_utils.now().tzinfo)


class TestConvertToTimezone:
    def test_happy_flow(self):
        d = datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("Europe/Rome"))
        r = datetime_utils.convert_to_timezone(d, ZoneInfo("America/New_York"))
        assert r == datetime(
            2022, 4, 30, 18, 15, 0, tzinfo=ZoneInfo("America/New_York")
        )

    def test_default_timezone(self):
        d = datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("America/New_York"))
        r = datetime_utils.convert_to_timezone(d)
        # Note: this test only works when run in Europe/Rome.
        assert r == datetime(2022, 5, 1, 6, 15, 0, tzinfo=datetime_utils.now().tzinfo)


class TestDateToDatetime:
    def test_happy_flow(self):
        d = date(2022, 5, 1)
        r = datetime_utils.date_to_datetime(d)
        assert r == datetime(2022, 5, 1, 0, 0, 0, tzinfo=datetime_utils.now().tzinfo)


class TestParseDatetimeArg:
    def test_happy_flow(self):
        r = datetime_utils.parse_datetime_arg("2024-01-01T00:00:01+01:00")
        assert r == datetime(
            2024, 1, 1, 0, 0, 1, tzinfo=timezone(timedelta(seconds=3600))
        )

    def test_none_value(self):
        r = datetime_utils.parse_datetime_arg(None, is_type_none_allowed=True)
        assert r is None
        with pytest.raises(DatetimeRequired):
            datetime_utils.parse_datetime_arg(None, is_type_none_allowed=False)

    def test_string_type(self):
        r = datetime_utils.parse_datetime_arg(
            "2024-01-01T00:00:01+01:00", is_type_str_allowed=True
        )
        assert r == datetime(
            2024, 1, 1, 0, 0, 1, tzinfo=timezone(timedelta(seconds=3600))
        )

    def test_string_type_not_allowed(self):
        with pytest.raises(InvalidDatetime):
            datetime_utils.parse_datetime_arg(
                "2024-01-01T00:00:01+01:00", is_type_str_allowed=False
            )

    def test_string_type_naive_not_allowed(self):
        with pytest.raises(NaiveDatetime):
            datetime_utils.parse_datetime_arg(
                "2024-01-01T00:00:01", is_naive_allowed=False
            )

    def test_datetime_type(self):
        d = datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("America/New_York"))
        r = datetime_utils.parse_datetime_arg(d, is_type_datetime_allowed=True)
        assert r == d

    def test_datetime_type_not_allowed(self):
        d = datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("America/New_York"))
        with pytest.raises(InvalidDatetime):
            datetime_utils.parse_datetime_arg(d, is_type_datetime_allowed=False)

    def test_datetime_type_naive_not_allowed(self):
        d = datetime(2022, 5, 1, 0, 15, 0)
        with pytest.raises(NaiveDatetime):
            datetime_utils.parse_datetime_arg(d, is_naive_allowed=False)

    def test_date_type(self):
        d = date(2022, 5, 1)
        r = datetime_utils.parse_datetime_arg(d, is_type_date_allowed=True)
        assert r == datetime(2022, 5, 1, 0, 0, 0, tzinfo=datetime_utils.now().tzinfo)

    def test_date_type_not_allowed(self):
        d = date(2022, 5, 1)
        with pytest.raises(InvalidDatetime):
            datetime_utils.parse_datetime_arg(d, is_type_date_allowed=False)

    def test_date_type_naive_not_allowed(self):
        d = date(2022, 5, 1)
        r = datetime_utils.parse_datetime_arg(d, is_naive_allowed=False)
        assert r == datetime(2022, 5, 1, 0, 0, 0, tzinfo=datetime_utils.now().tzinfo)


class TestParseDateArg:
    def test_happy_flow(self):
        d = "2022-03-18"
        r = datetime_utils.parse_date_arg(d)
        assert r == date(2022, 3, 18)

    def test_none_value(self):
        r = datetime_utils.parse_date_arg(None, is_type_none_allowed=True)
        assert r is None
        with pytest.raises(DateRequired):
            datetime_utils.parse_date_arg(None, is_type_none_allowed=False)

    def test_string_type(self):
        r = datetime_utils.parse_date_arg("2024-01-01", is_type_str_allowed=True)
        assert r == date(2024, 1, 1)

    def test_string_type_not_allowed(self):
        with pytest.raises(InvalidDate):
            datetime_utils.parse_date_arg("2024-01-01", is_type_str_allowed=False)

    def test_datetime_type(self):
        d = datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("America/New_York"))
        r = datetime_utils.parse_date_arg(d, is_type_datetime_allowed=True)
        assert r == d.date()

    def test_datetime_type_not_allowed(self):
        d = datetime(2022, 5, 1, 0, 15, 0, tzinfo=ZoneInfo("America/New_York"))
        with pytest.raises(InvalidDate):
            datetime_utils.parse_date_arg(d, is_type_datetime_allowed=False)

    def test_date_type(self):
        d = date(2022, 5, 1)
        r = datetime_utils.parse_date_arg(d, is_type_date_allowed=True)
        assert r == d

    def test_date_type_not_allowed(self):
        d = date(2022, 5, 1)
        with pytest.raises(InvalidDate):
            datetime_utils.parse_date_arg(d, is_type_date_allowed=False)
