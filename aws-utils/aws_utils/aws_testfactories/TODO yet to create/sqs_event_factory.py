import json
from typing import Optional

from aws_lambda_powertools.utilities.data_classes import SQSEvent
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord
from mundi.domains.s3_bucket_scanner_domain import S3_DATASET_SCANNER_TASK_ID

from ..testutils.dataset_testutils import (
    make_random_region_name,
    make_random_session_name,
)


class SQSEventWithS3DatasetScannerTaskFactory:
    def __init__(
        self,
        region: Optional[str] = None,
        session: Optional[str] = None,
    ):
        self.region = region if region is not None else make_random_region_name()
        self.session = session if session is not None else make_random_session_name()

    def _make_sqs_record_s3_dataset_scanner_task(self):
        data = {
            "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
            "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
            "body": json.dumps(
                {
                    "task_id": S3_DATASET_SCANNER_TASK_ID,
                    "region": self.region,
                    "session": self.session,
                }
            ),
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1545082649183",
                "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                "ApproximateFirstReceiveTimestamp": "1545082649185",
            },
            "messageAttributes": {
                "content_type": {
                    "DataType": "String",
                    "StringValue": "application/json",
                }
            },
            "md5OfBody": "e4e68fb7bd0e697a0ae8f1bb342846b3",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-east-2:123456789012:my-queue",
            "awsRegion": "us-east-2",
        }
        return SQSRecord(data)

    def make_s3_dataset_scanner_task_event(self):
        sqs_record = self._make_sqs_record_s3_dataset_scanner_task()
        sqs_event = SQSEvent({"Records": [sqs_record._data]})
        return sqs_event._data
