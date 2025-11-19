from threading import local

import pytest

from retry_utils import MaxRetriesReached, RetryException, retry_if_exc

# Data that belongs to the thread.
# Necessary because we run tests with pytest-xdist that uses threads.
data_local = local()


@retry_if_exc(
    n_retries_after_1st_failure=10,
    sleep_sec=0,
    do_not_raise_exc_on_max_retries_reached=False,
)
def gimme_five_10_retries():
    data = return_none_if_less_5()
    if data is None:
        raise RetryException
    return data


@retry_if_exc(
    n_retries_after_1st_failure=4,
    sleep_sec=0,
    do_not_raise_exc_on_max_retries_reached=False,
)
def gimme_five_4_retries():
    data = return_none_if_less_5()
    if data is None:
        raise RetryException
    return data


@retry_if_exc(
    n_retries_after_1st_failure=3,
    sleep_sec=0,
    do_not_raise_exc_on_max_retries_reached=False,
)
def gimme_five_3_retries():
    data = return_none_if_less_5()
    if data is None:
        raise RetryException
    return data


@retry_if_exc(
    n_retries_after_1st_failure=0,
    sleep_sec=0,
    do_not_raise_exc_on_max_retries_reached=False,
)
def gimme_five_0_retries():
    data = return_none_if_less_5()
    if data is None:
        raise RetryException
    return data


def return_none_if_less_5():
    if not hasattr(data_local, "count"):
        data_local.count = 0

    data_local.count += 1

    if data_local.count < 5:
        return None
    return data_local.count


class TestRetry:
    def setup_method(self):
        data_local.count = 0

    def test_0_retries(self):
        with pytest.raises(MaxRetriesReached):
            gimme_five_0_retries()
        assert data_local.count == 1

    def test_3_retries(self):
        with pytest.raises(MaxRetriesReached):
            gimme_five_3_retries()
        assert data_local.count == 4

    def test_4_retries(self):
        assert gimme_five_4_retries() == 5
        assert data_local.count == 5

    def test_10_retries(self):
        assert gimme_five_10_retries() == 5
        assert data_local.count == 5
