from datetime import timezone

from datetime_utils import datetime_utils


class TestNowUtc:
    def test_happy_flow(self):
        d = datetime_utils.now_utc()
        assert d.tzinfo == timezone.utc


class TestIsNaive:
    def test_happy_flow(self):
        assert not datetime_utils.is_naive(datetime_utils.now_utc())
