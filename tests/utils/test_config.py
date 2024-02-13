import pytest

from src.utils.config import get_config


def test_get_config():
    assert isinstance(get_config(), dict)

    with pytest.raises(FileNotFoundError):
        get_config("config.toml")

    with pytest.raises(KeyError):
        from pathlib import Path

        get_config(Path(__file__).with_name("bad.toml"))
