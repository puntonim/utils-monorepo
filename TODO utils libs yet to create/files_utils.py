import contextlib
import json
import mimetypes
import os
import re
from pathlib import Path
from typing import Any, Iterator, Match

from . import json_utils
from .regex import is_valid_regex

KB = 1024
MB = KB * KB


def write_file(path: Path | str, content: str = "") -> None:
    with open(path, "w") as fout:
        fout.write(content)


def write_json_file(path: Path | str, content: Any = "", **kwargs) -> None:
    with open(path, "w") as fout:
        fout.write(json_utils.to_json(content, **kwargs))


def read_json_file(path: Path | str):
    with open(path, "r") as fin:
        # `json.load` raises `JSONDecodeError: Expecting value: ...` when the file is empty.
        # return json.load(fin)
        data = fin.read()
        if not data:
            return None
        return json.loads(data)


@contextlib.contextmanager
def cd(path: Path) -> Iterator[None]:
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


class BaseFilesException(Exception):
    pass


class InvalidRegex(BaseFilesException):
    def __init__(self, pattern: str):
        self.pattern = pattern


def yield_files_in_dir(
    dir_path: Path | str,
    inclusion_pattern: str | None = None,
    do_yield_excluded: bool = False,
    do_ignore_subdirs: bool = False,
) -> Iterator[Path | tuple[Path, bool]]:
    r"""
    Yield files in a dir, (by default, recursively). Optionally use `inclusion_pattern` (a regex) to
    filter files.

    Args:
        dir_path: local directory path.
        inclusion_pattern: regex to filter files (case insensitive), eg: r"^.*\.(jpg|png)$".
        do_yield_excluded: avoid yielding files that are filtered out, according to
         the given inclusion_pattern.
        do_ignore_subdirs: true to avoid recursing on subdirectories.
    """
    if inclusion_pattern and not is_valid_regex(inclusion_pattern):
        raise InvalidRegex(inclusion_pattern)

    dir_path = Path(dir_path)
    # `*` means anything (files and dirs).
    paths = dir_path.rglob("*")  # `rglob` is recursive (on subdirs).
    if do_ignore_subdirs:
        paths = dir_path.glob("*")
    for file_path in paths:
        if not file_path.is_file() or (
            inclusion_pattern
            and not bool(re.match(inclusion_pattern, str(file_path), re.I))
        ):
            if do_yield_excluded:
                yield file_path, False
            continue

        if do_yield_excluded:
            yield file_path, True
        else:
            yield file_path


def guess_content_type(path: Path | str):
    """
    Guess the media type from the path name.
    Docs: https://docs.python.org/3/library/mimetypes.html#mimetypes.guess_type
    """
    return mimetypes.guess_type(str(path), strict=False)[0]


def find_pattern_in_file(pattern: str, path: Path | str) -> Match | None:
    """
    Extract match in file matching pattern.
    """
    compiled = re.compile(pattern)
    for line in open(path):
        match = re.match(compiled, line)
        if match:
            return match


def _round_size(size, factor, min_digits=1, max_digits=6) -> float:
    pretty_size = round(size / factor, min_digits)
    if not pretty_size > 0:
        pretty_size = round(size / factor, max_digits)
    return pretty_size


def round_bytes_to_mbytes(size, min_digits=1, max_digits=6) -> float:
    return _round_size(size, MB, min_digits, max_digits)


def round_mbytes_to_gbytes(size, min_digits=1, max_digits=9) -> float:
    return _round_size(size, KB, min_digits, max_digits)
