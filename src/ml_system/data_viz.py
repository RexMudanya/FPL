import pandas as pd
from loguru import logger

from ml_system.data_download import FPLData


class FPLDataStats(FPLData):
    def __init__(self, github, season, data_dir) -> None:
        FPLData.__init__(self, github, season, data_dir)

        self.data = pd.read_csv(self.latest_fpl_data(None))

        self.data["points_per_90"] = self.data["total_points"] / self.data["minutes"]
        self.data["points_per_90"] = self.data["points_per_90"].fillna(0)

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

    def get_points_per_gw_board(self, game_week=None):
        game_week = game_week if game_week else self.data["GW"].unique()[-1].item()
        return (
            self.data.loc[self.data["GW"] == game_week]
            .sort_values(by="total_points", ascending=False)
            .reset_index(drop=True)[  # TODO: include xp?
                [
                    "name",
                    "position",
                    "team",
                    "selected",
                    "minutes",
                    "GW",
                    "total_points",
                ]
            ]
            .to_dict(orient="records")
        )

    def get_points90_ownership_board(self, game_week=None):
        game_week = game_week if game_week else self.data["GW"].unique()[-1].item()
        return (
            self.data.loc[self.data["GW"] == game_week]
            .sort_values(by="points_per_90", ascending=False)
            .reset_index(drop=True)[
                [
                    "name",
                    "position",
                    "team",
                    "selected",
                    "minutes",
                    "GW",
                    "total_points",
                ]
            ]
            .to_dict(orient="records")
        )

    def get_form_vs_season_average(self):
        pass  # TODO: Impl

    def get_xg_xa(self, game_week=None):
        game_week = game_week if game_week else self.data["GW"].unique()[-1].item()
        return (
            self.data.loc[self.data["GW"] == game_week]
            .sort_values(
                by=["expected_goals", "expected_assists"], ascending=[False, False]
            )
            .reset_index(drop=True)[
                [
                    "name",
                    "position",
                    "team",
                    "GW",
                    "minutes",
                    "expected_goals",
                    "expected_assists",
                    "goals_scored",
                    "assists",
                ]
            ]
            .to_dict(orient="records")
        )

    def get_clean_sheet_vs_fdr(self):
        pass  # TODO: Impl

    def get_player_points_per_gw(self, player_name: str):
        # TODO: check if None insert top player by points
        return (
            self.data.loc[self.data["name"] == player_name]
            .sort_values(by="GW", ascending=True)
            .reset_index(drop=True)[["GW", "total_points"]]
            .to_dict(orient="records")
        )

    def get_player_points_90_ownership(self, player_name: str):
        # TODO: if player is None use top player
        player_name = (
            player_name if player_name else self.data["name"].unique()[0].item()
        )
        return (
            self.data.loc[self.data["name"] == player_name]
            .sort_values(by="GW", ascending=True)
            .reset_index(drop=True)[["GW", "points_per_90", "selected"]]
            .to_dict(orient="records")
        )

    def get_player_form_vs_season_average(self):
        pass  # TODO: Impl

    def get_player_xg_xa(self, player_name=None):
        return (
            self.data.loc[self.data["name"] == player_name]
            .sort_values(by="GW", ascending=True)
            .reset_index(drop=True)[["GW", "expected_goals", "expected_assists"]]
            .to_dict(orient="records")
        )

    def get_player_clean_sheet_vs_fdr(self):
        pass  # TODO: Impl
