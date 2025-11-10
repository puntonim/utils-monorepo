"""
** AWS UTILS: AWS TEST FACTORIES FOR AWS API GATEWAY EVENTS TO LAMBDA **
========================================================================

Test factory for AWS API Gateway version 2 events sent to Lambda.

Note: there are more utils to copy from patatrack_utils in patatrack-monorepo.

```py
from aws_utils.aws_testfactories.api_gateway_event_to_lambda_factory import ApiGatewayV2EventToLambdaFactory
from aws_utils.aws_testfactories.lambda_context_factory import LambdaContextFactory

class TestEndpointListActivitiesView:
    def setup_method(self):
        self.context = LambdaContextFactory().make()

    def test_happy_flow(self):
        after_ts = 1759424400
        response = lambda_handler(
            ApiGatewayEventToLambdaFactory.make_for_get_request(
                path="/activity",
                raw_query_string=f"after-ts={after_ts}&n-results-per-page=1",
            ),
            self.context,
        )
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body[0]["id"] == 16013371380
        assert body[0]["name"] == "Weight training: powerlifting"
```
"""

import json_utils

__all__ = ["ApiGatewayV2EventToLambdaFactory"]


class ApiGatewayV2EventToLambdaFactory:
    @staticmethod
    def make_for_get_request(
        path: str = "/health",
        raw_query_string: str | None = None,
    ):
        data = {
            "version": "2.0",
            "routeKey": f"GET {path}",
            "rawPath": path,
            "rawQueryString": "",
            "headers": {
                "accept": "*/*",
                "content-length": "0",
                "host": "bgszvfrn3l.execute-api.eu-south-1.amazonaws.com",
                "user-agent": "curl/8.1.2",
                "x-amzn-trace-id": "Root=1-65382160-7f8841e036763ad34d1952b1",
                "x-forwarded-for": "31.188.7.85",
                "x-forwarded-port": "443",
                "x-forwarded-proto": "https",
            },
            "requestContext": {
                "accountId": "477353422995",
                "apiId": "bgszvfrn3l",
                "domainName": "bgszvfrn3l.execute-api.eu-south-1.amazonaws.com",
                "domainPrefix": "bgszvfrn3l",
                "http": {
                    "method": "GET",
                    "path": path,
                    "protocol": "HTTP/1.1",
                    "sourceIp": "31.188.7.85",
                    "userAgent": "curl/8.1.2",
                },
                "requestId": "NUonIjbbMu8EP5g=",
                "routeKey": f"GET {path}",
                "stage": "$default",
                "time": "24/Oct/2023:19:56:16 +0000",
                "timeEpoch": 1698177376516,
            },
            "isBase64Encoded": False,
        }
        if raw_query_string:
            data["rawQueryString"] = raw_query_string
            qs_dict = {}
            for qs in raw_query_string.split("&"):
                key, val = qs.split("=")
                if key in qs_dict:
                    qs_dict[key] += f",{val}"
                else:
                    qs_dict[key] = val
            data["queryStringParameters"] = qs_dict
        return data

    @staticmethod
    def make_for_post_request(
        path: str = "/health",
        body_dict: dict | None = None,
        body_json: str | None = None,
        path_parameters_dict: dict | None = None,
        headers: dict | None = None,
    ):
        data = {
            "version": "2.0",
            "routeKey": f"POST {path}",
            "rawPath": path,
            "rawQueryString": None,
            "headers": {
                "accept": "*/*",
                "content-length": "0",
                "host": "bgszvfrn3l.execute-api.eu-south-1.amazonaws.com",
                "user-agent": "curl/8.1.2",
                "x-amzn-trace-id": "Root=1-6537f02b-26b365f302da43b8640c8b41",
                "x-forwarded-for": "31.188.7.85",
                "x-forwarded-port": "443",
                "x-forwarded-proto": "https",
            },
            "requestContext": {
                "accountId": "477353422995",
                "apiId": "bgszvfrn3l",
                "domainName": "bgszvfrn3l.execute-api.eu-south-1.amazonaws.com",
                "domainPrefix": "bgszvfrn3l",
                "http": {
                    "method": "POST",
                    "path": path,
                    "protocol": "HTTP/1.1",
                    "sourceIp": "31.188.7.85",
                    "userAgent": "curl/8.1.2",
                },
                "requestId": "NUJ2zjrfMu8EJdw=",
                "routeKey": f"POST {path}",
                "stage": "$default",
                "time": "24/Oct/2023:16:26:19 +0000",
                "timeEpoch": 1698164779210,
            },
            "isBase64Encoded": False,
        }
        body = None
        if body_dict is not None:
            body = json_utils.to_json_string(body_dict)
        elif body_json is not None:
            body = body_json
        if body is not None:
            data["body"] = body
        if path_parameters_dict:
            data["pathParameters"] = {
                "proxy": "/path/to/resource",
                **path_parameters_dict,
            }
        if headers:
            data["headers"].update(headers)
        return data

    @staticmethod
    def make_for_delete_request(
        path: str = "/health",
        path_parameters_dict: dict | None = None,
    ):
        data = {
            "version": "2.0",
            "routeKey": f"DELETE {path}",
            "rawPath": path,
            "rawQueryString": None,
            "headers": {
                "accept": "*/*",
                "content-length": "0",
                "host": "bgszvfrn3l.execute-api.eu-south-1.amazonaws.com",
                "user-agent": "curl/8.1.2",
                "x-amzn-trace-id": "Root=1-6537f02b-26b365f302da43b8640c8b41",
                "x-forwarded-for": "31.188.7.85",
                "x-forwarded-port": "443",
                "x-forwarded-proto": "https",
            },
            "requestContext": {
                "accountId": "477353422995",
                "apiId": "bgszvfrn3l",
                "domainName": "bgszvfrn3l.execute-api.eu-south-1.amazonaws.com",
                "domainPrefix": "bgszvfrn3l",
                "http": {
                    "method": "DELETE",
                    "path": path,
                    "protocol": "HTTP/1.1",
                    "sourceIp": "31.188.7.85",
                    "userAgent": "curl/8.1.2",
                },
                "requestId": "NUJ2zjrfMu8EJdw=",
                "routeKey": f"DELETE {path}",
                "stage": "$default",
                "time": "24/Oct/2023:16:26:19 +0000",
                "timeEpoch": 1698164779210,
            },
            "isBase64Encoded": False,
        }
        if path_parameters_dict:
            data["pathParameters"] = {
                "proxy": "/path/to/resource",
                **path_parameters_dict,
            }
        return data
