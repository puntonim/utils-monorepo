"""
** SPEED UTILS **
==================

```py
import speed_utils

speed_utils.minpkm_base10_to_base60(5.05) -> "5:03"
```
"""

from math import floor

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "minpkm_base10_to_base60",
    "mps_to_minpkm_base10",
    "mps_to_kmph",
    "minpkm_base60_to_base10",
    "minpkm_base10_to_mps",
    "kmph_to_mps",
]


def minpkm_base10_to_base60(x: float | int) -> str:
    """
    Eg. 5.05 min/km -> 5:03 min/km.
        minpkm_base10_to_base60(5.05) -> "5:03".
    """
    if not isinstance(x, (float, int)):
        raise ValueError("only float and int arg supported")
    int_val = floor(x)
    dec_val = round((x - int_val) * 60)
    if dec_val == 60:
        int_val += 1
        dec_val = 0
    return f"{int_val}:{dec_val:02d}"


def minpkm_base60_to_base10(x: str) -> float:
    """
    Eg. 5:03 min/km -> 5.05 min/km.
        minpkm_base60_to_base10("5:03") -> 5.05.
    """
    exc_msg = 'only str arg like "5:03" supported'
    if not isinstance(x, str):
        raise ValueError(exc_msg)
    tokens = x.split(":")
    if len(tokens) != 2:
        raise ValueError(exc_msg)
    try:
        minute = int(tokens[0])
        second = int(tokens[1])
    except ValueError as exc:
        raise ValueError(exc_msg) from exc

    return round(minute + second / 60, 2)


def mps_to_minpkm_base10(x: float | int) -> float:
    """
    Eg. 3.3 m/s -> 5.05 min/km.
        mps_to_minpkm_base10(3.3) -> 5.05
    Note that 5.05 min/km could then be converted to base60 to 5:03 min/km.
    """
    # Hack: support also Pandas' DataFrame (without importing it).
    if not isinstance(x, (float, int)) and x.__class__.__name__ != "DataFrame":
        raise ValueError(f"only float, int and DataFrame arg supported, not {type(x)}")
    return 60 / (x * 3.6)


def minpkm_base10_to_mps(x: float | int) -> float:
    """
    Eg. 5.05 min/km -> 3.3 m/s.
        minpkm_base10_to_mps(5.05) -> 3.3
    """
    # Hack: support also Pandas' DataFrame (without importing it).
    if not isinstance(x, (float, int)) and x.__class__.__name__ != "DataFrame":
        raise ValueError(f"only float, int and DataFrame arg supported, not {type(x)}")
    return 60 / (x * 3.6)


def mps_to_kmph(x: float | int) -> float:
    """
    Eg. 4.344 m/s -> 15.6384 min/km.
        mps_to_kmph(4.344) -> 15.6384
    """
    # Hack: support also Pandas' DataFrame (without importing it).
    if not isinstance(x, (float, int)) and x.__class__.__name__ != "DataFrame":
        raise ValueError(f"only float, int and DataFrame arg supported, not {type(x)}")
    return x * 3.6


def kmph_to_mps(x: float | int) -> float:
    """
    Eg. 15.6384 min/km -> 4.344 m/s.
        kmph_to_mps(15.6384) -> 4.344 m/s
    """
    # Hack: support also Pandas' DataFrame (without importing it).
    if not isinstance(x, (float, int)) and x.__class__.__name__ != "DataFrame":
        raise ValueError(f"only float, int and DataFrame arg supported, not {type(x)}")
    return x / 3.6
