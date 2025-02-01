import logging
import sys

from .base_adapter import BaseLogAdapter


class StdLibLoggingAdapter(BaseLogAdapter):
    def configure_default(self, level=logging.INFO, is_verbose=False):
        if is_verbose:
            level = logging.DEBUG
        # The default StreamHandler class uses stream=sys.stderr.
        logging.basicConfig(level=level)
        # Not sure if this is the right thing to do, but it works.
        for hl in logging.getLogger().handlers:
            hl.setLevel(level)

    def _format_message(self, message: str | None, extra: dict | None):
        if not extra:
            return message

        message = message or ""
        for key, value in extra.items():
            serialized_value = str(value)
            if message:
                message += "\n"
            message += f"{key}={serialized_value}"

        return message

    def debug(self, message: str, extra: dict | None):
        message = self._format_message(message, extra)
        logging.debug(message)

    def info(self, message: str, extra: dict | None):
        message = self._format_message(message, extra)
        logging.info(message)

    def warning(self, message: str, extra: dict | None):
        message = self._format_message(message, extra)
        logging.warning(message)

    def error(self, message: str, extra: dict | None):
        message = self._format_message(message, extra)
        logging.error(message)

    def critical(self, message: str, extra: dict | None):
        message = self._format_message(message, extra)
        logging.critical(message)

    def exception(self, message: str | None, extra: dict | None):
        message = self._format_message(message, extra)
        logging.error(message, exc_info=sys.exc_info(), stack_info=True)
