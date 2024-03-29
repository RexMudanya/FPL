import os

from git import Repo
from loguru import logger


class FPLData:
    def __init__(self, github: str, season, data_dir: str):
        assert github is not None, "url to vaastav/fpl_data"
        assert data_dir is not None, "set data destination"
        # todo: check if season is none apply default

        os.makedirs(data_dir, exist_ok=True)

        self.git_repo = github
        self.season = season
        self.data_dir = data_dir

        try:
            logger.info(f"Cloning {self.git_repo} at {self.data_dir}")
            self.repo_path = os.path.split(self._clone_repo())[0]
        except Exception as e:
            logger.warning(f"{e} \t repo at {self.data_dir}")
            self.repo_path = self.data_dir
            Repo(self.repo_path, search_parent_directories=True).remotes.origin.pull()

    def _clone_repo(self):  # pragma: no cover
        return Repo.clone_from(self.git_repo, self.data_dir).git_dir

    def latest_fpl_data(self, game_week=None):  # pragma: no cover
        gw = "gw" + str(game_week) if game_week else "merged_gw"
        return os.path.join(self.repo_path, f"data/{self.season}/gws/{gw}.csv")
