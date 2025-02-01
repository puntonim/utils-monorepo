import json
import os
from pathlib import Path
from typing import Callable


def get_string_from_env(key: str, default: str | None = None):
    value = os.getenv(key, "").strip()
    if not value:
        if default is None:
            raise KeyError
        return default
    return value


def get_bool_from_env(key: str, default: bool | None = None):
    value = os.getenv(key, "").lower().strip()
    if not value:
        if default is None:
            raise KeyError
        return default
    return value in ("true", "yes", "t", "y")


def get_string_from_env_or_file(
    env_key: str,
    json_file_path: str | Path,
    json_file_getter_fn: Callable,
    default: str | None = None,
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
        if default is None:
            raise KeyError
        value = default
    return value


def get_string_from_env_or_aws_parameter_store(
    env_key: str,
    parameter_store_key_path: str | Path,
    default: str | None = None,
    is_value_json=False,
):
    try:
        value = get_string_from_env(env_key)
    except KeyError:
        value = None

    if value is None:
        value = ParameterStoreClient().get_secret(parameter_store_key_path)

    if value and is_value_json:
        # Hack: store JSON strings as env vars (or in Parameter store) with
        #  a starting and ending single quote, like '{"foo": "bar"}'.
        value = value.replace("'", "")
        value = json.loads(value)

    if value is None:
        if default is None:
            raise KeyError
        value = default
    return value
