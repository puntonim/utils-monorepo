"""
** AWS UTILS: AWS TEST FACTORIES FOR LAMBDA CONTEXT **
=======================================================

Test factory for AWS Lambda context.

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
            ApiGatewayV2EventToLambdaFactory.make_for_get_request(
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

from dataclasses import dataclass


class LambdaContextFactory:
    @staticmethod
    def make():
        @dataclass
        class LambdaContext:
            function_name: str = __name__
            memory_limit_in_mb: int = 128
            invoked_function_arn: str = (
                "arn:aws:lambda:eu-west-1:809313241:function:" + __name__
            )
            aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

        return LambdaContext()
