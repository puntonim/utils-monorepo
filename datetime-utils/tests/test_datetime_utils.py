from datetime import datetime, timezone

from datetime_utils import datetime_testutils, datetime_utils


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
