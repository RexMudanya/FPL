# rfr baseline model trainer
import json
from datetime import datetime

import joblib
from data_download import FPLData
from preprocessing import Preprocess, split_data
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


class Predictor:
    def __init__(
        self, X, y, X_test, y_test, save_location=None, model_name=None
    ):  # todo: kwargs for model constructor
        self.X, self.y = X, y
        self.X_test, self.y_test = X_test, y_test
        self.save_location = save_location

        if model_name is None:
            self.model_name = "fpl_regressor"
        else:
            self.model_name = model_name

        self.regressor = RandomForestRegressor(
            n_estimators=100, verbose=0, criterion="squared_error"
        )

        self.latest_GW = None  # todo: set from data preprocessing
        self.metadata: dict

        self.date = str(datetime.now().isoformat())

        self.train()
        if save_location:
            self.save_model()
        self.save_metadata()

    def train(self):
        self.regressor.fit(self.X, self.y)

    def score(self):
        return self.regressor.score(self.X_test, self.y_test)

    def mae(self):
        prediction = self.regressor.predict(self.X_test)
        return mean_absolute_error(self.y_test, prediction)

    def save_model(self):
        joblib.dump(
            self.regressor, f"{self.save_location}/{self.model_name}_{self.date}.joblib"
        )

    def save_metadata(self):
        self.metadata = {
            "model_name": self.model_name,
            "latest_GW": self.latest_GW,
            "rscore": round(self.score(), 4),
            "mae": round(self.mae(), 4),
            "date": self.date,
        }  # todo: ref with wandb

        if self.save_location:
            with open(
                f"{self.save_location}/{self.model_name}_{self.date}.json", "w"
            ) as f:  # todo: ref with wandb
                json.dump(self.metadata, f)


class Trainer(FPLData, Preprocess, Predictor):
    def __init__(
        self, data_dir: str, github: str, season: int, game_week: int, save_dir: str
    ):
        FPLData.__init__(self, github, season, data_dir)
        Preprocess.__init__(self, self.latest_fpl_data(game_week))

        self.X_train, self.X_test, self.y_train, self.y_test = split_data(
            self.X, self.y
        )
        self.save_dir = save_dir
        Predictor.__init__(
            self, self.X_train, self.X_test, self.y_train, self.y_test, self.save_dir
        )
