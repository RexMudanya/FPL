from os import makedirs, path, remove, rmdir, system

from joblib import dump

from src.ml_system.cloud_ops import AwsOps


def test_awsops():
    dir_ = path.dirname(path.abspath(__file__))

    system(f"docker-compose -f {path.join(dir_,'docker-compose.yaml')} up --build")

    aws_client = AwsOps("test", "test")
    aws_client.s3_client.endpoint_url = "http://localhost:4566"

    bucket = "models"
    aws_client.s3_client.create_bucket(Bucket=bucket)

    model_path = path.join(dir_, "model.joblib")
    dump(None, model_path)
    aws_client.upload_s3(bucket, model_path, model_path)

    dir = path.join(dir_, "models")
    makedirs(dir, exist_ok=True)
    aws_client.download_s3(bucket, "model.joblib", dir)

    remove(model_path)
    rmdir(dir)

    system(f"docker-compose -f {path.join(dir_,'docker-compose.yaml')} down")
