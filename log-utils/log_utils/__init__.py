from .adapters.loguru_adapter import LoguruAdapter
from .adapters.powertools_adapter import PowertoolsLoggerAdapter
from .adapters.rich_adapter import RichAdapter
from .adapters.std_lib_logging_adapter import StdLibLoggingAdapter
from .log_adapter import (
    critical,
    debug,
    error,
    exception,
    flush_adapter,
    get_adapter,
    info,
    set_adapter,
    set_root_logger_to_stderr,
    warning,
)
