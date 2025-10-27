from typing import Optional


class EventBridgeEventFactory:
    @staticmethod
    def make_scheduled_event(detail_type: Optional[str] = None) -> dict:
        detail_type = detail_type if detail_type is not None else "Scheduled Event"
        data = {
            "id": "cdc73f9d-aea9-11e3-9d5a-835b769c0d9c",
            "detail-type": detail_type,
            "source": "aws.events",
            "account": "123456789012",
            "time": "1970-01-01T00:00:00Z",
            "region": "us-east-1",
            "resources": "arn:aws:events:us-east-1:123456789012:rule/TestRule",
            "detail": {},
        }
        return data
