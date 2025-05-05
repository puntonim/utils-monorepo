"""
** TEXT UTILS **
================

```py
import text_utils

text_utils.snake_to_camel(test_item) -> "testItem"
```
"""

import re

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "snake_to_camel",
    "camel_to_snake",
    "truncate_text",
    "title_to_snake",
]


def snake_to_camel(text: str) -> str:
    """
    Example: test_item > testItem
    """
    result = list(text.lower().split("_"))

    for i in range(1, len(result)):
        result[i] = result[i].capitalize()
    return "".join(result)


_pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(text: str) -> str:
    """
    Example: testItem > test_item
    """
    return _pattern.sub("_", text).lower()


def title_to_snake(text: str) -> str:
    """
    Example: TestItem > test_item
    """
    text = text[:1].lower() + text[1:]
    return camel_to_snake(text)


def truncate_text(text: str, max_length: int, symbol="…"):
    """
    Eg. truncate_text("Hello world!", 4) -> 'Hell…'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + symbol
