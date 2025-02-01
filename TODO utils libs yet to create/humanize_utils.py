"""
Check out the lib used here: https://github.com/python-humanize/humanize
I could add here more human-friendly functions, either from that lib or my own code.
"""

from datetime import datetime, timezone

import humanize

from . import datetime_utils


def time_diff_from_now(d: datetime | int | float, now: datetime | None = None):
    """
    Example:
        from patatrack_utils import datetime_utils, humanize_utils

        SECOND = 1
        MINUTE = 60 * SECOND
        HOUR = 60 * MINUTE

        d = datetime_utils.now_utc() + timedelta(seconds=6 * HOUR + 3 * MINUTE + 13)
        humanize_utils.time_diff_from_now(d)
        >>> "6 hours from now"
    """
    if now is None:
        now = datetime_utils.now_utc()

    if datetime_utils.is_naive(now):
        raise TypeError("Naive datetime not supported")

    if isinstance(d, datetime):
        if datetime_utils.is_naive(d):
            raise TypeError("Naive datetime not supported")
        d = d.astimezone(timezone.utc)
    else:
        now = now.timestamp()

    return humanize.naturaltime(now - d)
