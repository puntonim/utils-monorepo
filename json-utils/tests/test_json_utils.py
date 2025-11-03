import json
from datetime import datetime

import pytest

import json_utils


class TestToJsonString:
    def test_happy_flow(self):
        data = {"date": datetime(2025, 1, 1)}
        with pytest.raises(TypeError):
            json.dumps(data)
        assert json_utils.to_json_string(data)


class TestPrettifyToNonJsonString:
    def test_happy_flow(self):
        data = {
            "id": "39296166250439623962212092407450232854575369122363277321",
            "timestamp": 1762101037459,
            "message": '[ERROR] UnhealthEndpointException\nTraceback (most recent call last):\n\u00a0\u00a0File "/opt/python/aws_lambda_powertools/logging/logger.py", line 548, in decorate\n\u00a0\u00a0\u00a0\u00a0return lambda_handler(event, context, *args, **kwargs)\n\u00a0\u00a0File "/var/task/botte_be/views/endpoint_introspection_view.py", line 170, in lambda_handler\n\u00a0\u00a0\u00a0\u00a0raise UnhealthEndpointException(ts=now)',
        }
        text = json_utils.to_json_string(data, indent=4)
        assert "\\n" in text
        print("\n" + text)

        text = json_utils.prettify_to_non_json_string(text)
        print("\n" + text)
        assert "\\n" not in text


class TestCustomJsonEncoder:
    def test_happy_flow(self):
        data = {"date": datetime(2025, 1, 1)}
        with pytest.raises(TypeError):
            json.dumps(data)
        assert json.dumps(data, cls=json_utils.CustomJsonEncoder)
