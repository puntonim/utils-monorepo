import logging
from pathlib import Path

import log_utils as logger


class TestStdLibLogging:
    def setup_method(self):
        self.std_logging = logger.StdLibLoggingAdapter()
        self.std_logging.configure_default(is_verbose=True)
        logger.set_adapter(self.std_logging)

        self.debug_message = "First entry, debug"
        self.info_message = "Second entry, info"
        self.warning_message = "Third entry, warning"
        self.error_message = "Fourth entry, error"
        self.critical_message = "Fifth entry, critical"
        self.exception_message = "Sixth entry, exception"

    def teardown_method(self):
        logger.flush_adapter()

    def test_happy_flow(self, caplog):
        caplog.set_level(logging.DEBUG)

        logger.debug(self.debug_message)
        assert caplog.records[0].message == self.debug_message
        assert caplog.records[0].levelname == "DEBUG"
        assert Path(caplog.records[0].pathname).resolve() == Path(__file__).resolve()

        logger.info(
            self.info_message,
            extra=dict(color="red", car="ferrari", myclass=TestStdLibLogging),
        )
        assert caplog.records[1].message.startswith(self.info_message)
        assert "color=red" in caplog.records[1].message
        assert "car=ferrari" in caplog.records[1].message
        assert "myclass=" in caplog.records[1].message
        assert caplog.records[1].levelname == "INFO"
        assert Path(caplog.records[1].pathname).resolve() == Path(__file__).resolve()

        logger.warning(self.warning_message, extra=dict(color="red"))
        assert caplog.records[2].message.startswith(self.warning_message)
        assert "color=red" in caplog.records[2].message
        assert caplog.records[2].levelname == "WARNING"
        assert Path(caplog.records[2].pathname).resolve() == Path(__file__).resolve()

        logger.error(self.error_message, extra=dict(color="red"))
        assert caplog.records[3].message.startswith(self.error_message)
        assert "color=red" in caplog.records[3].message
        assert caplog.records[3].levelname == "ERROR"
        assert Path(caplog.records[3].pathname).resolve() == Path(__file__).resolve()

        logger.critical(self.critical_message, extra=dict(color="red"))
        assert caplog.records[4].message.startswith(self.critical_message)
        assert "color=red" in caplog.records[4].message
        assert caplog.records[4].levelname == "CRITICAL"
        assert Path(caplog.records[4].pathname).resolve() == Path(__file__).resolve()

        try:
            1 / 0
        except ZeroDivisionError:
            logger.exception(self.exception_message, extra=dict(color="red"))
        assert caplog.records[5].message.startswith(self.exception_message)
        assert "color=red" in caplog.records[5].message
        assert caplog.records[5].levelname == "ERROR"
        assert Path(caplog.records[5].pathname).resolve() == Path(__file__).resolve()

    def test_non_verbose(self, caplog):
        caplog.set_level(logging.INFO)

        logger.debug(self.debug_message)
        assert not caplog.records

        logger.info(self.info_message)
        assert caplog.records[0].message == self.info_message
        assert caplog.records[0].levelname == "INFO"
        assert Path(caplog.records[0].pathname).resolve() == Path(__file__).resolve()
