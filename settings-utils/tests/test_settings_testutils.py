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


class TestSettingsAsClass:
    """
    Test the case when the `settings` class is used without instantiating it.
    """

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


class TestSettingsAsInstance:
    """
    Test the case when the `settings` class is used as instance (not as a class).
    This is useful when we want to add attributes that are methods with @property.

    Example:
        class _Settings:
            APP_NAME = "Botte BE"
            IS_TEST = False

            @property
            def TELEGRAM_TOKEN(self):
                return settings_utils.get_string_from_env_or_aws_parameter_store(
                    env_key="TELEGRAM_TOKEN",
                    parameter_store_key_path="/botte-be/prod/telegram-token",
                    default="XXX",
                )

        class _TestSettings:
            IS_TEST = True

        settings = _Settings()
    """

    def setup_method(self):
        self.s = settings()

    def test_happy_flow(self):
        assert self.s.APP_NAME == "App name"
        assert self.s.FOO == "bar"

    def test_key_does_not_exist(self):
        with pytest.raises(AttributeError):
            self.s.XXX

    def test_override_settings(self):
        assert self.s.APP_NAME == "App name"
        assert self.s.FOO == "bar"

        @override_settings(self.s, APP_NAME="XXX", FOO="baz")
        def assert_overridden():
            assert self.s.APP_NAME == "XXX"
            assert self.s.FOO == "baz"

        assert_overridden()

        assert self.s.APP_NAME == "App name"
        assert self.s.FOO == "bar"

        with override_settings(self.s, APP_NAME="XXX", FOO="baz"):
            assert self.s.APP_NAME == "XXX"
            assert self.s.FOO == "baz"

        assert self.s.APP_NAME == "App name"
        assert self.s.FOO == "bar"

    def test_override_settings_key_does_not_exist(self):
        @override_settings(self.s, XXX="XXX", FOO="baz")
        def assert_overridden():
            with pytest.raises(AttributeError):
                self.s.XXX

        assert_overridden()
