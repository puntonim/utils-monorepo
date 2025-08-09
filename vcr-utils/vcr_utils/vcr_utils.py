"""
** VCR UTILS **
====================

Like [VCR.py](https://vcrpy.readthedocs.io/) but not limited to HTTP interactions.
Instead, it stubs an entire function/method (via pickle) and replays it back later.

So it can be used when unit testing software that makes local socket or Websocket or TCP
 connections. Or literally anything else, since what's stubbed is a Python
 function/method, not a connection.

You can see an example in the unit tests in this package.
Or an actual usage in tws-api-client (local socket) or tradingview-client (Websocket)
 in patatrack-monorepo.

Example
-------
Suppose you wrote a client for a service running in a local process that accepts socket
 connections (non-HTTP otherwise you would use vcr.py):
```py
class TwsApiClient:
    def get_trades(self) -> list[dict]:

        # This is the public method used by the consumer.
        raw_trades = self.get_raw_trades()

        # TODO do something with the raw_trades: typically validate the returned data,
        #   or catch exceptions and re-raise custom exceptions.

        return raw_trades

    def get_raw_trades(self) -> list[dict]:
        # In order to use @vcr_utils you always have to define a method that handles
        #  only the behavior to be stubbed, in this case the local socket request to
        #  the local process.
        # There should be no code here apart from just making the socket request.
        # It's the method that will be stubbed by @vcr_utils in unit tests.

        # TODO simulating the socket request and pretending it returns a dict.
        # raw_trades = local socket connection and request .....
        raw_trades = [
            dict(symbol="AAPL", quantity=2, avg_price=100.15),
            dict(symbol="NVDA", quantity=-5, avg_price=324.08),
        ]

        return raw_trades
```

This is how you would test it:
```py
from vcr_utils import vcr_utils
from mylib.tws_api_client import TwsApiClient

class TestTwsApiClient:
    @vcr_utils(
        "mylib.tws_api_client.TwsApiClient.get_raw_trades"
    )
    def test_happy_flow(self):
        client = TwsApiClient()
        trades = client.get_trades()
        assert trades[0] == dict(symbol="AAPL", quantity=2, avg_price=100.15)
        assert trades[1] == dict(symbol="NVDA", quantity=-5, avg_price=324.08)
```
"""

import functools
import inspect
import os
import pickle
from pathlib import Path
from unittest.mock import _get_target, patch

# Objects exported to the `import *` in `__init__.py`.
__all__ = ["vcr_utils"]


class _DEFAULT:
    pass


def _get_bool_from_env(key: str, default: bool | None = _DEFAULT):
    # Src: https://github.com/puntonim/utils-monorepo/blob/main/settings-utils/settings_utils/settings_utils.py
    value = os.getenv(key, "").lower().strip()
    if not value:
        if default == _DEFAULT:
            raise KeyError
        return default
    return value in ("true", "yes", "t", "y")


def vcr_utils(str_callable_to_be_stubbed):
    """
    Decorator @vcr_utils to be used to record/replay the stub for the given
     function/method.
    Use it to decorate unit tests functions/methods only.

    See the docstring at the top of this module to know more.

    Args:
        str_callable_to_be_stubbed: arg to the decorator, the original func/method to
         be stubbed; it's the string to be used for mock.patch(), eg. "tws_api_client.TwsApiClient.get_raw_trades".
    """
    # Get the actual function/method from the string str_callable_to_be_stubbed.
    # Eg. str_callable_to_be_stubbed="tws_api_client.TwsApiClient.get_raw_trades" -> the atcual method get_raw_trades().
    # getter eg.: functools.partial(<function resolve_name at 0x107b73600>, 'tws_api_client.TwsApiClient')
    # attribute: "get_raw_trades".
    getter, attribute = _get_target(str_callable_to_be_stubbed)
    # orig_callable eg.: <function TwsApiClient.get_raw_trades at 0x10b9c2840>
    orig_callable = getattr(getter(), attribute)

    # Keep track of the actual unit test func/method being decorated with @stub_player.
    cur_test_fn = None

    def spy(zelf, *args, **kwargs):
        """
        A test spy that is executed instead of the original func/method.
        In record-mode, it invokes the original func/method, pickle the result and store
         it in the cassette. In replay-mode, it unpickle the cassette and return it.
        Args:
            zelf: the `self` passed to the original func/method.
            *args: args passed to the original func/method.
            **kwargs: kwargs passed to the original func/method.
        """
        # File path where the decorated unit test is.
        cur_test_file = Path(inspect.getfile(cur_test_fn))
        # Dir where to store the cassette (.pickle file).
        cassette_dir = cur_test_file.parent / "cassettes" / cur_test_file.name
        # Path of the cassette (.pickle file).
        cassette_file = cassette_dir / (cur_test_fn.__qualname__ + ".pickle")

        is_record_mode = _get_bool_from_env("DO_RECORD_STUBS", False)

        if is_record_mode:
            # Run the original func/method, pickle the result and store it in the
            #  cassette.
            result = orig_callable(zelf, *args, **kwargs)
            os.makedirs(cassette_dir, exist_ok=True)
            with open(cassette_file, "wb") as fout:
                pickle.dump(result, fout, protocol=5)
        else:
            # Do not run the original function, but instead unpickle the casette and
            #  return it.
            if not cassette_file.is_file():
                raise CassetteNotFound(cassette_file)
            with open(cassette_file, "rb") as fin:
                result = pickle.load(fin)

        return result

    def wrapper(test_fn):  # `test_fn` is the decorated function, so the unit test case.
        @functools.wraps(test_fn)
        def wrapped_fn(
            # These are the args to the decorated function (the unit test case).
            *test_fn_args,
            **test_fn_kwargs,
        ):
            nonlocal cur_test_fn
            cur_test_fn = test_fn

            # mock.patch() the given function/method, so that we can either record its
            #  result or replay it back.
            with patch(
                str_callable_to_be_stubbed,
                side_effect=spy,
                autospec=True,
            ):
                result = test_fn(*test_fn_args, **test_fn_kwargs)
            return result

        return wrapped_fn

    return wrapper


class BaseVcrUtilsException(Exception):
    pass


class CassetteNotFound(BaseVcrUtilsException):
    def __init__(self, path):
        super().__init__("Use DO_RECORD_STUBS=y to record new stubs")
        self.path = path
