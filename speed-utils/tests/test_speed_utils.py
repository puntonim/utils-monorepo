import speed_utils


class TestMinPKmBase10ToBase60:
    def test_happy_flow(self):
        assert speed_utils.minpkm_base10_to_base60(5.05) == "5:03"

    def test_approx_60_secs(self):
        assert speed_utils.minpkm_base10_to_base60(4.999) == "5:00"

    def test_approx_0_secs(self):
        assert speed_utils.minpkm_base10_to_base60(4.0001) == "4:00"


class TestMpsToKmph:
    def test_happy_flow(self):
        assert speed_utils.mps_to_kmph(4.344) == 15.6384
