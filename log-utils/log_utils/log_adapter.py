"""
** LOG UTILS **
===============

Log Adapter is the entry point for log-utils lib.

Log-utils is meant to be used by:
    A. any library created by me, in any repository;
    B. any project (cli, webapps, AWS Lambda, ...) that uses such libs in point A;
    C. any project or lib (that does NOT use such libs in point A)

See README.md to know how to install log-utils.


A - ANY **LIBRARY** created by me
========================================================================================
Add `log_utils` as requirement:
    `$ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils`
Then:
    ```py
    import log_utils as logger

    # From anywhere in the source code, I can easily log with:
    logger.debug("Debug log from LIBRARY")
    logger.info("Info log from LIBRARY", extra=dict(color="red"))
    logger.error("Error log from LIBRARY")
    ```

Any library created by me should use `log_utils` for logging, like in the example above.

Example scenario:
 - I create the new library `foo-lib`, add `log-utils` as its requirement, and in its
    source code I use log statements as in the example above;
 - Then I create the new project `foo-project`, add `foo-lib` and `log-utils` as its
    requirements, and configure the rich-adapter (as explained in the next section).
 - The result is that all log statements work with rich, seamlessly.



B - ANY **PROJECT** that uses such libs in point A
========================================================================================
Add `log_utils` as requirement, with the right adapters:
    `$ poetry add "git+https://github.com/puntonim/utils-monorepo#subdirectory=log-utils[rich-adapter,loguru-adapter,powertools-adapter]"`
Then:
    ```py
    import log_utils as logger

    # To configure the std lib adapter.  <------------Typical use case: temp scripts ---
    std_lib_log = logger.StdLibLoggingAdapter()
    std_lib_log.configure_default(is_verbose=False)
    logger.set_adapter(std_lib_log)

    # Or, to configure powertools-adapter. <----------------Typical use case: Lambda ---
    powertools_logger = logger.PowertoolsLoggerAdapter()
    powertools_logger.configure_default(
        service_name=settings.APP_NAME,
        service_version=__version__,
        is_verbose=False,
    )
    logger.set_adapter(powertools_logger)

    # Or, to configure rich-adapter. <-------------------------Typical use case: CLI ---
    rich = logger.RichAdapter()
    rich.configure_default(is_verbose=False)
    logger.set_adapter(rich)

    # Or, to configure loguru-adapter. <--------------Typical use case: advanced CLI ---
    loguru = logger.LoguruAdapter()
    loguru.configure_default(do_enable_file_logging=True, log_file_name="map-cli.log")
    logger.set_adapter(loguru)


    # From anywhere in the source code, I can easily log with:
    logger.info("Info log from LIBRARY", extra=dict(color="red"))
    ```

Actual examples:
  Lambda:
     - botte-be, AWS Lambda with Powertools:
        https://github.com/puntonim/botte-monorepo/tree/main/projects/botte-be
     - odd-manager, AWS Lambda REST API with Powertools:
        hdmap-web/projects/odd-manager/odd_manager/views/endpoints/odd_definition_view/read_all_view.py

  CLI:
     - ibkr-cli in patatrack-monorepo, CLI with Rich:
         https://github.com/puntonim/patatrack-monorepo/blob/770092dabc3b6fb8dc3a9f03cea6b4ca15055a1c/projects/ibkr-cli/ibkr_cli/cli.py#L31
     - event-publisher, Docker CLI with Loguru:
         hdmap-web/projects/event-publisher/event_publisher/cli.py



C. ANY PROJECT OR LIB (that does NOT use such libs in point A)
========================================================================================
Any project or lib, that do NOT use libs that use `log-utils`, can still use `log-utils`
 for a simple logging system that can be extended in the future.

Example scenario:
 - My new project "space" pip-installs the lib `log-utils` for simple logging.
 - So, in project "space", we can log with the std logging module straight away:
    ```py
    import log_utils as logger

    # And log entries like:
    logger.info("Hello world", extra=dict(weight=81))
    ```
   Or we can configure StdLibLoggingAdapter and customize its defaults:
    ```py
    import log_utils as logger

    std_lib_log = logger.StdLibLoggingAdapter()
    std_lib_log.configure_default(level=logging.ERROR)
    logger.set_adapter(std_lib_log)

    # And log entries like:
    logger.error("Hello world", extra=dict(weight=81))
    ```
"""

import logging
import sys

from .adapters.std_lib_logging_adapter import StdLibLoggingAdapter

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "critical",
    "debug",
    "error",
    "exception",
    "flush_adapter",
    "get_adapter",
    "info",
    "set_adapter",
    "set_root_logger_to_stderr",
    "warning",
]

_LOG_ADAPTER = None


def set_adapter(adapter):
    global _LOG_ADAPTER
    if _LOG_ADAPTER:
        raise AlreadyConfigured("There is already an adapter configured")
    _LOG_ADAPTER = adapter


def get_adapter():
    global _LOG_ADAPTER
    if not _LOG_ADAPTER:
        std_logging = StdLibLoggingAdapter()
        std_logging.configure_default()
        _LOG_ADAPTER = std_logging
    return _LOG_ADAPTER


def flush_adapter():
    global _LOG_ADAPTER
    _LOG_ADAPTER = None


def set_root_logger_to_stderr():
    """
    Forcibly set the root logger to stderr.
    Some (3rd party) libs  project might use the std logging module with a root logger
     set to stdout instead of stderr.
    This is particularly annoying when developing an app that outputs JSON to stdout,
     as, in this case, stdout cannot be parsed reliably as errors are on stdout as well.
    This function solves the issue by redirecting the root logger to stderr.
    """
    root = logging.getLogger()
    if len(root.handlers) and hasattr(root.handlers[0], "stream"):
        root.handlers[0].stream = sys.stderr


def debug(message: str, extra: dict | None = None):
    """
    Debug-level logging.
    Eg. logger.debug("Nice color", extra=dict(color="red"))

    Args:
        message (str): the message string.
        extra (dict): optional extra data to be logged.
    """
    get_adapter().debug(message, extra)


def info(message: str, extra: dict | None = None):
    """
    Info-level logging.
    Eg. logger.info("Nice color", extra=dict(color="red"))

    Args:
        message (str): the message string.
        extra (dict): optional extra data to be logged.
    """
    get_adapter().info(message, extra)


def warning(message: str, extra: dict | None = None):
    """
    Warning-level logging.
    Eg. logger.warning("Nice color", extra=dict(color="red"))

    Args:
        message (str): the message string.
        extra (dict): optional extra data to be logged.
    """
    get_adapter().warning(message, extra)


def error(message: str, extra: dict | None = None):
    """
    Error-level logging.
    Eg. logger.error("Nice color", extra=dict(color="red"))

    Args:
        message (str): the message string.
        extra (dict): optional extra data to be logged.
    """
    get_adapter().error(message, extra)


def critical(message: str, extra: dict | None = None):
    """
    Critical-level logging.
    Eg. logger.critical("Nice color", extra=dict(color="red"))

    Args:
        message (str): the message string.
        extra (dict): optional extra data to be logged.
    """
    get_adapter().critical(message, extra)


def exception(message: str | None = None, extra: dict | None = None):
    """
    Log an exception. Notice that the actual exception is not given as parameter but
     it is automatically found in the stack trace.
    Eg. logger.critical("Nice color", extra=dict(color="red"))

    Args:
        message (str): the message string.
        extra (dict): optional extra data to be logged.
    """
    get_adapter().exception(message, extra)


class BaseLogUtilsException(Exception):
    pass


class AlreadyConfigured(BaseLogUtilsException):
    pass
