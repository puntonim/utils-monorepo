import importlib
import os
import sys
from pathlib import Path

from .base_adapter import BaseLogAdapter


class LoguruAdapter(BaseLogAdapter):
    def __init__(self):
        self.do_serialize_to_json: bool | None = None
        # Dynamic import, since loguru is an optional extra.
        self.logger = importlib.import_module("loguru").logger

    def configure_default(
        self,
        is_verbose=False,
        do_enable_file_logging=False,
        log_file_name="main.log",
        do_serialize_to_json=False,
        handler=None,  # To be used in tests, eg. `caplog.handler`.
    ):
        self.do_serialize_to_json = do_serialize_to_json

        self.logger.remove()

        # Add console logging.
        level = "INFO"
        if is_verbose:
            level = "DEBUG"
        # The default format is: <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>
        # See: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger
        self.logger.add(
            handler or sys.stderr,
            level=level,
            format="<level>{level: <8}</level> | <level>{message}</level>",
            # Filter to be used to skip logging to stderr, example:
            #   logger.bind(do_skip_stderr=True).info("Hello")  # Not logged by this logger!
            filter=lambda record: "do_skip_stderr" not in record["extra"],
            serialize=do_serialize_to_json,  # True to use structured logging with JSON.
            backtrace=True,  # For exceptions.
            diagnose=True,  # For parsing the backtrace.
        )

        # Add file logging.
        if do_enable_file_logging:
            log_file = Path(log_file_name)
            try:
                self.logger.add(
                    log_file,
                    level="DEBUG",
                    rotation="1 MB",
                    retention="30 days",
                    serialize=do_serialize_to_json,  # True to use structured logging with JSON.
                    backtrace=True,  # For exceptions.
                    diagnose=True,  # For parsing the backtrace.
                )
            except PermissionError as exc:
                self.logger.opt(exception=True).warning(exc)
                if not os.access(log_file.parent, os.W_OK):
                    raise CannotWriteToDir(log_file.parent) from exc
                raise LogPermissionError(log_file) from exc

    def _format_message_and_extra(
        self, message: str | None = None, extra: dict | None = None
    ):
        if not extra:
            extra = dict()

        if extra and not self.do_serialize_to_json:
            message = message or ""
            for key, value in extra.items():
                serialized_value = str(value)
                if message:
                    message += "\n"
                message += f"{key}={serialized_value}"
            extra = dict()
        return message, extra

    def debug(self, message: str, extra: dict | None = None):
        message, extra = self._format_message_and_extra(message, extra)
        self.logger.debug(message, **extra)

    def info(self, message: str, extra: dict | None = None):
        message, extra = self._format_message_and_extra(message, extra)
        self.logger.info(message, **extra)

    def warning(self, message: str, extra: dict | None = None):
        message, extra = self._format_message_and_extra(message, extra)
        self.logger.warning(message, **extra)

    def error(self, message: str, extra: dict | None = None):
        message, extra = self._format_message_and_extra(message, extra)
        self.logger.error(message, **extra)

    def critical(self, message: str, extra: dict | None = None):
        message, extra = self._format_message_and_extra(message, extra)
        self.logger.critical(message, **extra)

    def exception(self, message: str | None = None, extra: dict | None = None):
        message, extra = self._format_message_and_extra(message, extra)
        self.logger.exception(message, **extra)


class BaseLoguruAdapterException(Exception):
    pass


class CannotWriteToDir(BaseLoguruAdapterException):
    def __init__(self, path: Path):
        self.path = path


class LogPermissionError(BaseLoguruAdapterException):
    def __init__(self, path: Path):
        self.path = path
