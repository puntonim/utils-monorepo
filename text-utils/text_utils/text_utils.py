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
    "Emoji",
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


class Emoji:
    # Choose an emoji at https://emojipedia.org/
    #  and see the technical info.

    GREEN_CIRCLE = "\U0001F7E2"
    ORANGE_CIRCLE = "\U0001F7E0"
    RED_CIRCLE = "\U0001F534"

    CHECK_MARK1 = "\U0000FE0F"
    CHECK_MARK2 = "\U00002714"
    CROSS_MARK = "\U0000274C"
    POLICE_CAR_LIGHT = "\U0001F6A8"

    THREE_O_CLOCK = "\U0001F552"
    RED_QUESTION_MARK = "\U00002753"
    HOURGLASS_NOT_DONE = "\U000023F3"
    ENVELOPE = "\U00002709"
    RIGHT_ARROW = "\U000027A1"
    STAR = "\U00002B50"
    MUSCLE = "\U0001F4AA"
