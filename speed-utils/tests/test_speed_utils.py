import speed_utils


class Test_minpkm_base10_to_base60:
    def test_happy_flow(self):
        assert speed_utils.minpkm_base10_to_base60(5.05) == "5:03"

    def test_approx_60_secs(self):
        assert speed_utils.minpkm_base10_to_base60(4.999) == "5:00"

    def test_approx_0_secs(self):
        assert speed_utils.minpkm_base10_to_base60(4.0001) == "4:00"


class Test_minpkm_base60_to_base10:
    def test_happy_flow(self):
        assert speed_utils.minpkm_base60_to_base10("5:03") == 5.05

    def test_approx_60_secs(self):
        assert speed_utils.minpkm_base60_to_base10("5:00") == 5.0
        assert speed_utils.minpkm_base60_to_base10("4:59") == 4.98
        assert speed_utils.minpkm_base60_to_base10("5:01") == 5.02

    def test_approx_0_secs(self):
        assert speed_utils.minpkm_base60_to_base10("4:00") == 4.0
        assert speed_utils.minpkm_base60_to_base10("3:59") == 3.98
        assert speed_utils.minpkm_base60_to_base10("4:01") == 4.02


class Test_mps_to_minpkm_base10:
    def test_happy_flow(self):
        assert round(speed_utils.mps_to_minpkm_base10(3.3), 2) == 5.05
        assert round(speed_utils.mps_to_minpkm_base10(5.7), 2) == 2.92


class Test_minpkm_base10_to_mps:
    def test_happy_flow(self):
        assert round(speed_utils.minpkm_base10_to_mps(5.05), 2) == 3.30
        assert round(speed_utils.minpkm_base10_to_mps(2.92), 2) == 5.71


class Test_mps_to_kmph:
    def test_happy_flow(self):
        assert speed_utils.mps_to_kmph(4.344) == 15.6384


class Test_kmph_to_mps:
    def test_happy_flow(self):
        assert speed_utils.kmph_to_mps(15.6384) == 4.344
