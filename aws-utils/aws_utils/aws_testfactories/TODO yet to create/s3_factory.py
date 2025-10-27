import json
from typing import Dict, Optional

import boto3
from mundi.conf import settings
from mundi.utils.boto3_utils import get_s3_resource
from mypy_boto3_s3.service_resource import Object

from ..testutils.dataset_testutils import (
    make_random_region_name,
    make_random_session_name,
)

# TODO BAS-2510 BAS-2547 create a new lib test-factories and move this code there.
#  But use the S3Factory in map-cli because it has more features.
#  Also make sure the methods have names like Update_* rather than create_*.
#  And use s3_client lib extracted from map-cli instead of boto3 directly.


class S3Factory:
    """
    Test factory that mimics the S3 files and dirs uploaded by map-cli to the S3 buckets.
    """

    def __init__(
        self,
        region: Optional[str] = None,
        session: Optional[str] = None,
        drivelog: Optional[str] = None,
        do_create_all: bool = False,
        do_create_metadata_json: bool = False,
        do_create_upload_graph_data_metrics_json: bool = False,
        do_create_graph_data: bool = False,
        do_create_gpkg: bool = False,
        do_create_icp_map_v1: bool = False,
        do_create_icp_map_v2: bool = False,
        do_create_non_color_tiles: bool = False,
        do_create_color_tiles: bool = False,
        do_create_pcd: bool = False,
        do_create_road_metrics: bool = False,
        do_create_bev: bool = False,
    ):
        self.s3_resource = get_s3_resource()
        self.region = region if region is not None else make_random_region_name()
        self.session = session if session is not None else make_random_session_name()
        self.metadata_json: Optional[Object] = None

        if do_create_all:
            self._create_s3_metadata_json(drive_session=drivelog)
            self._create_s3_upload_graph_data_metrics_json()
            self._create_s3_graph_data()
            self._create_s3_gpkg()
            self._create_s3_icp_map_v1()
            self._create_s3_icp_map_v2()
            self._create_s3_non_color_tiles()
            self._create_s3_color_tiles()
            self._create_s3_pcd()
            self._create_s3_road_metrics()
            self._create_s3_bev()
        else:
            if do_create_metadata_json:
                self._create_s3_metadata_json()
            if do_create_upload_graph_data_metrics_json:
                self._create_s3_upload_graph_data_metrics_json()
            if do_create_graph_data:
                self._create_s3_graph_data()
            if do_create_gpkg:
                self._create_s3_gpkg()
            if do_create_icp_map_v1:
                self._create_s3_icp_map_v1()
            if do_create_icp_map_v2:
                self._create_s3_icp_map_v2()
            if do_create_non_color_tiles:
                self._create_s3_non_color_tiles()
            if do_create_color_tiles:
                self._create_s3_color_tiles()
            if do_create_pcd:
                self._create_s3_pcd()
            if do_create_road_metrics:
                self._create_s3_road_metrics()
            if do_create_bev:
                self._create_s3_bev()

    @staticmethod
    def create_s3_buckets():
        # Load S3 resource from boto3 directly (instead of using the global var
        # singleton in utils.boto3_utils) so this code can be used in conftest.py
        # with moto mocking S3.
        s3_resource = boto3.resource("s3")
        s3_resource.create_bucket(Bucket=settings.S3_BUCKET_NAME_BASEMAPDB)
        s3_resource.create_bucket(Bucket=settings.S3_BUCKET_NAME_BASEMAPTILES)
        return s3_resource

    def _create_s3_metadata_json(
        self, content: Dict = None, raw_content: str = None, drive_session: str = None
    ) -> None:
        # TODO BAS-2510 use s3_client lib extracted from map-cli instead. Same for the other methods.
        self.metadata_json = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPDB,
            f"{self.region}/{self.session}/metadata.json",
        )
        if raw_content is not None:
            self.metadata_json.put(Body=raw_content)
            return
        if not content:
            content = {
                "app_version": "a236620c",
                "drive_session": "MERGE",
                "map_files": {
                    "cloud_0.sqlite3": "edc783ce66e8cab2744c88ad04626b5e",
                    "graph.sqlite3": "b777112b19749e1e324df0f9b805aa09",
                },
                "odometer_distance": 10.1,
                "operation_type": "MERGE",
                "region": self.region,
                "session": self.session,
                "session_hierarchy": [
                    {"region": self.region, "session": "2022-01-26_03-51-25-GMT"},
                    {"region": self.region, "session": "2022-03-14_10-21-50-GMT"},
                ],
            }
        if drive_session:
            content["drive_session"] = drive_session
        self.metadata_json.put(Body=json.dumps(content, indent=4))

    def _create_s3_upload_graph_data_metrics_json(self) -> None:
        obj = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPDB,
            f"{self.region}/{self.session}/upload-graph-data-command-metrics.json",
        )
        content = {
            "start_ts": "2022-04-28T02:28:06.593079+00:00",
            "exc_info": "placeholder",
            "end_ts": "2022-04-28T02:28:17.247231+00:00",
            "duration_msec": 10654,
            "duration_min": 0.2,
            "uploaded_files_and_sizes_mb": {
                f"s3://{settings.S3_BUCKET_NAME_BASEMAPDB}/{self.region}/{self.session}/metadata.json": 0.000336,
                f"s3://{settings.S3_BUCKET_NAME_BASEMAPDB}/{self.region}/{self.session}/graph.sqlite3": 586.9,
                f"s3://{settings.S3_BUCKET_NAME_BASEMAPDB}/{self.region}/{self.session}/cloud_0.sqlite3": 586.9,
            },
            "uploaded_files_tot_number": 3,
            "uploaded_files_tot_size_gb": 1.2,
            "platform": "Linux-5.4.149-73.259.amzn2.x86_64-x86_64-with-Ubuntu-18.04-bionic",
            "platform_version": "#1 SMP Mon Sep 27 12:48:12 UTC 2021",
            "is_docker": True,
            "login_name": "uid=1000",
            "python_version": "3.6.9 (default, Mar 15 2022, 13:55:28) \n[GCC 8.4.0]",
            "hostname": "hdmap-services-540040da-292e-4941-bc50-0425317c8f54-m81dx-cg619",
            "ip": "172.26.135.175",
            "map_cli_version": "11.5.0",
            "sys_argv": [
                "/usr/local/bin/map-cli",
                "basemap2",
                "upload-graph-data",
                "--overwrite-remote-files",
                "--dir",
                f"./data/{self.region}-{self.session}",
                "-v",
            ],
            "sso_sub": "98jyE0Z0BM6FsPC64jV7jg51oWAWU00Z@clients",
            "auth_flow": "client-credentials",
            "sso_email": "john.doe@motional.com",
            "sso_name": "John Doe",
        }
        obj.put(Body=json.dumps(content, indent=4))

    def _create_s3_graph_data(self) -> None:
        pose_graph = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPDB,
            f"{self.region}/{self.session}/graph.sqlite3",
        )
        point_cloud = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPDB,
            f"{self.region}/{self.session}/cloud_0.sqlite3",
        )
        pose_graph.put(Body=".")
        point_cloud.put(Body=".")

    def _create_s3_gpkg(self) -> None:
        # TODO BAS-2510 use s3_client lib extracted from map-cli instead.
        gpkg = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPDB,
            f"{self.region}/{self.session}/resources/{self.region}-{self.session}-basemap.gpkg",
        )
        gpkg.put(Body=".")

    def _create_s3_icp_map_v1(self) -> None:
        s3 = boto3.resource("s3")
        icp_map_v1 = s3.Object(
            settings.S3_BUCKET_NAME_BASEMAPDB,
            f"{self.region}/{self.session}/icp-map/icp.dat",
        )
        icp_map_v1.put(Body=".")

    def _create_s3_icp_map_v2(self) -> None:
        icp_map_v2 = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPDB,
            f"{self.region}/{self.session}/icp-map/v2/icp.dat",
        )
        mini_icp_map_v2 = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPDB,
            f"{self.region}/{self.session}/icp-map/v2/icp-mini.dat",
        )
        icp_map_v2.put(Body=".")
        mini_icp_map_v2.put(Body=".")

    def _create_s3_non_color_tiles(self) -> None:
        intensity_tile_0 = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPTILES,
            f"basemaplive/{self.region}/{self.session}/intensity/0/0/0.png",
        )
        vertical_tile_0 = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPTILES,
            f"basemaplive/{self.region}/{self.session}/vertical/0/0/0.png",
        )
        intensity_tile_0.put(Body=".")
        vertical_tile_0.put(Body=".")

    def _create_s3_color_tiles(self) -> None:
        color_tile_0 = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPTILES,
            f"basemaplive/{self.region}/{self.session}/color/0/0/0.png",
        )
        color_tile_0.put(Body=".")

    def _create_s3_pcd(self) -> None:
        tiles_metadata_json = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPTILES,
            f"basemaplive/{self.region}/{self.session}/pcd/tiles-metadata.json",
        )
        tiles_metadata_json.put(Body=".")

    def _create_s3_road_metrics(self) -> None:
        road_metrics_tile_0 = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPTILES,
            f"basemaplive/{self.region}/{self.session}/roadthickness/0/0/0.png",
        )
        road_metrics_tile_0.put(Body=".")

    def _create_s3_bev(self) -> None:
        bev_tile_0 = self.s3_resource.Object(
            settings.S3_BUCKET_NAME_BASEMAPTILES,
            f"basemaplive/{self.region}/{self.session}/bev/0/0/0.png",
        )
        bev_tile_0.put(Body=".")
