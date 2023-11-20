import datetime
import logging
import os.path
import sys
from pathlib import Path

sys.path.insert(0, "..")

import joblib
from numpy import array, round

from ml_system.trainer import Trainer

BASE_DIR = Path(__file__).resolve(strict=True).parent
TODAY = datetime.date.today()


def train():
    os.makedirs(os.path.join(str(BASE_DIR), "temp"), exist_ok=True)
    model_trainer = Trainer(
        os.path.join(BASE_DIR, "temp"),  # todo: ref
        "https://github.com/vaastav/Fantasy-Premier-League.git",  # todo: impl env file
        "2023-24",  # todo: ref, impl
        None,  # todo: ref
        os.path.join(BASE_DIR, "models"),
    )

    metadata = model_trainer.metadata
    model_files = model_trainer.save_location
    logging.info(f"model metadata: {metadata}")
    logging.info(f"model location: {model_files}")
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
