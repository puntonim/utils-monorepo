"""
** JSON UTILS **
================
```py
import json
import json_utils

data = {"date": datetime(2025, 1, 1)}
json_utils.to_json_string(data, indent=4)

json.dumps(data, cls=json_utils.CustomJsonEncoder)
```
"""

import contextlib
import inspect
import json
import warnings
from datetime import datetime
from typing import Any
from uuid import UUID

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "CustomJsonEncoder",
    "to_json_string",
    "to_json",
    "prettify_to_non_json_string",
]


def to_json_string(data: Any, sort_keys=False, **kwargs) -> str:
    """
    Convert a Python object to a JSON string.
    The advantage, compared to a plain json.dumps(), is that it can handle types like
     datetime, bytes, UUID, that would raise a TypeError with a plain json.dumps().

    Args:
        data: any Python object.
        sort_keys: True to sort keys in the JSON string (if the JSON is a map or list).
        **kwargs: passed down to json.dumps(...), eg. `indent=4`.

    Usage:
        data = {"date": datetime(2025, 1, 1)}
        json_utils.to_json(data, indent=4)
    """
    return json.dumps(data, cls=CustomJsonEncoder, sort_keys=sort_keys, **kwargs)


def to_json(*args, **kwargs) -> str:
    """
    ** DEPRECATED **
    Use to_json_string() instead, which is exactly the same but with a better name.
    """
    text = "to_json() is deprecated; use to_json_string()"
    # Give some context to help trace where it is used.
    with contextlib.suppress(Exception):
        stack = inspect.stack()[1]
        text += "\nLikely `to_json()` is used here:"
        text += f"\n\tfile: {stack.filename}"
        text += f"\n\tline: {stack.lineno}"
        text += f"\n\tsrc: {stack.code_context}"
    warnings.warn(text, DeprecationWarning)
    return to_json_string(*args, **kwargs)


class CustomJsonEncoder(json.JSONEncoder):
    """
    A custom JSON encoder that can handle types like datetime, bytes, UUID, etc,
     unlike the std lib default encoder.

    Usage:
        import json
        data = {"date": datetime(2025, 1, 1)}
        json.dumps(data, cls=CustomJsonEncoder)
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, bytes):
            return obj.decode()
        elif obj.__class__.__name__ == "Decimal":
            # It's the Decimal class coming from DynamoDB and
            #  we don't want to import its lib, so we check for the
            #  class name.
            return float(obj)
        elif obj.__class__.__name__ == "Url":
            # It's the pydantic.HttpUrl class coming from pydantic and
            #  we don't want to import its lib, so we check for the
            #  class name.
            return str(obj)
        elif hasattr(obj, "to_dict") and callable(obj.to_dict):
            return obj.to_dict()
        elif isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def prettify_to_non_json_string(text: str):
    """
    Take a string (likely a JSON string) and performs char replacements
     like "\\n" to "\n" and similar.

    This is useful when the input JSON string is an object (a dict) containing strings
     that contains fi. new lines encoded as "\\n" (because you cannot use an actual
     new line inside a string in JSON). This function replaces "\\n" with an actual
     new line, so making the string not a JSON string anymore, but more
     human-readable.

    Example:
        text = \"""
            {
                "id": "39296166250439623962212092407450232854575369122363277321",
                "timestamp": 1762101037459,
                "message": "[ERROR] UnhealthEndpointException\nTraceback (most recent call last):\n\u00a0\u00a0File \"/opt/python/aws_lambda_powertools/logging/logger.py\", line 548, in decorate\n\u00a0\u00a0\u00a0\u00a0return lambda_handler(event, context, *args, **kwargs)\n\u00a0\u00a0File \"/var/task/botte_be/views/endpoint_introspection_view.py\", line 170, in lambda_handler\n\u00a0\u00a0\u00a0\u00a0raise UnhealthEndpointException(ts=now)"
            }
        \"""

        text = prettify_to_non_json_string(text)
        \"""
        {
            "id": "39296166250439623962212092407450232854575369122363277321",
            "timestamp": 1762101037459,
            "message": "[ERROR] UnhealthEndpointException
        Traceback (most recent call last):
          File "/opt/python/aws_lambda_powertools/logging/logger.py", line 548, in decorate
            return lambda_handler(event, context, *args, **kwargs)
          File "/var/task/botte_be/views/endpoint_introspection_view.py", line 170, in lambda_handler
            raise UnhealthEndpointException(ts=now)"
        }
        \"""
    """
    text = (
        text.replace("\\n", "\n")  # \n -> new line.
        .replace("\\u00a0", " ")  # \\u00a0 -> space.
        .replace('\\"', '"')  # \\" -> ".
    )
    return text
