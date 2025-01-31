import logging

from log_utils.std_lib_logging_utils import logger


class TestStdLibLoggingAdapter:
    def setup_method(self):
        logger.configure_default(is_verbose=True)

        self.debug_message = "First entry, debug"
        self.info_message = "Second entry, info"
        self.warning_message = "Third entry, warning"
        self.error_message = "Fourth entry, error"
        self.critical_message = "Fifth entry, critical"
        self.exception_message = "Sixth entry, exception"

    def test_happy_flow(self, caplog):
        caplog.set_level(logging.DEBUG)

        logger.debug(self.debug_message)
        assert caplog.records[0].message == self.debug_message
        assert caplog.records[0].levelname == "DEBUG"

        logger.info(
            self.info_message,
            extra=dict(color="red", car="ferrari", myclass=TestStdLibLoggingAdapter),
        )
        assert caplog.records[1].message.startswith(self.info_message)
        assert "color=red" in caplog.records[1].message
        assert "car=ferrari" in caplog.records[1].message
        assert "myclass=" in caplog.records[1].message
        assert caplog.records[1].levelname == "INFO"

        logger.warning(self.warning_message, extra=dict(color="red"))
        assert caplog.records[2].message.startswith(self.warning_message)
        assert "color=red" in caplog.records[2].message
        assert caplog.records[2].levelname == "WARNING"

        logger.error(self.error_message, extra=dict(color="red"))
        assert caplog.records[3].message.startswith(self.error_message)
        assert "color=red" in caplog.records[3].message
        assert caplog.records[3].levelname == "ERROR"

        logger.critical(self.critical_message, extra=dict(color="red"))
        assert caplog.records[4].message.startswith(self.critical_message)
        assert "color=red" in caplog.records[4].message
        assert caplog.records[4].levelname == "CRITICAL"

        try:
            1 / 0
        except ZeroDivisionError:
            logger.exception(self.exception_message, extra=dict(color="red"))
        assert caplog.records[5].message.startswith(self.exception_message)
        assert "color=red" in caplog.records[5].message
        assert caplog.records[5].levelname == "ERROR"

    def test_non_verbose(self, caplog):
        caplog.set_level(logging.INFO)

        logger.debug(self.debug_message)
        assert not caplog.records

        logger.info(self.info_message)
        assert caplog.records[0].message == self.info_message
        assert caplog.records[0].levelname == "INFO"
