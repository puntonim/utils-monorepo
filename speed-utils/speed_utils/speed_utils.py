"""
** SPEED UTILS **
==================

```py
import speed_utils

speed_utils.minpkm_base10_to_base60(5.05) -> "5:03"
```
"""

import importlib

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "minpkm_base10_to_base60",
    "mps_to_minpkm_base10",
    "mps_to_kmph",
    "minpkm_base60_to_base10",
    "minpkm_base10_to_mps",
    "kmph_to_mps",
]


# Note: works also with Pandas DataFrame:
# def minpkm_base10_to_base60(x: float | int | pd.DataFrame) -> str | pd.DataFrame:
def minpkm_base10_to_base60(x: float | int) -> str:
    """
    Eg. 5.05 min/km -> 5:03 min/km.
        minpkm_base10_to_base60(5.05) -> "5:03".
    """
    # Hack: support also Pandas' DataFrame (without importing it).
    if x.__class__.__name__ == "DataFrame":
        return x.map(minpkm_base10_to_base60)

    if not isinstance(x, (float, int)):
        raise ValueError(
            f"Only float and int arg supported (even inside a Pandas DataFrame), not: {x}"
        )

    ## This was the code I wrote.
    # int_val = floor(x)
    # dec_val = round((x - int_val) * 60)
    # if dec_val == 60:
    #     int_val += 1
    #     dec_val = 0
    # return f"{int_val}:{dec_val:02d}"

    # And this is the code written by Gemini.
    mins, secs = divmod(round(x * 60), 60)
    return f"{mins}:{secs:02d}"


# Note: works also with Pandas DataFrame:
# def minpkm_base60_to_base10(x: str | pd.DataFrame) -> float | pd.DataFrame:
def minpkm_base60_to_base10(x: str) -> float:
    """
    Eg. 5:03 min/km -> 5.05 min/km.
        minpkm_base60_to_base10("5:03") -> 5.05.
    """
    # Hack: support also Pandas' DataFrame (without importing it).
    if x.__class__.__name__ == "DataFrame":
        return x.map(minpkm_base60_to_base10)

    exc_msg = (
        f'only str arg like "5:03" supported (even inside a Pandas DataFrame), not: {x}'
    )
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


# Note: works also with Pandas DataFrame:
# def mps_to_minpkm_base10(x: float | int | pd.DataFrame) -> float | pd.DataFrame:
def mps_to_minpkm_base10(x: float | int) -> float:
    """
    Eg. 3.3 m/s -> 5.05 min/km.
        mps_to_minpkm_base10(3.3) -> 5.05
    Note that 5.05 min/km could then be converted to base60 to 5:03 min/km.
    """
    if isinstance(x, (float, int)) and x == 0:
        return 0
    # Hack: support also Pandas' DataFrame (without importing it).
    if not isinstance(x, (float, int)) and x.__class__.__name__ != "DataFrame":
        raise ValueError(
            f"only float, int arg supported (even inside a Pandas DataFrame), not {type(x)}"
        )
    result = 60 / (x * 3.6)

    if result.__class__.__name__ == "DataFrame":
        try:
            np = importlib.import_module("numpy")
        except ImportError as exc:
            raise ImportError(
                "The given arg is a Pandas DataFrame but it's impossible to import pandas"
            ) from exc
        # If x is a Pandas DataFrame that includes a 0, then its result is infinite
        #  (because of the division by 0). Replace infinite with 0 to fix this.
        result.replace([np.inf, -np.inf], 0, inplace=True)

    return result


# Note: works also with Pandas DataFrame:
# def minpkm_base10_to_mps(x: float | int | pd.DataFrame) -> float | pd.DataFrame:
def minpkm_base10_to_mps(x: float | int) -> float:
    """
    Eg. 5.05 min/km -> 3.3 m/s.
        minpkm_base10_to_mps(5.05) -> 3.3
    """
    if isinstance(x, (float, int)) and x == 0:
        return 0
    # Hack: support also Pandas' DataFrame (without importing it).
    if not isinstance(x, (float, int)) and x.__class__.__name__ != "DataFrame":
        raise ValueError(
            f"only float, int arg supported (even inside a Pandas DataFrame), not {type(x)}"
        )
    result = 60 / (x * 3.6)

    if result.__class__.__name__ == "DataFrame":
        try:
            np = importlib.import_module("numpy")
        except ImportError as exc:
            raise ImportError(
                "The given arg is a Pandas DataFrame but it's impossible to import pandas"
            ) from exc
        # If x is a Pandas DataFrame that includes a 0, then its result is infinite
        #  (because of the division by 0). Replace infinite with 0 to fix this.
        result.replace([np.inf, -np.inf], 0, inplace=True)

    return result


# Note: works also with Pandas DataFrame:
# def mps_to_kmph(x: float | int | pd.DataFrame) -> float | pd.DataFrame:
def mps_to_kmph(x: float | int) -> float:
    """
    Eg. 4.344 m/s -> 15.6384 min/km.
        mps_to_kmph(4.344) -> 15.6384
    """
    # Hack: support also Pandas' DataFrame (without importing it).
    if not isinstance(x, (float, int)) and x.__class__.__name__ != "DataFrame":
        raise ValueError(
            f"only float, int arg supported (even inside a Pandas DataFrame), not {type(x)}"
        )
    return x * 3.6


# Note: works also with Pandas DataFrame:
# def kmph_to_mps(x: float | int | pd.DataFrame) -> float | pd.DataFrame:
def kmph_to_mps(x: float | int) -> float:
    """
    Eg. 15.6384 min/km -> 4.344 m/s.
        kmph_to_mps(15.6384) -> 4.344 m/s
    """
    # Hack: support also Pandas' DataFrame (without importing it).
    if not isinstance(x, (float, int)) and x.__class__.__name__ != "DataFrame":
        raise ValueError(
            f"only float, int arg supported (even inside a Pandas DataFrame), not {type(x)}"
        )
    return x / 3.6
