import text_utils


class TestTruncateText:
    def test_happy_flow(self):
        assert text_utils.truncate_text("hello world!", 4) == "hell…"
