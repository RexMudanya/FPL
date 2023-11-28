import mlflow

config = {
    "MLFLOW_TRACKING_URI": "sqlite:///mlflow.db",
    "ENTITY": "",
    "NAME": "",
    "ARTIFACT_PATH": "",
}  # todo: setup in env


class MlflowOps:
    def __int__(
        self, experiment: str, config: dict = config
    ):  # todo: setup config dict
        assert config is not None, "provide config"
        assert experiment is not None, "provide experiment name"

        self.config = config
        self.experiment_name = experiment

        mlflow.set_tracking_uri(self.config["MLFLOW_TRACKING_URI"])
        mlflow.set_experiment(self.experiment_name)
        mlflow.set_tag(config["entity"], config["name"])

    def log_training(
        self, data: tuple[str, str], params: dict, metrics: dict, model: tuple[str, any]
    ):
        with mlflow.start_run():
            mlflow.log_param("train-data", data[0])
            mlflow.log_param("validation-data", data[1])
            [mlflow.log_param(k, v) for k, v in params.items() if params]
            [mlflow.log_metrics(k, v) for k, v in metrics.items() if metrics]
            mlflow.sklearn.log_model(
                model[1], model[0], artifact_path=self.config["ARTIFACT_PATH"]
            )

        mlflow.end_run()
