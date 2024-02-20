from os import makedirs
from os.path import basename, isfile, split

import boto3
from botocore.client import ClientError
from loguru import logger


class AwsOps:
    def __init__(
        self, access_key: str, secret_key: str, region: str, endpoint_url: str = None
    ):
        self.region = region
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=self.region,
            endpoint_url=endpoint_url if endpoint_url else None,
        )

    def _object_exists(self, bucket, key):
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=bucket, Prefix=key, MaxKeys=1
            )
            return (
                "Contents" in response
                and len(response["Contents"]) > 0
                and "Key" in response["Contents"][0]
                and response["Contents"][0]["Key"] == key
            )
        except Exception as exc:
            logger.exception(exc)
            return False

    def upload_s3(self, bucket: str, file, signature=None):
        assert isfile(file) is True, f"{file} not found"

        try:
            self.s3_client.head_bucket(Bucket=bucket)
        except ClientError as exc:
            if int(exc.response["Error"]["Code"]) == 404:
                logger.warning(f"does not exist, creating {bucket}")
                self.s3_client.create_bucket(
                    Bucket=bucket,
                    CreateBucketConfiguration={"LocationConstraint": self.region},
                )
            else:
                logger.exception(exc.response)

        logger.info(f"Uploading {file} to {bucket}; signature: {signature}")
        key = signature if signature else basename(file)
        self.s3_client.upload_file(Filename=file, Bucket=bucket, Key=key)

        assert self._object_exists(bucket, key) is True

    def download_s3(self, bucket, file, destination):
        if self._object_exists(bucket, file):
            logger.info(f"Downloading {file} from {bucket}; to {destination}")
            makedirs(split(destination)[0], exist_ok=True)
            self.s3_client.download_file(bucket, file, destination)
            # TODO: check downloaded
        else:
            logger.warning(f"{file} not found")
            raise Exception(f"{file} not found")
