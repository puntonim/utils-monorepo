"""
** RETRY UTILS **
=================

```py
import retry_utils

@retry_utils.retry_if_exc(
    n_retries_after_1st_failure=10,
    sleep_sec=0.2,
    do_not_raise_exc_on_max_retries_reached=False,
)
def foo():
    data = fn_that_might_fail_returning_none()
    if data is None:
        raise RetryException
    return data
```

Examples:
 - palanca-monorepo/libs/tradingview-client
"""

import functools
import time

import log_utils as logger

__all__ = [
    "retry_if_exc",
    "BaseRetryException",
    "RetryException",
    "MaxRetriesReached",
]


def retry_if_exc(
    # args to the decorator.
    n_retries_after_1st_failure=5,
    sleep_sec=1,
    do_not_raise_exc_on_max_retries_reached=False,
):
    """
    Decorator that re-runs the original function in case of failure.

    Args:
        n_retries_after_1st_failure: # max retries after the 1st failed attempt.
        sleep_sec: num seconds to wait between attempts.
        do_not_raise_exc_on_max_retries_reached: True to avoid raising MaxRetriesReached
         when the max # retries is reached.
    """

    def _retry_if_raises_wrapper(fn):  # `fn` is the decorated original function.
        @functools.wraps(fn)
        # `fn_args` and `fn_kwargs` are those to the decorated original function.
        def _retry_if_raises_wrapped(*fn_args, **fn_kwargs):
            i = 0
            exc = None
            while i <= n_retries_after_1st_failure:
                if i > 0 and sleep_sec:
                    logger.info(
                        f"retry_if_exc: about to sleep for {sleep_sec} sec before retrying..."
                    )
                    time.sleep(sleep_sec)
                try:
                    return fn(*fn_args, **fn_kwargs)
                except RetryException as _exc:
                    logger.info(f"retry_if_exc: detected failure in attempt #{i + 1}")
                    i += 1
                    exc = _exc
            if not do_not_raise_exc_on_max_retries_reached:
                raise MaxRetriesReached(str(exc)) from exc

        return _retry_if_raises_wrapped

    return _retry_if_raises_wrapper


class BaseRetryException(Exception): ...


class RetryException(BaseRetryException): ...


class MaxRetriesReached(BaseRetryException): ...
