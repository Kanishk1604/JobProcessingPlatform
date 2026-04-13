import boto3

from botocore.client import BaseClient

from app.core.config import get_settings

class StorageService:
    def __init__(self) -> None:
        settings = get_settings()
        self.bucket_name = settings.s3_bucket_name
        self.client: BaseClient = boto3.client(
            "s3",
            endpoint_url = settings.s3_endpoint_url,
            aws_access_key_id = settings.s3_access_key_id,
            aws_secret_access_key = settings.s3_secret_access_key,
            region_name = settings.s3_region,
        )

    def download_bytes(self, key: str) -> bytes:
        response = self.client.get_object(
            Bucket = self.bucket_name,
            Key = key,
        )
        return response["Body"].read()

    def upload_bytes(
        self,
        data: bytes,
        key: str,
        content_type: str
    ):
        self.client.put_object(
            Bucket= self.bucket_name,
            Key=key,
            Body=data,
            ContentType = content_type,
        )
