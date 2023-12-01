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

        self.RUN_INFO = None
        self.registered_model_name = None

    def log_training(
        self, data: tuple[str, str], params: dict, metrics: dict, model: tuple[str, any]
    ):
        with mlflow.start_run(nested=True) as run:
            self.RUN_INFO = dict(run.info)

            self.registered_model_name = (
                f'{self.experiment_name}_{self.RUN_INFO["run_id"]}_{model[0]}'
            )

            mlflow.log_param("train-data", data[0])
            mlflow.log_param("validation-data", data[1])

            mlflow.log_params(params)

            mlflow.log_metrics(metrics)

            mlflow.sklearn.log_model(
                model[1],
                model[0],
                artifact_path=self.config["ARTIFACT_PATH"],
                registered_model_name=self.registered_model_name,
            )

            self._change_model_stage(
                self.registered_model_name,
                mlflow.MlflowClient()
                .get_latest_versions(self.registered_model_name, stages=["None"])[0]
                .version,
                "Staging",
            )

            if self._check_best_run() == self.RUN_INFO["run_id"]:
                for models in mlflow.search_model_versions():
                    if models.current_stage == "Production":
                        self._change_model_stage(
                            models.name, models.version, "Archived"
                        )

                self._change_model_stage(
                    self.registered_model_name,
                    mlflow.MlflowClient()
                    .get_latest_versions(
                        self.registered_model_name, stages=["Staging"]
                    )[0]
                    .version,
                    "Production",
                )
                # TODO: upload to cloud
            else:
                self._change_model_stage(
                    self.registered_model_name,
                    mlflow.MlflowClient()
                    .get_latest_versions(
                        self.registered_model_name, stages=["Staging"]
                    )[0]
                    .version,
                    "Archived",
                )

                mlflow.MlflowClient().delete_registered_model(
                    name=self.registered_model_name
                )

        mlflow.end_run()

    def _check_best_run(self):
        current_experiment = dict(mlflow.get_experiment_by_name(self.experiment_name))
        run_data = mlflow.search_runs(
            [current_experiment["experiment_id"]], order_by=["metrics.mse DESC"]
        )  # TODO: ref metric to use

        return run_data.loc[0, "run_id"]

    def _change_model_stage(self, model_name: str, version: int, stage: str):
        mlflow.MlflowClient().transition_model_version_stage(model_name, version, stage)
