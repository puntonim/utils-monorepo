"""
** CRYPTOGRAPHIC HASH ALGORITHMS OVERVIEW **
============================================

Docs: https://en.wikipedia.org/wiki/Cryptographic_hash_function#Cryptographic_hash_algorithms

In brief:
- MD5 is old (1992) and with a relatively high collision prob. Very popular.
- SHA2 is old (2001) and with a relatively low collision prob, but slow.
- BLAKE2 is recent (2012) and with a low collision prob. Faster than MD5, thus the best choice.
- BLAKE3 is the most recent (2020), the fastest, promising but not popular yet.


** CHECKSUM UTILS **
====================
```py
import checksum_utils

data = "hello \n\\s\t\r &!%world"
ck = checksum_utils.md5_checksum_for_data(data)

ck = checksum_utils.md5_checksum_for_file("../myfile.txt")
```
"""

import hashlib
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable

from json_utils import json_utils

# Objects exported to the `import *` in `__init__.py`.
__all__ = [
    "blake2b_checksum_for_file",
    "md5_checksum_for_data",
    "md5_checksum_for_file",
]


def md5_checksum_for_data(
    obj: Any, do_try_json_conversion=True, custom_json_encoder=None
) -> str:
    """
    Compute MD5 for any type that is JSON serializable, like string, byte, datetime,
     UUID.
    """
    if do_try_json_conversion:
        try:
            if custom_json_encoder:
                obj = json.dumps(obj, cls=custom_json_encoder)
            else:
                obj = json_utils.to_json(obj, sort_keys=True)
        except TypeError as exc:
            pass
    if hasattr(obj, "encode"):
        obj = obj.encode()
    return hashlib.md5(obj).hexdigest()


def md5_checksum_for_file(file_path: str | Path, do_use_lru_cache: bool = True) -> str:
    """
    Compute MD5 for a file's content.
    """
    if do_use_lru_cache:
        # Use absolute file path for optimizing the lru cache.
        absolute_file_path = Path(file_path).resolve()
        # Ensure the file still exists and it is still a file.
        if not absolute_file_path.exists():
            raise FileNotFoundError
        if absolute_file_path.is_dir():
            raise IsADirectoryError
        return _md5_checksum_for_file_lru(absolute_file_path)
    return _checksum_for_file(file_path, hashlib.md5)


@lru_cache
def _md5_checksum_for_file_lru(absolute_file_path: Path):
    return _checksum_for_file(absolute_file_path, hashlib.md5)


def blake2b_checksum_for_file(
    file_path: str | Path, do_use_lru_cache: bool = True
) -> str:
    """
    Compute BLAKE2b for a file's content.
    """
    if do_use_lru_cache:
        # Use absolute file path for optimizing the lru cache.
        absolute_file_path = Path(file_path).resolve()
        # Ensure the file still exists and it is still a file.
        if not absolute_file_path.exists():
            raise FileNotFoundError
        if absolute_file_path.is_dir():
            raise IsADirectoryError
        return _blake2b_checksum_for_file_lru(absolute_file_path)
    return _checksum_for_file(file_path, hashlib.blake2b)


@lru_cache
def _blake2b_checksum_for_file_lru(absolute_file_path: Path):
    return _checksum_for_file(absolute_file_path, hashlib.blake2b)


def _checksum_for_file(file_path: str | Path, hash_fn: Callable):
    """
    Memory-optimized function to compute the checksum for a file's content.
    It accepts a callable as hash function.
    """
    # Src: https://stackoverflow.com/a/44873382
    h = hash_fn()
    block_size = 128 * 1024
    b = bytearray(block_size)
    mv = memoryview(b)
    file_path = Path(file_path)
    # Disable buffering, we have an optimized size already.
    with open(file_path, "rb", buffering=0) as f:
        # Sequentially read blocks from the file.
        # Use `readinto` to avoid buffer churning.
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()
