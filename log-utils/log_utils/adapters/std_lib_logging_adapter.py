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
        # Use stacklevel=4 to get to the original source line that
        #  invoked the log statement, which is 4 frames above in the stack.
        # It's an arg used in Python std-lib logging:
        #  https://docs.python.org/3/library/logging.html#logging.Logger.debug
        logging.debug(message, stacklevel=4)

    def info(self, message: str, extra: dict | None):
        message = self._format_message(message, extra)
        logging.info(message, stacklevel=4)

    def warning(self, message: str, extra: dict | None):
        message = self._format_message(message, extra)
        logging.warning(message, stacklevel=4)

    def error(self, message: str, extra: dict | None):
        message = self._format_message(message, extra)
        logging.error(message, stacklevel=4)

    def critical(self, message: str, extra: dict | None):
        message = self._format_message(message, extra)
        logging.critical(message, stacklevel=4)

    def exception(self, message: str | None, extra: dict | None):
        message = self._format_message(message, extra)
        logging.error(message, exc_info=sys.exc_info(), stack_info=True, stacklevel=4)
