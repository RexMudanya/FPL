import wandb


class Mlops:
    def __init__(self, project, entity, job, name) -> None:
        self.run = wandb.init(project=project, entity=entity, job_type=job, name=name)

    def log_dataset(self, data, name):
        self.run.job_type = "dataset"

        artifact = wandb.Artifact(name=name + f"_{self.run.id}", type="training data")
        artifact.add_file(data)
        self.run.log_artifact(artifact)

    def log_model(self, model, name):
        self.run.job_type = "save"

        artifact = wandb.Artifact(name=name + f"_{self.run.id}", type="model")
        artifact.add_file(model)
        self.run.log_artifact(artifact)

        self.run.link_artifact(artifact, "model-registry")

    def log_metrics(self, metrics):
        self.run.job_type = "evaluate"

        wandb.log({"metrics": metrics})
