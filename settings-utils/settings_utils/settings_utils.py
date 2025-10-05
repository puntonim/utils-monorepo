"""
** SETTINGS UTILS **
====================

```py
import settings_utils

settings_utils.get_string_from_env("DB_USER", "XXX")
```
"""

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


## Not implemented yet: see project Reborn Automator.
# def get_string_from_env_or_aws_parameter_store(
#     env_key: str,
#     parameter_store_key_path: str | Path,
#     default: str | None = _DEFAULT,
#     is_value_json=False,
# ):
#     try:
#         value = get_string_from_env(env_key)
#     except KeyError:
#         value = None
#
#     if value is None:
#         value = ParameterStoreClient().get_secret(parameter_store_key_path)
#
#     if value and is_value_json:
#         # Hack: store JSON strings as env vars (or in Parameter store) with
#         #  a starting and ending single quote, like '{"foo": "bar"}'.
#         value = value.replace("'", "")
#         value = json.loads(value)
#
#     if value is None:
#         if default == _DEFAULT:
#             raise KeyError
#         value = default
#     return value


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
