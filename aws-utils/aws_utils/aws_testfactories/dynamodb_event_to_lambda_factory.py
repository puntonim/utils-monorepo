from uuid import uuid4

__all__ = ["DynamodbEventToLambdaFactory"]


class _DEFAULT_VALUE: ...


class DynamodbEventToLambdaFactory:
    @staticmethod
    def make_for_insert(
        keys: dict = _DEFAULT_VALUE,
        new_image: dict | None = _DEFAULT_VALUE,
    ):
        if keys is _DEFAULT_VALUE:
            # keys = {
            #         "TaskId": {"S": "BOTTE_MESSAGE"},
            #         "Text": {
            #             "S": "2023-10-29T13:22:56.252653+00:00#Hello world!!",
            #         },
            # }
            keys = {
                "PK": {"S": "BOTTE_MESSAGE"},
                # It should be KsuidMs but that requires a new requirement which I
                #  don't want here because this test lib should have few dependencies.
                "SK": {"S": str(uuid4())},
            }
        if new_image is _DEFAULT_VALUE:
            new_image = {
                **keys,
                "TaskId": {"S": "BOTTE_MESSAGE"},
                "SenderApp": {"S": "AWS_UTILS"},
                "Payload": {
                    "M": {
                        "text": {
                            "S": "Hello World from (utils-monorepo) aws-utils pytests!"
                        },
                    }
                },
                "ExpirationTs": {"N": 1698672903},
            }
        data = {
            "eventID": "ff29711457aeb0372bc2a89d8edd7098",
            "eventName": "INSERT",
            "eventVersion": "1.1",
            "eventSource": "aws:dynamodb",
            "awsRegion": "eu-south-1",
            "dynamodb": {
                "ApproximateCreationDateTime": 1698673253,
                "Keys": keys,
                "NewImage": new_image,
                "SequenceNumber": "45400000000013380201987",
                "SizeBytes": 180,
                "StreamViewType": "NEW_IMAGE",
            },
            "eventSourceARN": "arn:aws:dynamodb:eu-south-1:477353422995:table/patatrack-botte-message-db-queue-production/stream/2023-10-30T13:38:23.986",
        }
        event = {"Records": [data]}
        return event
