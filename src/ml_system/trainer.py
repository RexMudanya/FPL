# rfr baseline model trianer
import json
from datetime import datetime

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


class Predictor:
    def __init__(self, model_name=None):  # todo: kwargs for model constructor
        if model_name is None:
            self.model_name = "fpl_regressor"
        else:
            self.model_name = model_name

        self.regressor = RandomForestRegressor(
            n_estimators=100, verbose=0, criterion="squared_error"
        )

        
        self.latest_GW: int  # todo: set from data preprocessing
        self.metadata: dict

        self.date = str(datetime.now().isoformat())

    def train(self, X, y):
        self.regressor.fit(X, y)

    def score(self, X_test, y_test):
        return self.regressor.score(X_test, y_test)

    def mae(self, X_test, y_test):
        prediction = self.regressor.predict(X_test)
        return mean_absolute_error(y_test, prediction)

    def save_model(self, save_location, model_name):
        self.model_name = model_name
        joblib.dump(self.regressor, f"{save_location}/{model_name}_{self.date}.joblib")

    def save_metadata(self, X_test, y_test, save_location):
        self.metadata = {
            "model_name": self.model_name,
            "latest_GW": self.latest_GW,
            "rscore": round(self.score(X_test, y_test), 4),
            "mae": round(self.mae(X_test, y_test), 4),
            "date": self.date,
        }

        with open(f"{save_location}/{self.model_name}_{self.date}.json", "w") as f:
            json.dump(self.metadata, f)
