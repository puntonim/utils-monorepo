from typing import Any


def is_truthy(value: Any):
    # Def: https://developer.mozilla.org/en-US/docs/Glossary/Truthy
    if isinstance(value, str):
        if value.lower().strip() in ("true", "yes"):
            return True
        return False
    return bool(value)
