"""
Note: if settings are managed with Dynaconf, then see `hdmap-web/odd-manager`.
"""

from contextlib import ContextDecorator


class override_settings(ContextDecorator):
    """
    Context manager and decorator to override single keys in `conf.settings`.
    Only already existing keys can be overridden; non-existing keys are discarded.

    As a context manager:
        from ..conf import settings
        with override_settings(settings, APP_NAME="XXX")
            assert settings.APP_NAME == "XXX"

    As decorator, you can decorate a test function or method like:
        from ..conf import settings
        @override_settings(settings, APP_NAME="XXX")
        def test_happy_flow(...):
            assert settings.APP_NAME == "XXX"

    But you can NOT decorate a (test) class. To use it for the entire test class:
        from ..conf import settings
        class TestMyTest:
            def setup(self):
                self.override_settings = override_settings(settings, APP_NAME="XXX")
                self.override_settings.__enter__()

            def teardown(self):
                self.override_settings.__exit__()
    """

    def __init__(self, settings, **kwargs):
        self.settings = settings
        self.kwargs = kwargs
        self.orig_values = dict()

    def __enter__(self):
        for key, value in self.kwargs.items():
            # Only update existing keys; discard non-existing keys.
            if not hasattr(self.settings, key):
                continue
            self.orig_values[key] = getattr(self.settings, key)
            setattr(self.settings, key, value)
        return self

    def __exit__(self, *exc):
        for key, value in self.orig_values.items():
            setattr(self.settings, key, value)
        return False
