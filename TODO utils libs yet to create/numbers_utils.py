from decimal import Decimal


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
