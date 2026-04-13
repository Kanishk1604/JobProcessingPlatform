import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from app.core.config import get_settings

#s3/MiniIO client wrapper
#boto3 -> library that lets your python code talk to aws services through its APIs
#AWS -> exposes REST APIs
# => we need to create aws signs, contruct http req, handle retries, parse responses  
# so boto3 wraps all of above into functions
# in simple words, it is helpful for uploading and downlaoding files
class StorageService:
    def __init__(self) -> None:
        settings = get_settings()
        self.bucket_name = settings.s3_bucket_name
        self.client: BaseClient = boto3.client(
            "s3",
            endpoint_url = settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key_id,
            aws_secret_access_key = settings.s3_secret_access_key,
            region_name = settings.s3_region,
        )

    def ensure_bucket_exists(self) -> None:
        try:
            self.client.head_bucket(Bucket= self.bucket_name)
        except ClientError:
            self.client.create_bucket(Bucket=self.bucket_name)

    def upload_bytes(
        self,
        data: bytes,
        key: str,
        content_type: str,
    ) -> None:
        self.client.put_object(
            Bucket = self.bucket_name,
            Key=key,
            Body=data,
            ContentType= content_type,
        )

    def download_bytes(
        self,
        key: str,
    )-> bytes:
        response = self.client.get_object(
            Bucket= self.bucket_name,
            Key = key,
        )

        return response["Body"].read()
