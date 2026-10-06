import pandas as pd

import speed_utils


class Test_minpkm_base10_to_base60:
    def test_happy_flow(self):
        assert speed_utils.minpkm_base10_to_base60(5.05) == "5:03"

    def test_0(self):
        assert speed_utils.minpkm_base10_to_base60(0) == "0:00"

    def test_approx_60_secs(self):
        assert speed_utils.minpkm_base10_to_base60(4.999) == "5:00"

    def test_approx_0_secs(self):
        assert speed_utils.minpkm_base10_to_base60(4.0001) == "4:00"

    def test_dataframe(self):
        df = pd.DataFrame([5.05, 0, 4.999, 0.0, 0.01, 4.0001], columns=["pace"])
        assert speed_utils.minpkm_base10_to_base60(df).pace.to_list() == [
            "5:03",
            "0:00",
            "5:00",
            "0:00",
            "0:01",
            "4:00",
        ]

    def test_series(self):
        df = pd.DataFrame([5.05, 0, 4.999, 0.0, 0.01, 4.0001], columns=["pace"])
        assert speed_utils.minpkm_base10_to_base60(df.pace).to_list() == [
            "5:03",
            "0:00",
            "5:00",
            "0:00",
            "0:01",
            "4:00",
        ]


class Test_minpkm_base60_to_base10:
    def test_happy_flow(self):
        assert speed_utils.minpkm_base60_to_base10("5:03") == 5.05

    def test_0(self):
        assert speed_utils.minpkm_base60_to_base10("0:00") == 0

    def test_approx_60_secs(self):
        assert speed_utils.minpkm_base60_to_base10("5:00") == 5.0
        assert speed_utils.minpkm_base60_to_base10("4:59") == 4.98
        assert speed_utils.minpkm_base60_to_base10("5:01") == 5.02

    def test_approx_0_secs(self):
        assert speed_utils.minpkm_base60_to_base10("4:00") == 4.0
        assert speed_utils.minpkm_base60_to_base10("3:59") == 3.98
        assert speed_utils.minpkm_base60_to_base10("4:01") == 4.02

    def test_dataframe(self):
        df = pd.DataFrame(
            [
                "5:03",
                "0:00",
                "5:00",
                "4:59",
                "5:01",
                "0:00",
                "0:01",
                "4:00",
                "3:59",
                "4:01",
            ],
            columns=["pace"],
        )
        assert speed_utils.minpkm_base60_to_base10(df).pace.to_list() == [
            5.05,
            0,
            5.0,
            4.98,
            5.02,
            0.0,
            0.02,
            4.0,
            3.98,
            4.02,
        ]

    def test_series(self):
        df = pd.DataFrame(
            [
                "5:03",
                "0:00",
                "5:00",
                "4:59",
                "5:01",
                "0:00",
                "0:01",
                "4:00",
                "3:59",
                "4:01",
            ],
            columns=["pace"],
        )
        assert speed_utils.minpkm_base60_to_base10(df.pace).to_list() == [
            5.05,
            0,
            5.0,
            4.98,
            5.02,
            0.0,
            0.02,
            4.0,
            3.98,
            4.02,
        ]


class Test_mps_to_minpkm_base10:
    def test_happy_flow(self):
        assert round(speed_utils.mps_to_minpkm_base10(3.3), 2) == 5.05
        assert round(speed_utils.mps_to_minpkm_base10(5.7), 2) == 2.92

    def test_0(self):
        assert round(speed_utils.mps_to_minpkm_base10(0), 2) == 0

    def test_dataframe(self):
        df = pd.DataFrame(
            [3.3, 5.7, 0],
            columns=["pace"],
        )
        assert speed_utils.mps_to_minpkm_base10(df).pace.round(2).to_list() == [
            5.05,
            2.92,
            0,
        ]

    def test_series(self):
        df = pd.DataFrame(
            [3.3, 5.7, 0],
            columns=["pace"],
        )
        assert speed_utils.mps_to_minpkm_base10(df.pace).round(2).to_list() == [
            5.05,
            2.92,
            0,
        ]


class Test_minpkm_base10_to_mps:
    def test_happy_flow(self):
        assert round(speed_utils.minpkm_base10_to_mps(5.05), 2) == 3.30
        assert round(speed_utils.minpkm_base10_to_mps(2.92), 2) == 5.71

    def test_0(self):
        assert round(speed_utils.minpkm_base10_to_mps(0), 2) == 0

    def test_dataframe(self):
        df = pd.DataFrame(
            [5.05, 2.92, 0],
            columns=["pace"],
        )
        assert speed_utils.minpkm_base10_to_mps(df).pace.round(2).to_list() == [
            3.30,
            5.71,
            0,
        ]

    def test_series(self):
        df = pd.DataFrame(
            [5.05, 2.92, 0],
            columns=["pace"],
        )
        assert speed_utils.minpkm_base10_to_mps(df.pace).round(2).to_list() == [
            3.30,
            5.71,
            0,
        ]


class Test_mps_to_kmph:
    def test_happy_flow(self):
        assert speed_utils.mps_to_kmph(4.344) == 15.6384

    def test_0(self):
        assert speed_utils.mps_to_kmph(0) == 0

    def test_dataframe(self):
        df = pd.DataFrame(
            [4.344, 0],
            columns=["pace"],
        )
        assert speed_utils.mps_to_kmph(df).pace.to_list() == [
            15.6384,
            0,
        ]

    def test_series(self):
        df = pd.DataFrame(
            [4.344, 0],
            columns=["pace"],
        )
        assert speed_utils.mps_to_kmph(df.pace).to_list() == [
            15.6384,
            0,
        ]


class Test_kmph_to_mps:
    def test_happy_flow(self):
        assert speed_utils.kmph_to_mps(15.6384) == 4.344

    def test_0(self):
        assert speed_utils.kmph_to_mps(0) == 0

    def test_dataframe(self):
        df = pd.DataFrame(
            [15.6384, 0],
            columns=["pace"],
        )
        assert speed_utils.kmph_to_mps(df).pace.to_list() == [
            4.344,
            0,
        ]

    def test_series(self):
        df = pd.DataFrame(
            [15.6384, 0],
            columns=["pace"],
        )
        assert speed_utils.kmph_to_mps(df.pace).to_list() == [
            4.344,
            0,
        ]
