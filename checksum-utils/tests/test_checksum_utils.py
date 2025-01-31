import tempfile
from datetime import datetime
from unittest import mock
from uuid import UUID

from checksum_utils import checksum_utils


class TestMd5ChecksumForData:
    def test_string(self):
        data = "hello \n\\s\t\r &!%world"
        ck = checksum_utils.md5_checksum_for_data(data)
        assert ck == "4d59fa55c96f97ebe056b5e35e365546"

    def test_byte(self):
        data = "hello \n\\s\t\r &!%world".encode()
        ck = checksum_utils.md5_checksum_for_data(data)
        assert ck == "4d59fa55c96f97ebe056b5e35e365546"

    def test_dict(self):
        data = {
            "today": datetime(2025, 1, 1),
            "c": "hello".encode(),
            "a": UUID("6092679c-6f53-42f8-90bd-8704a52f1774"),
        }
        ck = checksum_utils.md5_checksum_for_data(data)
        assert ck == "597bbabc635c88cd39d5cbb9ad35847a"


class TestMd5ChecksumForFile:
    HASH = "6b44e24d2a68b97c916d44c76aed6e1f"

    def test_happy_flow(self):
        with tempfile.NamedTemporaryFile() as tmp:
            with open(tmp.name, mode="w") as fout:
                fout.write("hello \n\\s\t\r &!%world")

            assert checksum_utils.md5_checksum_for_file(tmp.name) == self.HASH

    def test_lru_cache(self):
        with (
            tempfile.NamedTemporaryFile() as tmp,
            mock.patch(
                "checksum_utils.checksum_utils._checksum_for_file",
                wraps=checksum_utils._checksum_for_file,
            ) as mock_checksum_for_file,
        ):

            with open(tmp.name, mode="w") as fout:
                fout.write("hello \n\\s\t\r &!%world")

            assert (
                checksum_utils.md5_checksum_for_file(tmp.name, do_use_lru_cache=False)
                == self.HASH
            )
            assert (
                checksum_utils.md5_checksum_for_file(tmp.name, do_use_lru_cache=False)
                == self.HASH
            )
            assert mock_checksum_for_file.call_count == 2

            assert (
                checksum_utils.md5_checksum_for_file(tmp.name, do_use_lru_cache=True)
                == self.HASH
            )
            assert (
                checksum_utils.md5_checksum_for_file(tmp.name, do_use_lru_cache=True)
                == self.HASH
            )
            assert (
                checksum_utils.md5_checksum_for_file(tmp.name, do_use_lru_cache=True)
                == self.HASH
            )
            assert (
                checksum_utils.md5_checksum_for_file(tmp.name, do_use_lru_cache=True)
                == self.HASH
            )
            assert (
                checksum_utils.md5_checksum_for_file(tmp.name, do_use_lru_cache=True)
                == self.HASH
            )
            assert mock_checksum_for_file.call_count == 3

            assert (
                checksum_utils.md5_checksum_for_file(tmp.name, do_use_lru_cache=False)
                == self.HASH
            )
            assert mock_checksum_for_file.call_count == 4


class TestBlake2bChecksumForFile:
    HASH = "48bb448c6a5d247147ae20ffead5c7646532eb68b6e77fd45816587ad71e6ea31c3470cedd1a7ac6c5e356d0262b69af35ab55672e3eb8f6031967c65bf93383"

    def test_happy_flow(self):
        with tempfile.NamedTemporaryFile() as tmp:
            with open(tmp.name, mode="w") as fout:
                fout.write("hello \n\\s\t\r &!%world")

            assert checksum_utils.blake2b_checksum_for_file(tmp.name) == self.HASH

    def test_lru_cache(self):
        with (
            tempfile.NamedTemporaryFile() as tmp,
            mock.patch(
                "checksum_utils.checksum_utils._checksum_for_file",
                wraps=checksum_utils._checksum_for_file,
            ) as mock_checksum_for_file,
        ):

            with open(tmp.name, mode="w") as fout:
                fout.write("hello \n\\s\t\r &!%world")

            assert (
                checksum_utils.blake2b_checksum_for_file(
                    tmp.name, do_use_lru_cache=False
                )
                == self.HASH
            )
            assert (
                checksum_utils.blake2b_checksum_for_file(
                    tmp.name, do_use_lru_cache=False
                )
                == self.HASH
            )
            assert mock_checksum_for_file.call_count == 2

            assert (
                checksum_utils.blake2b_checksum_for_file(
                    tmp.name, do_use_lru_cache=True
                )
                == self.HASH
            )
            assert (
                checksum_utils.blake2b_checksum_for_file(
                    tmp.name, do_use_lru_cache=True
                )
                == self.HASH
            )
            assert (
                checksum_utils.blake2b_checksum_for_file(
                    tmp.name, do_use_lru_cache=True
                )
                == self.HASH
            )
            assert (
                checksum_utils.blake2b_checksum_for_file(
                    tmp.name, do_use_lru_cache=True
                )
                == self.HASH
            )
            assert (
                checksum_utils.blake2b_checksum_for_file(
                    tmp.name, do_use_lru_cache=True
                )
                == self.HASH
            )
            assert mock_checksum_for_file.call_count == 3

            assert (
                checksum_utils.blake2b_checksum_for_file(
                    tmp.name, do_use_lru_cache=False
                )
                == self.HASH
            )
            assert mock_checksum_for_file.call_count == 4
