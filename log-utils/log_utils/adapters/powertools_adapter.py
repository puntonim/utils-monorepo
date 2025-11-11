import importlib
import logging
import sys

from .base_adapter import BaseLogAdapter


class PowertoolsLoggerAdapter(BaseLogAdapter):
    def __init__(self):
        self.do_serialize_to_json: bool | None = None
        # Dynamic import, since Lambda Powertools is not a requirement (it is a Lambda layer).
        self.LoggerClass = importlib.import_module("aws_lambda_powertools").Logger
        self.logger = self.LoggerClass()

    def configure_default(
        self,
        #  Mind that "service" (and not "app") is the exact term used by
        #   aws_lambda_powertools.Logger.
        service_name: str,
        service_version: str | None = None,
        is_verbose=False,
        handler=None,  # To be used in tests, eg. `caplog.handler`.
    ):
        """
        Args:
            service_name: service name to be used in the logs. Mind that "service" (and
             not "app") is the exact term used by aws_lambda_powertools.Logger.
            service_version: service version to be used in the logs.
            is_verbose: True to set the level to DEBUG.
            handler: to be used in tests,  eg. `caplog.handler`.
        """
        level = logging.DEBUG if is_verbose else logging.INFO
        service = service_name
        if service_version:
            service += f" @ v{service_version}"
        self.logger = self.LoggerClass(
            service=service,
            level=level,
            location="%(pathname)s::%(funcName)s::%(lineno)d",
            logger_handler=handler,
        )

    def debug(self, message: str, extra: dict | None = None):
        # Use stacklevel=4 to get to the original source line that
        #  invoked the log statement, which is 4 frames above in the stack.
        # It's an arg used in Python std-lib logging:
        #  https://docs.python.org/3/library/logging.html#logging.Logger.debug
        self.logger.debug(message, extra=extra, stacklevel=4)

    def info(self, message: str, extra: dict | None = None):
        self.logger.info(message, extra=extra, stacklevel=4)

    def warning(self, message: str, extra: dict | None = None):
        self.logger.warning(message, extra=extra, stacklevel=4)

    def error(self, message: str, extra: dict | None = None):
        self.logger.error(message, extra=extra, stacklevel=4)

    def critical(self, message: str, extra: dict | None = None):
        self.logger.critical(message, extra=extra, stacklevel=4)

    def exception(self, message: str | None = None, extra: dict | None = None):
        if extra:
            message = message or ""
            for key, value in extra.items():
                serialized_value = str(value)
                if message:
                    message += "\n"
                message += f"{key}={serialized_value}"
        self.logger.exception(
            message, exc_info=sys.exc_info(), stack_info=True, stacklevel=4
        )

    def inject_lambda_context(self, *args, **kwargs):
        return self.logger.inject_lambda_context(*args, **kwargs)
