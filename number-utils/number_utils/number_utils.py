"""
** NUMBER UTILS **
==================

```py
import number_utils

number_utils.ordinal(5) -> "5th"
```
"""

from decimal import Decimal

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "count_decimal_digits",
    "ordinal",
]


def count_decimal_digits(n: float) -> int:
    """
    Count the numer of decimal digits in the given float.

    Examples:
        count_decimal_digits(0.0001) == 4
        count_decimal_digits(-13.678) == 3
        count_decimal_digits(0.00010000) == 4
    """
    n_dec = Decimal(str(n))
    exp = n_dec.as_tuple().exponent
    return abs(exp)


def ordinal(n: int) -> str:
    """
    Examples:
        ordinal(1) -> "1st"
        ordinal(5) -> "5th"
        ordinal(13) -> "13th"
        ordinal(22) -> "22nd"
    """
    suffix = {1: "st", 2: "nd", 3: "rd", 11: "th", 12: "th", 13: "th"}
    return str(n) + (suffix.get(n % 100) or suffix.get(n % 10, "th"))
