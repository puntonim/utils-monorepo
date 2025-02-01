class BaseGetFqnException(Exception):
    pass


class NotSupported(BaseGetFqnException):
    pass


def get_fqn(fn):
    """
    Get the fully qualified name of a function, method or class.
    Docs: https://www.python.org/dev/peps/pep-3155/
    """
    if not hasattr(fn, "__module__") or not hasattr(fn, "__qualname__"):
        raise NotSupported("Only works with functions, methods and classes")
    return f"{fn.__module__}::{fn.__qualname__}"
