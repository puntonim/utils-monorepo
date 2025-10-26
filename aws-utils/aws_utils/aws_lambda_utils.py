"""
** AWS UTILS: AWS LAMBDA UTILS **
=================================

Response util for AWS Lambda.

Note: there are more utils to copy from patatrack_utils in patatrack-monorepo.

```py
from aws_utils import aws_lambda_utils
import log_utils as logger
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEventV2
from aws_lambda_powertools.utilities.typing import LambdaContext

@aws_lambda_utils.redact_http_headers(headers_names=("authorization",))
@logger.get_adapter().inject_lambda_context(log_event=True)
def lambda_handler(event: dict[str, Any], context: LambdaContext) -> dict:
    api_event = APIGatewayProxyEventV2(event)
    activities = domain.list_activities(
            after_ts=after_ts,
            before_ts=before_ts,
        )
    except domain_exceptions.RequestedResultsPageDoesNotExistInStravaApi as exc:
        return aws_lambda_utils.BadRequest400Response(
            f"The requested page-n does not exist: page-n={exc.page_n}"
        ).to_dict()

    return aws_lambda_utils.Ok200Response(activities).to_dict()
```
"""

import importlib
from abc import ABC
from collections.abc import Callable, Sequence

import json_utils
import log_utils as logger

__all__ = [
    "BadRequest400Response",
    "Unauthorized401Response",
    "NotFound404Response",
    "InternalServerError500Response",
    "Ok200Response",
    "Created201Response",
    "redact_http_headers",
]


class BaseJsonResponse(ABC):
    STATUS_CODE = 200

    def __init__(
        self,
        body: str | dict | list | None = None,
        do_convert_to_json=True,
        status_code: int | None = None,
    ):
        self.body = body
        self.do_convert_to_json = do_convert_to_json
        self.status_code = status_code

    def to_dict(self) -> dict:
        status_code = self.status_code or self.STATUS_CODE
        response = dict()
        response["statusCode"] = status_code
        if self.body is not None:
            response["Content-Type"] = "application/json"
            response["body"] = (
                json_utils.to_json(self.body) if self.do_convert_to_json else self.body
            )

        # Log the response only if not a 2XX.
        extra = None
        if status_code > 299:
            extra = dict(response=response)

        # Log with error level or info level.
        if status_code > 499:
            logger.error(f"Responding {status_code}", extra=extra)
        else:
            logger.info(f"Responding {status_code}", extra=extra)
        return response


class BadRequest400Response(BaseJsonResponse):
    STATUS_CODE = 400


class Unauthorized401Response(BaseJsonResponse):
    STATUS_CODE = 401


class NotFound404Response(BaseJsonResponse):
    STATUS_CODE = 404


class InternalServerError500Response(BaseJsonResponse):
    STATUS_CODE = 500


class Ok200Response(BaseJsonResponse):
    STATUS_CODE = 200


class Created201Response(BaseJsonResponse):
    STATUS_CODE = 201


def __raise_fn(msg):
    raise Exception(msg)


redact_http_headers = lambda *args, **kwargs: __raise_fn(
    "The extra lib `aws_lambda_powertools` is required in order to use"
    " `redact_http_headers()`; you should:"
    " pip install aws-utils[lambda-redact-http-headers]"
)
_is_powertools_req_installed = False
try:
    _is_powertools_req_installed = importlib.import_module("aws_lambda_powertools")
except ImportError as exc:
    pass

if _is_powertools_req_installed:
    # Dynamically import requirements.
    lambda_handler_decorator = importlib.import_module(
        "aws_lambda_powertools.middleware_factory"
    ).lambda_handler_decorator
    LambdaContext = importlib.import_module(
        "aws_lambda_powertools.utilities.typing"
    ).LambdaContext

    @lambda_handler_decorator
    def _redact_http_headers(
        handler: Callable[[dict, LambdaContext], dict],
        event: dict,
        context: LambdaContext,
        headers_names: Sequence[str],
    ) -> dict:
        """
        Redact HTTP headers before they end up in CloudWatch logs.
        Typical usage: authorization header.

        Example:
            from aws_utils import aws_lambda_utils

            @aws_lambda_utils.redact_http_headers(headers_names=("authorization",))
            @logger.get_adapter().inject_lambda_context(log_event=True)
            def lambda_handler(event: dict[str, Any], context: LambdaContext) -> dict:
                ...
        """
        # Implemented with the Middleware Factory of AWS Lambda Powertools for Python:
        #  https://docs.aws.amazon.com/powertools/python/latest/utilities/middleware_factory

        ## Run code before the Lambda handler.
        ...

        if "headers" in event:
            for header_name in headers_names:
                # Search for the key, but case-insensitive.
                for k in event["headers"]:
                    if k.lower() == header_name.lower():
                        header_name = k
                        break

                logger.debug(f"Redacting header: {header_name}")
                value = event.get("headers", {}).get(header_name)
                if value is not None:
                    event["headers"][header_name] = value[:1] + "**REDACTED**"

        ## Run the Lambda handler.
        response = handler(event, context)

        ## Run code after the Lambda handler.
        ...

        return response

    redact_http_headers = _redact_http_headers
