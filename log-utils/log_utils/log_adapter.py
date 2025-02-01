"""
** LOG UTILS **
===============

Log Adapter is the entry point for log-utils lib.

Log-utils is meant to be used by:
 A. projects (cli, webapps, AWS Lambda, ...) that use libs in this utils-monorepo
 B. any project or lib (that do NOT use libs in this utils-monorepo)

See README.md to know how to install log-utils.


A - PROJECTS THAT USE LIBS IN utils-monorepo
============================================
Log-utils is used by other libs in this utils-monorepo in order to log entries
 in a way that works for any project (that use std lib or loguru or others).
And libs in this utils-monorepo can be part of different projects like an AWS Lambda
 project (eg. Job Scheduler, Slackbot) or a CLI (eg. Events Publisher released as
 Docker image).
So, those libs need to **be able to log entries in such a way that works for different
 projects**.

How it works
------------
The idea is:
 - Libs in this utils-monorepo import log-utils (`import log_utils as logger`) and
    have generic log statements like `logger.info("Done")`.
 - Projects that requires libs in this utils-monorepo that use log-utils must import
    log-utils (`import log_utils as logger`), then set the right adapter (loguru,
    AWS Powertools, rich or std lib's logging module) with
    `logger.set_adapter(logger.LoguruAdapter())` and finally have log statements
    like `logger.info("START")` where the logger is either from log-utils or
    from loguru|powertools directly.

Example: CLI project (released as Docker image)
-----------------------------------------------
Actual examples:
 - ibkr-cli in patatrack-monorepo, CLI with Rich:
     https://github.com/puntonim/patatrack-monorepo/blob/770092dabc3b6fb8dc3a9f03cea6b4ca15055a1c/projects/ibkr-cli/ibkr_cli/cli.py#L31
 - event-publisher, Docker CLI with Loguru:
     hdmap-web/projects/event-publisher/event_publisher/cli.py

My new project "space" pip-installs the lib `peewee-utils` (or any other lib in
 utils-monorepo) that requires `log-utils`.
The project "space" invokes `set_adapter(...)` with a `LoguruAdapter` so that
 `peewee-utils` logs entries using Loguru (instead of the default std libs's logging
 module).

So, in project "space", in the main `cli.py`:
```py
import log_utils as logger

loguru = logger.LoguruAdapter()
# Now, if loguru hasn't been configured for the "Space" project yet, then we can:
# loguru.configure_default(do_enable_file_logging=True, log_file_name="map-cli.log")
logger.set_adapter(loguru)

## Or, if the project was to use rich:
# rich = logger.RichAdapter()
# logger.set_adapter(rich)
```
and now anywhere in the project we can:
```py
# Now we can log either using logger from log-utils or loguru:
import log_utils as logger  # Or: from loguru import logger.
logger.debug("START")
```

Note: the `peewee-utils` lib contains log entries that are agnostic of the actual
 adapter in use, like:
```py
import log_utils as logger
logger.debug("Hello", extra={"color": "red"})
```

Example: AWS Lambda project
---------------------------
Actual examples:
 - odd-manager, AWS Lambda REST API with Powertools:
     hdmap-web/projects/odd-manager/odd_manager/views/endpoints/odd_definition_view/read_all_view.py

My new project "space" pip-installs the lib `peewee-utils` (or any other lib in
 utils-monorepo) that requires `log-utils`.
The project "space" invokes `set_adapter(...)` with a `PowertoolsLoggerAdapter` so
 that `peewee-utils` logs entries using Powertools (instead of the default std libs's
 logging module).

So, in project "space", in every lambda handler (view):
```py
import log_utils as logger
powertools_logger = logger.PowertoolsLoggerAdapter()
# Now we can either invoke `configure_default()` or configure directly Powertools
#  in the project.
# powertools_logger.configure_default(
#     service_name=f"ODD Manager BE",
#     service_version=__version__,
#     is_verbose=False,
# )
logger.set_adapter(powertools_logger)
```
and now anywhere in the project we can:
```py
# Now we can log either using logger from log-utils or powertools:
import log_utils as logger  # Or: from aws_lambda_powertools import Logger; logger = Logger(...).
logger.debug("START")
```

Note: the `peewee-utils` lib contains log entries that are agnostic of the actual
 adapter in use, like:
```py
import log_utils as logger
logger.debug("Hello", extra={"color": "red"})
```


B. ANY PROJECT OR LIB
=====================
Any project or lib, that do NOT use libs in this utils-monorepo, can use log-utils for
 a simple logging that can be extended in the future.

My new project "space" pip-installs the lib `log-utils` for simple logging.

So, in project "space", we can log with the std logging module straight away:
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
Or we can configure StdLibLoggingAdapter and customize its defaults:
```py
import log_utils as logger

rich_log = logger.RichAdapter()
rich_log.configure_default()
logger.set_adapter(rich_log)

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
