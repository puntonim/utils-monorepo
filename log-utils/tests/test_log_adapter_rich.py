import log_utils as logger


class TestRich:
    def setup_method(self):
        rich_adapter = logger.RichAdapter()
        rich_adapter.configure_default(is_verbose=True)
        logger.set_adapter(rich_adapter)

        self.debug_message = "First entry, debug"
        self.info_message = "Second entry, info"
        self.warning_message = "Third entry, warning"
        self.error_message = "Fourth entry, error"
        self.critical_message = "Fifth entry, critical"
        self.exception_message = "Sixth entry, exception"

    def teardown_method(self):
        logger.flush_adapter()

    def test_happy_flow(self, capfd):
        # NOTE: this test only work when running test with the option "-s", eg: pytest -s tests.
        logger.debug(self.debug_message)
        logger.info(self.info_message)

        captured = capfd.readouterr()
        assert self.debug_message in captured.err
        assert self.info_message in captured.err
