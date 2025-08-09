from tests.car import Car
from vcr_utils import vcr_utils


class TestVcrUtils:
    @vcr_utils("tests.car.Car.start")
    def test_happy_flow(self):
        start_ts = Car().start()
        assert start_ts.isoformat() == "2025-08-09T13:11:05.179929+00:00"
