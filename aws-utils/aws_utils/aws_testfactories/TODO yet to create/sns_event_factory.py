import json
from enum import Enum, auto
from typing import Optional

from aws_lambda_powertools.utilities.data_classes import S3Event, SNSEvent
from aws_lambda_powertools.utilities.data_classes.s3_event import S3EventRecord
from aws_lambda_powertools.utilities.data_classes.sns_event import SNSEventRecord
from events.hdmap_services_events.hdmap_services_event_base import SERVICE_ID_MAP_RUNNER
from events.hdmap_services_events.hdmap_services_start_event import ServiceStartEvent
from events.hdmap_services_events.hdmap_services_stop_event import (
    SERVICE_FINAL_STATUS_FAILURE,
    ServiceStopEvent,
)
from mundi.conf import settings

from ..testutils.dataset_testutils import (
    make_random_drivelog_name,
    make_random_region_name,
    make_random_session_name,
)

# TODO BAS-2547 create a new lib test-factories and move this code there.

_DEFAULT_VALUE = "DEFAULT_VALUE"


class S3ObjectTypesForRecordFactoryEnum(Enum):
    GRAPH_DATA_METRICS = auto()
    GPKG_METRICS = auto()
    APPLOGS_METRICS = auto()
    TILES_METRICS = auto()
    PCD_METRICS = auto()
    ROAD_METRICS_METRICS = auto()
    ICP_MAP_V1_METRICS = auto()
    ICP_MAP_V2_METRICS = auto()
    BEV_METRICS = auto()
    UNRECOGNIZED = auto()
    NO_FILE = auto()


class S3ConfigurationIdEnum(Enum):
    DEFAULT = auto()


class S3EventFactory:
    def __init__(
        self,
        s3_object_type: Optional[
            S3ObjectTypesForRecordFactoryEnum
        ] = S3ObjectTypesForRecordFactoryEnum.GRAPH_DATA_METRICS,
        s3_configuration_id: Optional[
            S3ConfigurationIdEnum
        ] = S3ConfigurationIdEnum.DEFAULT,
        bucket_name: Optional[str] = None,
        region: Optional[str] = None,
        session: Optional[str] = None,
    ):
        self.configuration_id = s3_configuration_id
        self.region = region if region is not None else make_random_region_name()
        self.session = session if session is not None else make_random_session_name()

        self.bucket_name = (
            bucket_name
            if bucket_name is not None
            else settings.S3_BUCKET_NAME_BASEMAPDB
        )

        self.s3_object_type = s3_object_type
        if s3_object_type == S3ObjectTypesForRecordFactoryEnum.GRAPH_DATA_METRICS:
            self.key = (
                f"{self.region}/{self.session}/upload-graph-data-command-metrics.json"
            )
        elif s3_object_type == S3ObjectTypesForRecordFactoryEnum.GPKG_METRICS:
            self.key = f"{self.region}/{self.session}/resources/upload-gpkg-command-metrics.json"
        elif s3_object_type == S3ObjectTypesForRecordFactoryEnum.APPLOGS_METRICS:
            self.key = f"{self.region}/{self.session}/applogs/upload-applogs-command-metrics.json"
        elif s3_object_type == S3ObjectTypesForRecordFactoryEnum.TILES_METRICS:
            self.key = f"{self.region}/{self.session}/upload-tiles-command-metrics.json"
        elif s3_object_type == S3ObjectTypesForRecordFactoryEnum.PCD_METRICS:
            self.key = f"{self.region}/{self.session}/upload-commands-metrics/service-upload-command-PCD_TILES_UPLOAD-metrics.json"
        elif s3_object_type == S3ObjectTypesForRecordFactoryEnum.ROAD_METRICS_METRICS:
            self.key = f"{self.region}/{self.session}/upload-commands-metrics/service-upload-command-ROAD_METRICS_TILES_UPLOAD-metrics.json"
        elif s3_object_type == S3ObjectTypesForRecordFactoryEnum.ICP_MAP_V1_METRICS:
            self.key = f"{self.region}/{self.session}/icp-map/upload-icp-map-command-metrics.json"
        elif s3_object_type == S3ObjectTypesForRecordFactoryEnum.ICP_MAP_V2_METRICS:
            self.key = f"{self.region}/{self.session}/icp-map/v2/upload-icp-map-command-metrics.json"
        elif s3_object_type == S3ObjectTypesForRecordFactoryEnum.BEV_METRICS:
            self.key = f"{self.region}/{self.session}/upload-commands-metrics/service-upload-command-BEV_TILES_UPLOAD-metrics.json"
        elif s3_object_type == S3ObjectTypesForRecordFactoryEnum.UNRECOGNIZED:
            self.key = f"{self.region}/{self.session}"
        else:
            raise Exception("Unknown `s3_object_type`")

        if s3_configuration_id == S3ConfigurationIdEnum.DEFAULT:
            self.configuration_id = "InvokeLambdaOnNewObjects"

    def _make_s3_event_record(self):
        data = {
            "eventVersion": "2.1",
            "eventSource": "aws:s3",
            "awsRegion": "ap-southeast-1",
            "eventTime": "2020-11-19T02:41:48.587Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {"principalId": "AWS:AIDAW6JD3GCJUSNZNWXG3"},
            "requestParameters": {"sourceIPAddress": "58.96.230.81"},
            "responseElements": {
                "x-amz-request-id": "6B54BFEF00AE4278",
                "x-amz-id-2": "E5NOQuZrxxIuqItALrBYG4Qid39a3PhBtbbJErpKSE0TGwXIvjRbjgDSZPWnsS6RKVGFy8C6p6Ud1ZB7xCAcZ3G72k2jx/tj",
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": self.configuration_id,
                "bucket": {
                    "name": self.bucket_name,
                    "ownerIdentity": {"principalId": "A8ISZCP1PWC04"},
                    "arn": "arn:aws:s3:::s3-events-demo-paolo-test1",
                },
                "object": {
                    "key": self.key,
                    "size": 6,
                    "eTag": "4226bff064575be69d3a255842ab98f7",
                    "sequencer": "005FB5DB70285DC37F",
                },
            },
        }
        return S3EventRecord(data)

    def make(self):
        s3_event_record = self._make_s3_event_record()
        s3_event = S3Event({"Records": [s3_event_record._data]})
        return s3_event._data


class SNSEventWithS3EventFactory:
    def __init__(
        self,
        inner_s3_object_type: Optional[
            S3ObjectTypesForRecordFactoryEnum
        ] = S3ObjectTypesForRecordFactoryEnum.GRAPH_DATA_METRICS,
        inner_s3_configuration_id: Optional[
            S3ConfigurationIdEnum
        ] = S3ConfigurationIdEnum.DEFAULT,
        inner_bucket_name: Optional[str] = None,
        region: Optional[str] = None,
        session: Optional[str] = None,
    ):
        self.s3_event_factory = S3EventFactory(
            s3_object_type=inner_s3_object_type,
            s3_configuration_id=inner_s3_configuration_id,
            bucket_name=inner_bucket_name,
            region=region,
            session=session,
        )
        self.s3_event = self.s3_event_factory.make()

    @property
    def region(self):
        return self.s3_event_factory.region

    @property
    def session(self):
        return self.s3_event_factory.session

    @property
    def s3_object_key(self):
        return self.s3_event_factory.key

    def _make_sns_event_record(self):
        data = {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:289485838881:hdmap-services-events-production:8d659a7b-3015-43cf-9367-0e1ceca796a8",
            "Sns": {
                "Type": "Notification",
                "MessageId": "830aa9f2-c097-5b32-8edc-f0c13a8a95ce",
                "TopicArn": "arn:aws:sns:us-east-1:289485838881:hdmap-services-events-production",
                "Subject": "Amazon S3 Notification",
                "Message": json.dumps(self.s3_event),
                "Timestamp": "2021-06-04T09:52:29.907Z",
                "SignatureVersion": "1",
                "Signature": "iu/VHAn9TVRqUmGABfuQhzA/m/BqewrFPpQwX9OeslJZlDmy1sb6NCbegH+MR3k74iS9v+E8kWRDbtxgWl9sgH0GMzEjKuiDYr9Zn3sfbFu5T3r7qNjRQADe6vBn/8ArUx98C0WuEd0lSfnmjTsaW8SN5SM4ZzrVLHP5DEKQAKPNMLuNduNjyRQo4Lu8M0JWylZJcIIkIMspaYhz2gVrcuThLzRNukdYJ8l8MImx910YgU83gh3MPlX4BvUCzDWtgsF/JjxNjOLbOKDAcrmjhQCmJgf5Ec5Z4bgtZpK9KDzPf45/ZVOnDNNVtDvE2Es6+jxgGlQ1SB4Plw+H3ttwxw==",
                "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-010a507c1833636cd94bdb98bd93083a.pem",
                "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:289485838881:hdmap-services-events-production:8d659a7b-3015-43cf-9367-0e1ceca796a8",
                "MessageAttributes": {},
            },
        }
        return SNSEventRecord(data)

    def make(self):
        sns_event_record = self._make_sns_event_record()
        sns_event = SNSEvent({"Records": [sns_event_record._data]})
        return sns_event._data


class SnsEventWithHdmapServicesEventFactory:
    def __init__(
        self,
        region: Optional[str] = _DEFAULT_VALUE,
        session: Optional[str] = _DEFAULT_VALUE,
    ):
        self.region = region if region != _DEFAULT_VALUE else make_random_region_name()
        self.session = (
            session if session != _DEFAULT_VALUE else make_random_session_name()
        )
        self.service_start_event = None
        self.service_stop_event = None

    def _make_sns_service_event_record(self, event):
        data = {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:289485838881:hdmap-services-events-production:7b2ae548-0858-4ee6-9dd1-4fde5426d4bd",
            "Sns": {
                "Type": "Notification",
                "MessageId": "02b592f6-bb09-5b39-a9f7-c845f18e0c1c",
                "TopicArn": "arn:aws:sns:us-east-1:289485838881:hdmap-services-events-production",
                "Subject": None,
                # "Message": "{\"event_source\": \"MAP_RUNNER_JENKINS\", \"payload\": {\"drivelog\": \"2022.02.16.18.48.56-g1p-veh-2042\", \"service_progress_url\": \"http://www.google.com\", \"service_error_message\": \"Drivelog missing!\", \"dataset_region\": \"sg-one-north\", \"dataset_session\": \"2022-02-17_00-32-21-GMT\", \"service_final_status\": \"FAILURE\", \"is_test_data\": false, \"service_id\": \"MAP_RUNNER\"}, \"hdmap_slackbot\": {\"do_skip_notification\": null, \"extra_text\": null}, \"slack_message\": {\"channel\": null, \"text\": null}, \"force_skip_subscribed_services\": [\"*!\", \"MAP_RUNNER\", \"MAP_RASTERIZER\"], \"event_id\": \"SERVICE_STOP\"}",
                "Message": event.to_json(),
                "Timestamp": "2022-03-22T03:53:43.530Z",
                "SignatureVersion": "1",
                "Signature": "UOHU0T6hK2QXiJI6XaXPKT5bwXpowIxMNeT35P/PY6oWVQAACHA2TPIFqbUciNIT6C60BlHzGmn4vlLDC63c5I62RtEVzqtg7NVgIcDUuOGPHT0tE2bwVTY590EnhZAXBId4EO32rJKsVOG8AU9ozqBdtoM5pM6MzJsY6YLIXG7F/Hk7Z/jALcLxAYgkf7d1StXnlrn5bsLtfKXBt93BRx3tdckCQj2zi2KBJFgnuZ82QAygKz3j0J33w/Qc+T2CM84zx2xilzGcXIaneKWjg83W9JgdXlhmggCvCCBI28N+x7IDKJnoipF5VEE+aRTW0S5nXaz6QGvKK/2CsW7pcA==",
                "SigningCertUrl": "https://sns.uhttps://sns.us-east-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem",
                "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:289485838881:hdmap-services-events-production:7b2ae548-0858-4ee6-9dd1-4fde5426d4bd",
                "MessageAttributes": {
                    "content_type": {"Type": "String", "Value": "application/json"}
                },
            },
        }
        return SNSEventRecord(data)

    def make_service_start_event(self, **kwargs):
        params = dict(
            event_source="MAP_RUNNER_JENKINS",
            service_id=SERVICE_ID_MAP_RUNNER,
            service_progress_url="http://www.google.com",
            is_test_data=False,
            dataset_region=self.region,
            dataset_session=self.session,
            drivelog=make_random_drivelog_name(),
            slackbot_extra_text="Slackbot Extra Text",
            do_skip_slackbot_notification=False,
            slack_message_text="Custom Slack message text",
            slack_message_channel="test-slackbot-private",
            has_colored_point_cloud=None,
        )
        self.service_start_event = ServiceStartEvent(**dict(params, **kwargs))
        sns_event_record = self._make_sns_service_event_record(self.service_start_event)
        sns_event = SNSEvent({"Records": [sns_event_record._data]})
        return sns_event._data

    def make_service_stop_event(self, **kwargs):
        params = dict(
            event_source="MAP_RUNNER_JENKINS",
            force_skip_subscribed_services=["*"],
            service_id=SERVICE_ID_MAP_RUNNER,
            service_progress_url="http://www.google.com",
            service_final_status=SERVICE_FINAL_STATUS_FAILURE,
            service_error_message="Drivelog file missing: foo.bar",
            is_test_data=False,
            dataset_region=self.region,
            dataset_session=self.session,
            drivelog=make_random_drivelog_name(),
            slackbot_extra_text="Slackbot Extra Text",
            do_skip_slackbot_notification=False,
            slack_message_text="Custom Slack message text",
            slack_message_channel="test-slackbot-private",
            has_colored_point_cloud=None,
        )
        self.service_stop_event = ServiceStopEvent(**dict(params, **kwargs))
        sns_event_record = self._make_sns_service_event_record(self.service_stop_event)
        sns_event = SNSEvent({"Records": [sns_event_record._data]})
        return sns_event._data
