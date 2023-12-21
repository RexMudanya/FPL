import datetime
import os.path
import sys
from pathlib import Path

import joblib
from loguru import logger
from numpy import array, round

sys.path.insert(0, "..")

from ml_system.trainer import Trainer
from utils.config import get_config

BASE_DIR = Path(__file__).resolve(strict=True).parent
TODAY = datetime.date.today()
CONFIG = get_config()


def train():
    os.makedirs(os.path.join(str(BASE_DIR), "temp"), exist_ok=True)
    model_trainer = Trainer(
        os.path.join(BASE_DIR, "temp"),  # todo: ref
        CONFIG["training_data"]["git_repo_url"],
        CONFIG["training_data"]["training_season"],
        None,  # todo: ref
        os.path.join(BASE_DIR, "models"),
    )

    metadata = model_trainer.metadata
    model_files = os.path.join(
        model_trainer.save_location,
        f"{model_trainer.model_name}_{model_trainer.date}.joblib",
    )
    logger.info(f"model metadata: {metadata}")
    logger.info(f"model location: {model_files}")
    return model_files, metadata


def predict(input: list):
    # todo: check input type & shape matches model input
    model_file = Path(BASE_DIR).joinpath(r"models/baseline.joblib")  # todo: ref

    model = (
        joblib.load(model_file)
        if model_file.exists()
        else FileNotFoundError(model_file)
    )

    return round(model.predict(array(input).reshape(1, -1)))  # todo: ref
