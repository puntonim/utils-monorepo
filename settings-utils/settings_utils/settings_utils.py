"""
** SETTINGS UTILS **
====================

```py
import settings_utils

settings_utils.get_string_from_env("DB_USER", "XXX")
```
"""

import importlib
import json
import os
from pathlib import Path
from typing import Callable

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "get_string_from_env",
    "get_bool_from_env",
    "get_string_from_env_or_file",
    "copy_settings",
    "get_string_from_env_or_aws_parameter_store",
]


class _DEFAULT:
    pass


def get_string_from_env(key: str, default: str | None = _DEFAULT):
    value = os.getenv(key, "").strip()
    if not value:
        if default == _DEFAULT:
            raise KeyError
        return default
    return value


def get_bool_from_env(key: str, default: bool | None = _DEFAULT):
    value = os.getenv(key, "").lower().strip()
    if not value:
        if default == _DEFAULT:
            raise KeyError
        return default
    return value in ("true", "yes", "t", "y")


def get_string_from_env_or_file(
    env_key: str,
    json_file_path: str | Path,
    json_file_getter_fn: Callable,
    default: str | None = _DEFAULT,
    is_env_string_json=False,
):
    """
    Warning: storing secrets as plain-text in local files is not recommended.
    Check out `get_string_from_env_or_aws_parameter_store()`, instead, and store your
     secrets in AWS Parameter Store.
    """
    try:
        value = get_string_from_env(env_key)
    except KeyError:
        value = None

    if value and is_env_string_json:
        # Hack: store JSON strings as env vars (or in Parameter store) with
        #  a starting and ending single quote, like '{"foo": "bar"}'.
        value = value.replace("'", "")
        value = json.loads(value)

    if value is None:
        with open(json_file_path) as fin:
            data = json.load(fin)
        value = json_file_getter_fn(data)

    if value is None:
        if default == _DEFAULT:
            raise KeyError
        value = default
    return value


def get_string_from_env_or_aws_parameter_store(
    env_key: str,
    param_store_key_path: str | Path,
    default: str | None = _DEFAULT,
    is_value_json=False,
    param_store_cache_ttl: int | None = None,
    do_skip_param_store_cache=False,
):
    """
    Read a string from env vars (eg. in PROD for AWS Lambda projects) or from
     AWS Param Store (eg. in TEST for AWS Lambda projects, when running tests or
     recording test cassettes).
    This is way better than using a local file with the secret in plain-text.

    The typical usage, for a **Lambda**, is:
     - PROD settings: use Serverless to write env vars read from Param Store, then
        use `get_string_from_env()` in the class `_Settings`.
     - TEST settings: use `get_string_from_env_or_aws_parameter_store()` in the class
        `_TestSettings`, and make it a @property (see example down here)

    Mind that the actual settings' attribute needs to be a @property for lazily
     evaluation, so vcr.py can catch it on time.
    And also, mind that in conftest.py you have to use the fixture
     `clear_cache_for_aws_param_store_client()` to clear AWS Param Store client cache,
     to make its HTTP interactions deterministic (otherwise vcr.py fails).

    Note: this fn is available only if (pip-)installed with the extra `get-from-aws-param-store`.
     So, if you follow the pattern shown down here, then:
     $ poetry add git+https://github.com/puntonim/utils-monorepo#subdirectory=settings-utils
     $ poetry add -G test "git+https://github.com/puntonim/utils-monorepo#subdirectory=settings-utils[get-from-aws-param-store]"
     This will install the AWS Param Store Client only as test req.

    Args:
        env_key: name of the env var.
        parameter_store_key_path: path in AWS Param Store.
        default: default value, if the string is not found in the env var nor in Param Store.
        is_value_json: True for JSON value.
        param_store_cache_ttl: time-to-live for the Python in-memory cached params from AWS Param Store, seconds.
        do_skip_param_store_cache: skip the Python in-memory cache for AWS Param Store.

    Example, from:
     https://github.com/puntonim/botte-monorepo/tree/main/projects/botte-be:
     Copy the code from botte-be itself, as it includes useful comments.

        File: conf/settings_module.py
        ```py
        from abc import ABC
        import settings_utils

        IS_TEST = False

        class _BaseSettings(ABC):
            def __getattribute__(self, name):
                if name == "IS_TEST":
                    return IS_TEST
                if IS_TEST and hasattr(test_settings, name):
                    return getattr(test_settings, name)
                return super().__getattribute__(name)

        class _Settings(_BaseSettings):
            APP_NAME = "Botte BE"
            DO_ENABLE_API_AUTHORIZER = True
            API_AUTHORIZER_TOKEN = settings_utils.get_string_from_env(
                "API_AUTHORIZER_TOKEN", "XXX"
            )
            TELEGRAM_TOKEN = settings_utils.get_string_from_env(
                "TELEGRAM_TOKEN", "XXX"
            )

        class _TestSettings:
            @property
            def TELEGRAM_TOKEN(self):
                return settings_utils.get_string_from_env_or_aws_parameter_store(
                    env_key="TELEGRAM_TOKEN",
                    param_store_key_path="/botte-be/prod/telegram-token",
                    default="XXX",
                    param_store_cache_ttl=60,
                )

        settings = _Settings()
        test_settings = _TestSettings()
        ```

        File: tests/conftest.py
        ```py
        from botte_be.conf import settings_module

        @pytest.fixture(autouse=True, scope="session")
        def test_settings_fixture():
            settings_module.IS_TEST = True
        ...
        @pytest.fixture(autouse=True, scope="function")
        def clear_cache_for_aws_param_store_client():
            aws_parameter_store_client.cache.clear_cache()
        ```
    """
    try:
        # Since this requires an extra req, dynamically import requirements.
        AwsParameterStoreClient = importlib.import_module(
            "aws_parameter_store_client"
        ).AwsParameterStoreClient
    except ImportError as exc:
        msg = (
            "The extra lib `aws-parameter-store-client` is required in order to use"
            " `get_string_from_env_or_aws_parameter_store()`; you should:"
            " pip install settings-utils[get-from-aws-param-store]"
        )
        raise Exception(msg) from exc

    try:
        value = get_string_from_env(env_key)
    except KeyError:
        value = None

    if value is None:
        kwargs = dict(
            path=param_store_key_path,
            do_skip_cache=do_skip_param_store_cache,
        )
        if param_store_cache_ttl is not None:
            kwargs["cache_ttl"] = param_store_cache_ttl
        value = AwsParameterStoreClient().get_secret(**kwargs)

    if value and is_value_json:
        # Hack: store JSON strings as env vars (or in Parameter store) with
        #  a starting and ending single quote, like '{"foo": "bar"}'.
        value = value.replace("'", "")
        value = json.loads(value)

    if value is None:
        if default == _DEFAULT:
            raise KeyError
        value = default
    return value


def copy_settings(from_, to_):
    """
    Copy all settings from a class to another.
    Typically used to copy `test_settings` to `settings` in `pytest.py`.
    """
    attr_names = [
        attr
        for attr in dir(from_)
        if not callable(getattr(from_, attr)) and not attr.startswith("__")
    ]
    for attr_name in attr_names:
        attr_value = getattr(from_, attr_name)
        setattr(to_, attr_name, attr_value)
