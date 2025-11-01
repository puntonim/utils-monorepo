import boto3

REGION_NAME_N_VIRGINIA = "us-east-1"
REGION_NAME_SINGAPORE = "ap-southeast-1"
REGION_NAME_MILAN = "eu-south-1"
REGION_NAME_DEFAULT = REGION_NAME_MILAN


class SnsFactory:
    @staticmethod
    def create_topic(topic_name: str, region_name: str | None = None) -> str:
        if not region_name:
            region = REGION_NAME_DEFAULT
        client = boto3.client("sns", region_name=region_name)
        response = client.create_topic(Name=topic_name)
        topic_arn = response["TopicArn"]
        return topic_arn
