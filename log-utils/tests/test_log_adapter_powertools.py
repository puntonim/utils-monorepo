import pytest
from _pytest.logging import LogCaptureFixture

import log_utils as logger


@pytest.fixture(scope="function")
def caplog_for_powertools(caplog: LogCaptureFixture):
    # Configure loguru adapter, but use `caplog.handler` so that caplog can
    #  intercept the log entries.
    pwr_logging = logger.PowertoolsLoggerAdapter()
    pwr_logging.configure_default(
        service_name="myname",
        service_version="1.2.3",
        is_verbose=True,
        handler=caplog.handler,
    )
    logger.set_adapter(pwr_logging)

    yield caplog


# TODO these tests do not work properly. Find a better way to test this!


class TestPowertools:
    def setup_method(self):
        self.debug_message = "First entry, debug"
        self.info_message = "Second entry, info"
        self.warning_message = "Third entry, warning"
        self.error_message = "Fourth entry, error"
        self.critical_message = "Fifth entry, critical"
        self.exception_message = "Sixth entry, exception"

    def teardown_method(self):
        logger.flush_adapter()

    def test_happy_flow(self, caplog_for_powertools):
        logger.debug(self.debug_message)
        logger.info(self.debug_message)
        logger.error(self.debug_message)
        # assert caplog_for_powertools.records[0].message[11:] == self.debug_message
