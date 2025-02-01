from datetime import datetime, timedelta

import datetime_utils
from datetime_utils import datetime_testutils


class TestFreezeTime:
    NOW = datetime(2022, 1, 21, 20, 33, 0).astimezone()

    @datetime_testutils.freeze_time(NOW)
    def test_happy_flow(self):
        assert datetime_utils.now() == self.NOW


class TestApproxNow:
    NOW = datetime(2022, 1, 21, 20, 33, 0).astimezone()

    @datetime_testutils.freeze_time(NOW)
    def test_happy_flow(self):
        d = self.NOW + timedelta(seconds=3)
        assert d != self.NOW
        assert datetime_testutils.approx_now(buffer_seconds=20) == d
