# rfr baseline model trainer
import json
import sys
from datetime import datetime
from os.path import join

import joblib
from loguru import logger
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from ml_system.data_download import FPLData
from ml_system.mlops import MlflowOps
from ml_system.preprocessing import Preprocess, split_data
from utils.config import get_config

sys.path.insert(0, "..")

CONFIG = get_config()


class Predictor:
    def __init__(
        self,
        X_train,
        y_train,
        X_test,
        y_test,
        latest_gw,
        save_location=None,
        model_name=None,
    ):  # todo: kwargs for model constructor
        assert len(X_train) == len(
            y_train
        ), f"X: {len(X_train)} not equal to y: {len(y_train)}"
        logger.info("Training process started")

        self.X_train, self.y_train = X_train, y_train
        self.X_test, self.y_test = X_test, y_test
        self.save_location = save_location

        if model_name is None:
            self.model_name = "fpl_regressor"
        else:
            self.model_name = model_name

        self.mlops = MlflowOps(
            self.model_name + "_experiment",
            CONFIG["mlops"],
        )

        self.regressor = RandomForestRegressor(
            n_estimators=100, verbose=0, criterion="squared_error"
        )  # TODO: add input as params

        self.latest_GW = latest_gw  # todo: set from data preprocessing
        self.metadata = None

        self.date = str(datetime.now()).replace(":", ".")

        self.train()
        self.prediction = self.regressor.predict(self.X_test)

        try:
            self.mlops.log_training(
                ((self.X_train, self.y_train), (self.X_test, self.y_test)),
                {
                    "n_estimators": 100,
                    "criterion": "squared_error",
                },  # TODO: feed model_params
                {"rscore": round(self.score(), 4), "mae": round(self.mae(), 4)},
                (self.model_name, self.regressor),
            )
        except Exception as e:
            logger.exception(f"{e}: experiment logging ignored")

        self.upload = self.mlops.best_model

        self.model_location = None
        self.metadata_location = None

        if save_location and self.upload:
            self.save_model()
            self.save_metadata()

    def train(self):
        self.regressor.fit(self.X_train.values, self.y_train.values)

    def score(self):
        return self.regressor.score(self.X_test, self.y_test)

    def mae(self):
        return mean_absolute_error(self.y_test, self.prediction)

    def save_model(self):
        self.model_location = join(self.save_location, f"{self.model_name}.joblib")
        joblib.dump(
            self.regressor,
            self.model_location,
        )
        logger.success(f"Model {self.model_name} saved at: {self.save_location}")

    def save_metadata(self):
        self.metadata = {
            "model_name": self.model_name,
            "latest_GW": self.latest_GW,
            "rscore": round(self.score(), 4),
            "mae": round(self.mae(), 4),
            "date": self.date,
        }
        logger.info(f"Model metadata: {self.metadata}")

        self.metadata_location = join(self.save_location, f"{self.model_name}.json")

        if self.save_location:
            with open(self.metadata_location, "w") as f:
                json.dump(self.metadata, f)
            logger.success(f"{self.model_name} metadata saved at: {self.save_location}")


class Trainer(FPLData, Preprocess, Predictor):
    def __init__(self, data_dir: str, github: str, season, game_week, save_dir: str):
        FPLData.__init__(self, github, season, data_dir)
        Preprocess.__init__(self, self.latest_fpl_data(game_week))

        X_train, X_test, y_train, y_test = split_data(self.X, self.y)
        self.save_dir = save_dir
        Predictor.__init__(
            self, X_train, y_train, X_test, y_test, game_week, self.save_dir
        )
