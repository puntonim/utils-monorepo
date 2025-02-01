import json
from datetime import datetime

import pytest

import json_utils


class TestToJson:
    def test_happy_flow(self):
        data = {"date": datetime(2025, 1, 1)}
        with pytest.raises(TypeError):
            json.dumps(data)
        assert json_utils.to_json(data)


class TestCustomJsonEncoder:
    def test_happy_flow(self):
        data = {"date": datetime(2025, 1, 1)}
        with pytest.raises(TypeError):
            json.dumps(data)
        assert json.dumps(data, cls=json_utils.CustomJsonEncoder)
