from os import makedirs
from os.path import basename, exists, split

import boto3
from botocore.client import ClientError
from loguru import logger


class AwsOps:
    def __init__(self, access_key: str, secret_key: str):
        self.s3_client = boto3.client(
            "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
        )

    def _object_exists(self, bucket, key):
        response = self.s3_client.list_objects_v2(Bucket=bucket, Prefix=key, MaxKeys=1)
        return (
            "Contents" in response
            and len(response["Contents"]) > 0
            and "Key" in response["Contents"][0]
            and response["Contents"][0]["Key"] == key
        )

    def upload_s3(self, bucket: str, file, signature=None):
        assert exists(file), f"{file} not found"

        try:
            self.s3_client.head_bucket(Bucket=bucket)
        except ClientError as exc:
            if int(exc.response["Error"]["Code"]) == 404:
                logger.warning(f"does not exist, creating {bucket}")
                self.s3_client.create_bucket(Bucket=bucket)
            else:
                logger.exception(exc.response)

        logger.info(f"Uploading {file} to {bucket}; signature: {signature}")
        self.s3_client.upload_file(
            Filename=file, Bucket=bucket, Key=signature if signature else basename(file)
        )

    def download_s3(self, bucket, file, destination):
        if self._object_exists(bucket, file):
            logger.info(f"Downloading {file} from {bucket}; to {destination}")
            makedirs(split(destination)[0], exist_ok=True)
            self.s3_client.download_file(bucket, file, destination)
        else:
            logger.warning(f"{file} not found")
            raise Exception(f"{file} not found")
