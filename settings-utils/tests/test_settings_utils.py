import os

import settings_utils


class TestGetStringFromEnv:
    def setup_method(self):
        self.env_var_name = "PYTEST_SETTINGS_UTILS"

    def teardown_method(self):
        if self.env_var_name in os.environ:
            del os.environ[self.env_var_name]

    def test_happy_flow(self):
        os.environ[self.env_var_name] = "1"

        assert settings_utils.get_string_from_env(self.env_var_name, "XXX") == "1"

    def test_not_found(self):
        assert settings_utils.get_string_from_env(self.env_var_name, "XXX") == "XXX"


class TestGetBoolFromEnv:
    def setup_method(self):
        self.env_var_name = "PYTEST_SETTINGS_UTILS"

    def teardown_method(self):
        if self.env_var_name in os.environ:
            del os.environ[self.env_var_name]

    def test_true(self):
        for val in ("true", "yes", "t", "y"):
            os.environ[self.env_var_name] = val

            assert settings_utils.get_bool_from_env(self.env_var_name, False) is True

    def test_false(self):
        for val in ("false", "no", "f", "n", "whatever"):
            os.environ[self.env_var_name] = val

            assert settings_utils.get_bool_from_env(self.env_var_name, None) is False

    def test_not_found(self):
        assert settings_utils.get_bool_from_env(self.env_var_name, False) is False
