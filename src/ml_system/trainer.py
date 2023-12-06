# rfr baseline model trainer
import json
import os.path
import sys
from datetime import datetime

sys.path.insert(0, "..")

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from ml_system.data_download import FPLData
from ml_system.mlops import MlflowOps
from ml_system.preprocessing import Preprocess, split_data

config = {
    "MLFLOW_TRACKING_URI": "sqlite:///mlflow.db",
    "ENTITY": "dev",
    "NAME": "test",
    "ARTIFACT_PATH": "",
}  # todo: setup in env


class Predictor:
    def __init__(
        self, X_train, y_train, X_test, y_test, save_location=None, model_name=None
    ):  # todo: kwargs for model constructor
        assert len(X_train) == len(
            y_train
        ), f"X: {len(X_train)} not equal to y: {len(y_train)}"
        self.X_train, self.y_train = X_train, y_train
        self.X_test, self.y_test = X_test, y_test
        self.save_location = save_location

        if model_name is None:
            self.model_name = "fpl_regressor"
        else:
            self.model_name = model_name

        self.mlops = MlflowOps(
            self.model_name + "_experiment", config  # TODO: read from toml/ env
        )

        self.regressor = RandomForestRegressor(
            n_estimators=100, verbose=0, criterion="squared_error"
        )  # TODO: add input as params

        self.latest_GW = None  # todo: set from data preprocessing
        self.metadata: dict

        self.date = str(datetime.now()).replace(":", ".")

        self.train()
        self.prediction = self.regressor.predict(self.X_test)

        try:
            self.mlops.log_training(
                ((self.X_train, self.y_train), (self.X_test, self.y_test)),
                None,  # TODO: feed model_params
                {"rscore": round(self.score(), 4), "mae": round(self.mae(), 4)},
                (self.model_name, self.regressor),
            )
        except Exception as e:
            print(e)

        if save_location:
            self.save_model()
        self.save_metadata()

    def train(self):
        self.regressor.fit(self.X_train, self.y_train)

    def score(self):
        return self.regressor.score(self.X_test, self.y_test)

    def mae(self):
        return mean_absolute_error(self.y_test, self.prediction)

    def save_model(self):
        joblib.dump(
            self.regressor,
            os.path.join(self.save_location, f"{self.model_name}_{self.date}.joblib"),
        )

    def save_metadata(self):
        self.metadata = {
            "model_name": self.model_name,
            "latest_GW": self.latest_GW,
            "rscore": round(self.score(), 4),
            "mae": round(self.mae(), 4),
            "date": self.date,
        }

        if self.save_location:
            with open(
                f"{self.save_location}/{self.model_name}_{self.date}.json", "w"
            ) as f:
                json.dump(self.metadata, f)


class Trainer(FPLData, Preprocess, Predictor):
    def __init__(self, data_dir: str, github: str, season, game_week, save_dir: str):
        FPLData.__init__(self, github, season, data_dir)
        Preprocess.__init__(self, self.latest_fpl_data(game_week))

        X_train, X_test, y_train, y_test = split_data(self.X, self.y)
        self.save_dir = save_dir
        Predictor.__init__(self, X_train, y_train, X_test, y_test, self.save_dir)
