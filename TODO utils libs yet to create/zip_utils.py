import zlib


def zip_text(text: str) -> bytes:
    return zlib.compress(text.encode())


def unzip_text(text: bytes) -> str:
    return zlib.decompress(text).decode()
