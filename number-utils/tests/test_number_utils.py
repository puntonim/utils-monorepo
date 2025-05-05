import number_utils


class TestOrdinal:
    def test_happy_flow(self):
        assert number_utils.ordinal(5) == "5th"
