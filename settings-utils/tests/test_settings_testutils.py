import pytest

from settings_utils.settings_testutils import override_settings


class settings:
    """
    Usage:
        from conf import settings
        print(setting.APP_NAME)
    """

    APP_NAME = "App name"
    IS_TEST = False
    FOO = "bar"


class TestSettings:
    def test_happy_flow(self):
        assert settings.APP_NAME == "App name"
        assert settings.FOO == "bar"

    def test_key_does_not_exist(self):
        with pytest.raises(AttributeError):
            settings.XXX

    def test_override_settings(self):
        assert settings.APP_NAME == "App name"
        assert settings.FOO == "bar"

        @override_settings(settings, APP_NAME="XXX", FOO="baz")
        def assert_overridden():
            assert settings.APP_NAME == "XXX"
            assert settings.FOO == "baz"

        assert_overridden()

        assert settings.APP_NAME == "App name"
        assert settings.FOO == "bar"

        with override_settings(settings, APP_NAME="XXX", FOO="baz"):
            assert settings.APP_NAME == "XXX"
            assert settings.FOO == "baz"

        assert settings.APP_NAME == "App name"
        assert settings.FOO == "bar"

    def test_override_settings_key_does_not_exist(self):
        @override_settings(settings, XXX="XXX", FOO="baz")
        def assert_overridden():
            with pytest.raises(AttributeError):
                settings.XXX

        assert_overridden()
