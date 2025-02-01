import json

import log_utils as logger
import pytest
from _pytest.logging import LogCaptureFixture


@pytest.fixture(scope="function")
def caplog_for_loguru(caplog: LogCaptureFixture):
    # Configure Loguru adapter, but use `caplog.handler` so that caplog can
    #  intercept the log entries.
    loguru_adapter = logger.LoguruAdapter()
    loguru_adapter.configure_default(
        is_verbose=True, do_serialize_to_json=False, handler=caplog.handler
    )
    logger.set_adapter(loguru_adapter)

    yield caplog


@pytest.fixture(scope="function")
def caplog_for_loguru_non_verbose(caplog: LogCaptureFixture):
    # Configure Loguru adapter, but use `caplog.handler` so that caplog can
    #  intercept the log entries.
    loguru_adapter = logger.LoguruAdapter()
    loguru_adapter.configure_default(
        is_verbose=False, do_serialize_to_json=False, handler=caplog.handler
    )
    logger.set_adapter(loguru_adapter)

    yield caplog


@pytest.fixture(scope="function")
def caplog_for_loguru_serialized_to_json(caplog: LogCaptureFixture):
    # Configure Loguru adapter, but use `caplog.handler` so that caplog can
    #  intercept the log entries.
    loguru_adapter = logger.LoguruAdapter()
    loguru_adapter.configure_default(
        is_verbose=True, do_serialize_to_json=True, handler=caplog.handler
    )
    logger.set_adapter(loguru_adapter)

    yield caplog


class TestLoguru:
    def setup_method(self):
        self.debug_message = "First entry, debug"
        self.info_message = "Second entry, info"
        self.warning_message = "Third entry, warning"
        self.error_message = "Fourth entry, error"
        self.critical_message = "Fifth entry, critical"
        self.exception_message = "Sixth entry, exception"

    def teardown_method(self):
        logger.flush_adapter()

    def test_happy_flow(self, caplog_for_loguru):
        logger.debug(self.debug_message)
        assert caplog_for_loguru.records[0].message[11:] == self.debug_message
        assert caplog_for_loguru.records[0].levelname == "DEBUG"

        logger.info(
            self.info_message,
            extra=dict(color="red", car="ferrari", myclass=TestLoguru),
        )
        assert caplog_for_loguru.records[1].message[11:].startswith(self.info_message)
        assert "color=red" in caplog_for_loguru.records[1].message
        assert "car=ferrari" in caplog_for_loguru.records[1].message
        assert "myclass=" in caplog_for_loguru.records[1].message
        assert caplog_for_loguru.records[1].levelname == "INFO"

        logger.warning(self.warning_message, extra=dict(color="red"))
        assert (
            caplog_for_loguru.records[2].message[11:].startswith(self.warning_message)
        )
        assert "color=red" in caplog_for_loguru.records[2].message
        assert caplog_for_loguru.records[2].levelname == "WARNING"

        logger.error(self.error_message, extra=dict(color="red"))
        assert caplog_for_loguru.records[3].message[11:].startswith(self.error_message)
        assert "color=red" in caplog_for_loguru.records[3].message
        assert caplog_for_loguru.records[3].levelname == "ERROR"

        logger.critical(self.critical_message, extra=dict(color="red"))
        assert (
            caplog_for_loguru.records[4].message[11:].startswith(self.critical_message)
        )
        assert "color=red" in caplog_for_loguru.records[4].message
        assert caplog_for_loguru.records[4].levelname == "CRITICAL"

        try:
            1 / 0
        except ZeroDivisionError:
            logger.exception(self.exception_message, extra=dict(color="red"))
        assert (
            caplog_for_loguru.records[5].message[11:].startswith(self.exception_message)
        )
        assert "color=red" in caplog_for_loguru.records[5].message
        assert caplog_for_loguru.records[5].levelname == "ERROR"

    def test_serialize_to_json(self, caplog_for_loguru_serialized_to_json):
        logger.info(
            self.info_message,
            extra=dict(color="red", car="ferrari", myclass=TestLoguru),
        )
        message = caplog_for_loguru_serialized_to_json.records[0].message
        record = json.loads(message)["record"]

        assert record["message"] == self.info_message
        assert record["extra"]["color"] == "red"
        assert record["extra"]["car"] == "ferrari"
        assert "myclass" in record["extra"]

    def test_non_verbose(self, caplog_for_loguru_non_verbose):
        logger.debug(self.debug_message)
        assert not caplog_for_loguru_non_verbose.records

        logger.info(self.info_message)
        assert (
            caplog_for_loguru_non_verbose.records[0]
            .message[11:]
            .startswith(self.info_message)
        )
