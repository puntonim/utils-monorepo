"""
** AWS UTILS: AWS LAMBDA UTILS **
=================================

Response util for AWS Lambda.

Note: there are more utils to copy from patatrack_utils in patatrack-monorepo.

```py
from aws_utils.aws_lambda_utils import BadRequest400Response, Ok200Response

def lambda_handler(event: dict[str, Any], context) -> dict:

    activities = domain.list_activities(
            after_ts=after_ts,
            before_ts=before_ts,
        )
    except domain_exceptions.RequestedResultsPageDoesNotExistInStravaApi as exc:
        return BadRequest400Response(
            f"The requested page-n does not exist: page-n={exc.page_n}"
        ).to_dict()

    return Ok200Response(activities).to_dict()
```
"""

from abc import ABC

import json_utils
import log_utils as logger


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
