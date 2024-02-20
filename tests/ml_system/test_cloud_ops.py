import subprocess
from os import makedirs, path, remove, rmdir

import pytest
from joblib import dump

from src.ml_system.cloud_ops import AwsOps


@pytest.mark.slow
def test_awsops():
    dir_ = path.dirname(path.abspath(__file__))

    subprocess.Popen(
        [
            "docker-compose",
            "-f",
            f"{path.join(dir_,'docker-compose.yaml')}",
            "up",
            "--build",
        ]
    )

    aws_client = AwsOps("test", "test", "us-east-1", "http://localhost:4566")

    bucket = "models"
    model_key = "model.joblib"
    assert aws_client._object_exists(bucket, model_key) is False

    # aws_client.s3_client.create_bucket(Bucket=bucket)

    model_path = path.join(dir_, model_key)
    with pytest.raises(AssertionError):
        aws_client.upload_s3(bucket, "xyz", model_path)

    dump(None, model_path)

    aws_client.upload_s3(bucket, model_path, model_path)
    # assert aws_client._object_exists(bucket, model_key) is True

    dir = path.join(dir_, bucket)
    makedirs(dir, exist_ok=True)
    with pytest.raises(Exception):
        aws_client.download_s3(bucket, "mdl.pth", dir)

    aws_client.download_s3(bucket, model_key, dir)

    remove(model_path)
    rmdir(dir)

    subprocess.Popen(
        ["docker-compose", "-f", f"{path.join(dir_,'docker-compose.yaml')}", "down"]
    )
