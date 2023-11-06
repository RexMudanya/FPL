import logging
import os

from git import Repo


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
            self.repo_path = os.path.split(self._clone_repo())[0]
        except Exception as e:
            logging.info(f"{e} \t repo at {self.data_dir}")
            self.repo_path = self.data_dir
            Repo(self.repo_path).remotes.origin.pull()

    def _clone_repo(self):
        return Repo.clone_from(self.git_repo, self.data_dir).git_dir

    def latest_fpl_data(self, game_week: int = None):
        gw = "gw" + str(game_week) if game_week else "merged_gw"
        return os.path.join(self.repo_path, f"{self.season}/gws/{gw}.csv")
