# Note: in mundi there is also a factory for S3 events to SNS to Lambda.

__all__ = ["SnsEventToLambdaFactory"]


class SnsEventToLambdaFactory:
    @staticmethod
    def make_for_cloudwatch_log():
        data = "H4sIAAAAAAAA/+2W7WrkNhSGb8WI/khSO9aHJX9AobPZ2ZAlu4UkZQtxGDT2GY+JRnIlzUxmQ+5lr2WvrNhOQkJYaFP2T7sYbNk659UrnUdGt2gFzskGLnYdoAK9nVxMZh+m5+eT4ykKkdlqsKhASZoyzhJK85yjECnTHFuz7lCBYrl1sZKreS3jufEeojlEnTV1BLruTKt91Gpvjeug8q3RY/a5tyBXqEAUUx4TEmMWX/50OrmYnl9c0fmcLbisOUmzpF5UOa/FIscJJhXJ6qRCIXLruats2/WK71rlwTpUXCK5ddFW+mpZm2Y0caTMuh4+vZVuqUzTP8BaY13f8qa/Oz28bIe+lWxV39DGt4tT07jzF2MNop960VPTsGjyx9qdqvef34PE6GqY33QD2veWblFbowKxnOapIClnjCWYZikmTLCEEME4z3KWCMxwwtNU8JQmNKc4I5RzjELk2xU4L1cdKkgqKBGCEE4ZDx8qhwp0WyIFG1AlKkr0aXL28eTjcYnCEilTyd730BFvpI29dNdjoWZziDctbF38UKnZs0rN+s7DblcUY3lnS6lrBbYoiEgH9XsD46jS6lY3gTJNANrb3RDxaH6I6YsdERJhFhBcMF4QHlLGf8YY4yHcgd201Sj4pvcYvJkGvwYbcogPx4jKqHrmvLS+RIW3awhLtFjr0bCWqzH374A4yD2mrmBl7G7m2s+jAuXieYC04yJKqwu5dfdrUsA6cmbtlxEpnu6R4iGv+OdWLPy5BudnbT0MWCVECgoiYnkmowQSEeWAaZQscMUySHIs5SBwY+Vu5q2s4CGVRCLHWcYFjWheJWm6kGSBszoHIubpPFtAVqK7UqO78N9xSl7D6fTs7Lez70pp9oLSab/zfzD6f2SUvobRo7OTi5Ojyel3xTR/gemRbX1bSfWD1P8MqYLyLE15ljEqEpGnOWZJngtMacYxw1zgJKEizWku8m+TKp6Sejn8Qa+C3/USpPLL6f1yTG8qGE4rpb7oJzCX1XWwtzLOBxYq0D6opFKBks7vF6X++uXrl3etgqBEsel83O380uj+XDe7Z7UzW7DeGOViZZqm1c3wBHvY9WAGqtUQ8CQLg1YHNVTGSg+jcH9Z8Gurg+fg70F/RAqDymgPNz4MDqRtXBgcHFxv+9b+c2Ov222P5kiKB3PPPTyxKFsH317IPe9+0Wa7j+6u7v4CmTu5fjILAAA="
        # data is base64 and gzip encoded and it can be decoded with:
        #   import zlib
        #   import base64
        #   zlib.decompress(base64.b64decode(data), zlib.MAX_WBITS | 32).decode()
        # Or with Lambda Powertools:
        #   cloudwatch_event = CloudWatchLogsEvent(data)
        #   text = cloudwatch_event.decompress_logs_data.decode()
        # It decodes to:
        # {
        #     "messageType": "DATA_MESSAGE",
        #     "owner": "477353422995",
        #     "logGroup": "/aws/lambda/botte-be-prod-endpoint-introspection",
        #     "logStream": "2025/11/03/[$LATEST]2bb3f5ad51784dfc95d6f90401c18d4c",
        #     "subscriptionFilters": [
        #         "aws-watchdog-prod-CloudwatchDashlogDasherrorsDashtoDashsnsDashwDashemailDashnotifLogsSubscriptionFilterCloudWatchLog3-AXusLlJzJea0"
        #     ],
        #     "logEvents": [
        #         {
        #             "id": "39297617533340287013634116355893460304577657242920812550",
        #             "timestamp": 1762166115235,
        #             "message": {
        #                 "level": "WARNING",
        #                 "location": "/var/task/botte_be/views/endpoint_introspection_view.py::lambda_handler::167",
        #                 "message": "Warning log entry",
        #                 "timestamp": "2025-11-03 10:35:15,235+0000",
        #                 "service": "Botte BE @ v1.0.0",
        #                 "cold_start": true,
        #                 "function_name": "botte-be-prod-endpoint-introspection",
        #                 "function_memory_size": "256",
        #                 "function_arn": "arn:aws:lambda:eu-south-1:477353422995:function:botte-be-prod-endpoint-introspection",
        #                 "function_request_id": "c41a62e6-398a-4e46-9e02-4f0c38e490aa",
        #                 "xray_trace_id": "1-69088562-29c477fa1f08d9e16b7b8fe8"
        #             }
        #         },
        #         {
        #             "id": "39297617533340287013634116355893460304577657242920812551",
        #             "timestamp": 1762166115235,
        #             "message": {
        #                 "level": "ERROR",
        #                 "location": "/var/task/botte_be/views/endpoint_introspection_view.py::lambda_handler::168",
        #                 "message": "Error log entry",
        #                 "timestamp": "2025-11-03 10:35:15,235+0000",
        #                 "service": "Botte BE @ v1.0.0",
        #                 "cold_start": true,
        #                 "function_name": "botte-be-prod-endpoint-introspection",
        #                 "function_memory_size": "256",
        #                 "function_arn": "arn:aws:lambda:eu-south-1:477353422995:function:botte-be-prod-endpoint-introspection",
        #                 "function_request_id": "c41a62e6-398a-4e46-9e02-4f0c38e490aa",
        #                 "xray_trace_id": "1-69088562-29c477fa1f08d9e16b7b8fe8"
        #             }
        #         },
        #         {
        #             "id": "39297617533340287013634116355893460304577657242920812552",
        #             "timestamp": 1762166115235,
        #             "message": {
        #                 "level": "CRITICAL",
        #                 "location": "/var/task/botte_be/views/endpoint_introspection_view.py::lambda_handler::169",
        #                 "message": "Critical log entry",
        #                 "timestamp": "2025-11-03 10:35:15,235+0000",
        #                 "service": "Botte BE @ v1.0.0",
        #                 "cold_start": true,
        #                 "function_name": "botte-be-prod-endpoint-introspection",
        #                 "function_memory_size": "256",
        #                 "function_arn": "arn:aws:lambda:eu-south-1:477353422995:function:botte-be-prod-endpoint-introspection",
        #                 "function_request_id": "c41a62e6-398a-4e46-9e02-4f0c38e490aa",
        #                 "xray_trace_id": "1-69088562-29c477fa1f08d9e16b7b8fe8"
        #             }
        #         },
        #         {
        #             "id": "39297617533362587758832646979034996022850305604426792969",
        #             "timestamp": 1762166115236,
        #             "message": "[ERROR] UnhealthEndpointException
        # Traceback (most recent call last):
        #   File "/opt/python/aws_lambda_powertools/logging/logger.py", line 548, in decorate
        #     return lambda_handler(event, context, *args, **kwargs)
        #   File "/var/task/botte_be/views/endpoint_introspection_view.py", line 170, in lambda_handler
        #     raise UnhealthEndpointException(ts=now)"
        #         }
        #     ]
        # }

        event = {"awslogs": {"data": data}}
        return event
