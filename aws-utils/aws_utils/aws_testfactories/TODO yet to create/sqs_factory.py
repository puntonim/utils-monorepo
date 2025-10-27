import boto3
from mundi.conf.config import settings


class SQSFactory:
    @staticmethod
    def create_queue():
        sqs_client = boto3.client("sqs", region_name="us-east-1")
        queue_url = sqs_client.create_queue(
            QueueName=settings.S3_BUCKET_SCANNER_SQS_QUEUE_NAME
        )["QueueUrl"]

        return boto3.resource("sqs").Queue(queue_url)
