from os import makedirs
from os.path import basename, exists, split

import boto3
from loguru import logger


class AwsOps:
    def __init__(self, access_key: str, secret_key: str):
        self.s3_client = boto3.client(
            "s3", aws_access_key_id=access_key, aws_secret_access_key=secret_key
        )
        # TODO: create bucket

    def upload_s3(self, bucket: str, file, signature=None):
        assert exists(file), f"{file} not found"
        logger.info(f"Uploading {file} to {bucket}; signature: {signature}")
        self.s3_client.upload_file(
            Filename=file, Bucket=bucket, Key=signature if signature else basename(file)
        )  # todo: check for success

    def download_s3(self, bucket, file, destination):
        logger.info(f"Downloading {file} from {bucket}; to {destination}")
        makedirs(split(destination)[0], exist_ok=True)
        self.s3_client.download_file(bucket, file, destination)
