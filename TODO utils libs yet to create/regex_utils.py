import re
from sre_constants import error


def is_valid_regex(pattern: str):
    try:
        re.compile(pattern)
    except error:
        # Eg. the pattern "[".
        return False
    except Exception:
        # The stock exception `error` should suffice, but just in case, we catch all exceptions.
        return False
    return True
