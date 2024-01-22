from os import makedirs
from os.path import basename, exists, split

import boto3
from loguru import logger


class AwsOps:
    def __init__(self, access_key: str, secret_key: str):
        self.session = boto3.Session(
            aws_access_key_id=access_key, aws_secret_access_key=secret_key
        )
        self.s3 = self.session.resource("s3")
        self.s3_client = boto3.client(
            "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
        )

    def upload_s3(self, bucket: str, file, signature=None):  # pragma: no cover
        assert exists(file), f"{file} not found"
        logger.info(f"Uploading {file} to {bucket}; signature: {signature}")
        self.s3.meta.client.upload_file(
            Filename=file, Bucket=bucket, Key=signature if signature else basename(file)
        )  # todo: check for success
        # TODO: ref to client

    def download_s3(self, bucket, file, destination):  # pragma: no cover
        logger.info(f"Downloading {file} from {bucket}; to {destination}")
        makedirs(split(destination)[0], exist_ok=True)
        self.s3_client.download_file(bucket, file, destination)
        # TODO: test, ref
