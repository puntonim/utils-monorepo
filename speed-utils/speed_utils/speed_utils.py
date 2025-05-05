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
]


def minpkm_base10_to_base60(x: float) -> str:
    """
    Eg. 5.05 min/km -> 5:03 min/km.
        minpkm_base10_to_base60(5.05) -> "5:03".
    """
    int_val = floor(x)
    dec_val = round((x - int_val) * 60)
    if dec_val == 60:
        int_val += 1
        dec_val = 0
    return f"{int_val}:{dec_val:02d}"


def mps_to_minpkm_base10(x: float) -> float:
    """
    Eg. 3.3 m/s -> 5.05 min/km.
        mps_to_minpkm(3.3) -> 5.05
    Note that 5.05 min/km could then be converted to base60 to 5:03 min/km.
    """
    return 60 / (x * 3.6)
