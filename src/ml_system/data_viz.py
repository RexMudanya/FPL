import pandas as pd
from loguru import logger

from ml_system.data_download import FPLData


class FPLDataStats(FPLData):
    def __init__(self, github, season, data_dir) -> None:
        FPLData.__init__(self, github, season, data_dir)

        self.data = pd.read_csv(self.latest_fpl_data(None))

    def _filter(self, column: str):
        filtered = {}
        for position in self.data["position"].unique():
            filtered[position] = (
                self.data.loc[self.data["position"] == position][column].sum().item()
            )
        logger.info(filtered)

        return filtered

    def goal_distribution(self):
        return self._filter("goals_scored")

    def assist_distribution(self):
        return self._filter("assists")

    def clean_sheet_table(self, top: int = 5):
        return dict(
            self.data.loc[self.data["position"] == "GK"]
            .sort_values(by=["clean_sheets"], ascending=False)[["name", "clean_sheets"]]
            .head(top)
            .values
        )
