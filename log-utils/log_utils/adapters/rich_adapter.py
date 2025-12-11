import importlib
import sys

from .base_adapter import BaseLogAdapter


class RichAdapter(BaseLogAdapter):
    def __init__(self):
        self.is_verbose = None
        # Dynamic import, since Rich is an optional extra.
        self.stderr_console = importlib.import_module("rich.console").Console(
            file=sys.stderr
        )

    def configure_default(self, is_verbose=False):
        # Rich does not hande levels, so we have to handle them here.
        self.is_verbose = is_verbose

    def debug(self, message: str, extra: dict | None = None, **kwargs):
        if self.is_verbose:
            self._log(message, extra, **kwargs)

    def info(self, message: str, extra: dict | None = None, **kwargs):
        self._log(message, extra, **kwargs)

    def warning(self, message: str, extra: dict | None = None, **kwargs):
        self._log(message, extra, **kwargs)

    def error(self, message: str, extra: dict | None = None, **kwargs):
        self._log(message, extra, **kwargs)

    def critical(self, message: str, extra: dict | None = None, **kwargs):
        self._log(message, extra, **kwargs)

    def exception(
        self, message: str | None = None, extra: dict | None = None, **kwargs
    ):
        extra = extra or {}
        extra["exc_info"] = sys.exc_info()
        self._log(message, extra, **kwargs)

    def _log(self, message: str, extra: dict | None = None, **kwargs):
        args = [x for x in (message, extra) if x]
        # Use _stack_offset=4 to get to the original source line that
        #  invoked the log statement, which is 4 frames above in the stack.
        self.stderr_console.log(*args, _stack_offset=4, **kwargs)
