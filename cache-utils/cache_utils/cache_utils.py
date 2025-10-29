"""
** CACHE UTILS **
====================

Note: there are a few more utils about WORKING DAYS AND HOLIDAYS in `ibkr-etf-trade-ideas`.

```py
import cache_utils

cache = cache_utils.CacheForTimeMap()
cache.set("mykey", "myvalue", ttl=10)
item = cache.get("mykey")
assert item == "myvalue"
```
"""

from datetime import datetime, timedelta
from typing import Any, NamedTuple

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "CacheForTimeMap",
    "BaseCacheForTimeMapException",
    "KeyNotFound",
    "ItemExpired",
    "TtlZeroOrLess",
]


class _ExpirableValue(NamedTuple):
    value: Any
    ttl: datetime


class CacheForTimeMap:
    """
    Cache keys for time, in a map data structure (dict).
    """

    def __init__(self):
        self._store: dict[str, _ExpirableValue] = dict()

    def clear_cache(self):
        self._store.clear()

    def get(self, key: str) -> Any:
        """
        Read an item from the cache.

        Args:
            key (str): item's key.
        """
        if key in self._store:
            ttl = self._store[key].ttl
            if ttl < datetime.now():
                value = self._store[key].value
                del self._store[key]
                raise ItemExpired(key, value, ttl)
            else:
                return self._store[key].value
        raise KeyNotFound(key)

    def set(self, key: str, value: Any, ttl: int) -> None:
        """
        Write an item to the cache.

        Args:
            key (str): item's key.
            value (Any): item's value.
            ttl (int): time-to-live in seconds.
        """
        if ttl <= 0:
            raise TtlZeroOrLess("TTL must be > 0")

        self._store[key] = _ExpirableValue(
            value=value, ttl=datetime.now() + timedelta(seconds=ttl)
        )


class BaseCacheForTimeMapException(Exception):
    pass


class KeyNotFound(BaseCacheForTimeMapException):
    def __init__(self, key: str):
        self.key = key


class ItemExpired(BaseCacheForTimeMapException):
    def __init__(self, key: str, value: Any, ttl: datetime):
        self.key = key
        self.value = value
        self.ttl = ttl


class TtlZeroOrLess(BaseCacheForTimeMapException): ...
