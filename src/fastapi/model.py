import datetime
from pathlib import Path

import joblib
from numpy import array, round

BASE_DIR = Path(__file__).resolve(strict=True).parent
TODAY = datetime.date.today()


def train():
    # todo: download historical data
    # todo: fit new model
    # todo: serialize and save model
    pass


def predict(input: list):
    # todo: check input type & shape matches model input
    model_file = Path(BASE_DIR).joinpath(r"models/baseline.joblib")  # todo: ref

    model = (
        joblib.load(model_file)
        if model_file.exists()
        else FileNotFoundError(model_file)
    )

    return round(model.predict(array(input).reshape(1, -1)))  # todo: ref
