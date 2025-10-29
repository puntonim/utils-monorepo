from time import sleep

import pytest

import cache_utils


class TestCacheForTimeMap:
    def setup_method(self):
        self.key = "mykey"
        self.value = "myvalue"

    def test_happy_flow(self):
        cache = cache_utils.CacheForTimeMap()
        cache.set(self.key, self.value, ttl=1)
        item = cache.get(self.key)
        assert item == self.value

    def test_ttl_zero_or_less(self):
        cache = cache_utils.CacheForTimeMap()
        with pytest.raises(cache_utils.TtlZeroOrLess):
            cache.set(self.key, self.value, ttl=0)
        with pytest.raises(cache_utils.TtlZeroOrLess):
            cache.set(self.key, self.value, ttl=-1)

    def test_not_found(self):
        key = self.key + "XXX"
        cache = cache_utils.CacheForTimeMap()
        cache.set(self.key, self.value, ttl=1)
        with pytest.raises(cache_utils.KeyNotFound) as exc:
            cache.get(key)
        assert exc.value.key == key

    def test_expired(self):
        cache = cache_utils.CacheForTimeMap()
        cache.set(self.key, self.value, ttl=1)

        item = cache.get(self.key)
        assert item == self.value

        sleep(1)
        with pytest.raises(cache_utils.ItemExpired) as exc:
            cache.get(self.key)
        assert exc.value.key == self.key
        assert exc.value.value == self.value

    def test_clear_cache(self):
        cache = cache_utils.CacheForTimeMap()
        cache.set(self.key, self.value, ttl=1)

        item = cache.get(self.key)
        assert item == self.value

        cache.clear_cache()

        with pytest.raises(cache_utils.KeyNotFound):
            cache.get(self.key)

    def test_many_items(self):
        cache = cache_utils.CacheForTimeMap()

        for i in range(10_000):
            cache.set(f"key-{i}", f"value-{i}", ttl=5)

        for i in range(10_000):
            item = cache.get(f"key-{i}")
            assert item == f"value-{i}"

    def test_value_int(self):
        value = 34543534
        cache = cache_utils.CacheForTimeMap()
        cache.set(self.key, value, ttl=1)
        item = cache.get(self.key)
        assert item == value

    def test_value_obj(self):
        """
        The goal is to test what happens when the value is not a string or number, but
         an object, like a class.
        """
        value = TestCacheForTimeMap
        cache = cache_utils.CacheForTimeMap()
        cache.set(self.key, value, ttl=1)
        item = cache.get(self.key)
        assert item == value
