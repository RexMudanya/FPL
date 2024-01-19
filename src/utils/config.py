from os import path

import toml
from loguru import logger


def get_config(config_path=None):
    config_path = (
        path.dirname(__file__) + "/../config.toml" if not config_path else config_path
    )

    if not path.exists(config_path):
        logger.error(f"{config_path} not found, create file from config_example.toml")
        raise FileNotFoundError()

    config = toml.load(config_path)
    if config.keys() != {"aws", "training_data", "mlops", "env", "api"}:
        logger.error(f"{config_path} missing keys, check config_example")
        raise KeyError(f"{config_path} missing keys, check config_example")

    return config
