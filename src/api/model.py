import datetime
import sys
from os import makedirs
from os.path import exists, join
from pathlib import Path

import joblib
from loguru import logger
from numpy import array, round

sys.path.insert(0, "..")

from ml_system.cloud_ops import AwsOps  # noqa E402
from ml_system.trainer import Trainer  # noqa E402
from utils.config import get_config  # noqa E402

BASE_DIR = Path(__file__).resolve(strict=True).parent
TODAY = datetime.date.today()
CONFIG = get_config()
AWS_CLIENT = AwsOps(CONFIG["aws"]["access_key"], CONFIG["aws"]["secret_key"])


def train():
    makedirs(join(str(BASE_DIR), "temp"), exist_ok=True)
    model_trainer = Trainer(
        join(BASE_DIR, "temp"),  # todo: ref
        CONFIG["training_data"]["git_repo_url"],
        CONFIG["training_data"]["training_season"],
        None,  # todo: ref
        CONFIG["env"]["ml_save_location"],
    )

    metadata = model_trainer.metadata_location
    model_files = model_trainer.model_location

    logger.info(f"model metadata: {metadata}")
    logger.info(f"model location: {model_files}")

    if CONFIG["mlops"]["upload_model_artifacts"] and model_trainer.upload:
        AWS_CLIENT.upload_s3(
            CONFIG["aws"]["ml_models_bucket"],
            model_files,
            CONFIG["mlops"]["upload_model_signature"] + ".joblib",
        )
        AWS_CLIENT.upload_s3(
            CONFIG["aws"]["ml_models_bucket"],
            metadata,
            CONFIG["mlops"]["upload_model_signature"] + ".json",
        )

    return model_files, metadata


def predict(input_data: list):
    # todo: check input type & shape matches model input
    if CONFIG["mlops"]["download_model_artifacts"]:
        AWS_CLIENT.download_s3(
            CONFIG["aws"]["ml_models_bucket"],
            f'{CONFIG["mlops"]["upload_model_signature"]}.joblib',
            join(
                CONFIG["env"]["ml_save_location"],
                f'{CONFIG["mlops"]["upload_model_signature"]}.joblib',
            ),
        )
        AWS_CLIENT.download_s3(
            CONFIG["aws"]["ml_models_bucket"],
            f'{CONFIG["mlops"]["upload_model_signature"]}.json',
            join(
                CONFIG["env"]["ml_save_location"],
                f'{CONFIG["mlops"]["upload_model_signature"]}.json',
            ),
        )

    logger.info(CONFIG["mlops"]["download_model_artifacts"])

    model_file = join(
        CONFIG["env"]["ml_save_location"],
        f'{CONFIG["mlops"]["upload_model_signature"]}.joblib',
    )

    model = (
        joblib.load(model_file) if exists(model_file) else FileNotFoundError(model_file)
    )

    return round(model.predict(array(input_data).reshape(1, -1)))  # todo: ref
