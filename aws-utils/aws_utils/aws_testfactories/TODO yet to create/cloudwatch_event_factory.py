class CloudWatchEventFactory:
    @staticmethod
    def make_for_scheduled_event():
        data = {
            "version": "0",
            "id": "a9e5bf35-6650-3a79-e6c0-d6b88ca83ddb",
            "detail-type": "Scheduled Event",
            "source": "aws.events",
            "account": "477353422995",
            "time": "2023-10-25T05:00:00Z",
            "region": "eu-south-1",
            "resources": [
                "arn:aws:events:eu-south-1:477353422995:rule/intrac-bot-production-EndpointDashbotEventsRuleSch-1JBBVYY0B5RK3"
            ],
            "detail": {},
        }
        return data
