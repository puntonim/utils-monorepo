__all__ = ["EventbridgeSchedulerEventToLambdaFactory"]


class EventbridgeSchedulerEventToLambdaFactory:
    @staticmethod
    def make_for_scheduled_event():
        data = {
            "version": "0",
            "id": "bc6910d7-184e-4cd8-b68b-9e4088ca5558",
            "detail-type": "Scheduled Event",
            "source": "aws.scheduler",
            "account": "477353422995",
            "time": "2025-11-09T18:02:00Z",
            "region": "eu-south-1",
            "resources": [
                "arn:aws:scheduler:eu-south-1:477353422995:schedule/default/reborn-automator-prod-CronDashbookDashpowerDashcla-BRZOO817TRP0"
            ],
            "detail": "{}",
        }
        return data
