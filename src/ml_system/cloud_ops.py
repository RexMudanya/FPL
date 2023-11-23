from os.path import exists, basename
import boto3


class AwsOps:
    def __init__(self, access_key: str, secret_key: str):
        self.session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.s3 = self.session.resource('s3')

    def upload_s3(self, bucket: str, file, key=None):
        assert exists(file), f'{file} not found'
        self.s3.meta.client.upload_file(
            Filename=file,
            Bucket=bucket,
            key=key if key else basename(file)
        )  # todo: check for success
