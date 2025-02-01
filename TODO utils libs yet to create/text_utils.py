import re


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
