import logging
import sys


def set_root_logger_to_stderr():
    """
    Forcibly set the root logger to stderr.
    Loguru is typically configured to log to stderr, however a project might include
     libs that use the logging module with a root logger set to stdout.
    This is typically useful for when printing JSON, to make sure that stdout only
     contains the desired output and every log is redirected to stderr.
    """
    root = logging.getLogger()
    if len(root.handlers) and hasattr(root.handlers[0], "stream"):
        root.handlers[0].stream = sys.stderr


class StdLibLoggingAdapter:
    """
    Usage:
        from log_utils.log_utils import logger
        logger.configure_default()  # Do it on start-up, only once.
        logger.info("Hello", extra=dict(year=2025))
    """

    def configure_default(self, is_verbose=False):
        level = logging.DEBUG if is_verbose else logging.INFO
        # The default StreamHandler class uses stream=sys.stderr.
        logging.basicConfig(level=level)

    def _format_message(self, message: str | None = None, extra: dict | None = None):
        if not extra:
            return message

        message = message or ""
        for key, value in extra.items():
            serialized_value = str(value)
            if message:
                message += "\n"
            message += f"{key}={serialized_value}"

        return message

    def debug(self, message: str, extra: dict | None = None):
        message = self._format_message(message, extra)
        logging.debug(message)

    def info(self, message: str, extra: dict | None = None):
        message = self._format_message(message, extra)
        logging.info(message)

    def warning(self, message: str, extra: dict | None = None):
        message = self._format_message(message, extra)
        logging.warning(message)

    def error(self, message: str, extra: dict | None = None):
        message = self._format_message(message, extra)
        logging.error(message)

    def critical(self, message: str, extra: dict | None = None):
        message = self._format_message(message, extra)
        logging.critical(message)

    def exception(self, message: str | None = None, extra: dict | None = None):
        message = self._format_message(message, extra)
        logging.error(message, exc_info=sys.exc_info(), stack_info=True)


logger = StdLibLoggingAdapter()
