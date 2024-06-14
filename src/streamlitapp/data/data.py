import json

import requests
from loguru import logger


class Data:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_points_prediction(self, predictors: list):
        try:
            response = requests.post(
                self.api_url + "predict",
                data=json.dumps({"input": predictors}),
                timeout=5,
            )
            response.raise_for_status()
            return json.loads(response.content.decode("utf-8"))
        except Exception as exc:
            logger.error(exc)
            return exc

    def get_game_week_points(self, game_week: int):
        try:
            response = requests.post(
                self.api_url + "game_week_points",
                data=json.dumps({"game_week": game_week}),
                timeout=5,
            )
            response.raise_for_status()
            return json.loads(response.content.decode("utf-8"))
        except Exception as exc:
            logger.error(exc)
            return exc

    def get_player_points_per_game_week(self, player_name: str):
        try:
            response = requests.post(
                self.api_url + "player_points_per_gw",
                data=json.dumps({"player_name": player_name}),
                timeout=5,
            )
            response.raise_for_status()
            return json.loads(response.content.decode("utf-8"))
        except Exception as exc:
            logger.error(exc)
            return exc

    def get_game_week_points_ownership(self, game_week: int):
        try:
            response = requests.post(
                self.api_url + "point_ownership",
                data=json.dumps({"game_week": game_week}),
                timeout=5,
            )
            response.raise_for_status()
            return json.loads(response.content.decode("utf-8"))
        except Exception as exc:
            logger.error(exc)
            return exc

    def get_player_90_points_ownership(self, player_name: str):
        try:
            response = requests.post(
                self.api_url + "points_90_ownership",
                data=json.dumps({"player_name": player_name}),
                timeout=5,
            )
            response.raise_for_status()
            return json.loads(response.content.decode("utf-8"))
        except Exception as exc:
            logger.error(exc)
            return exc

    def get_game_week_xg_xa(self, game_week: int):
        try:
            response = requests.post(
                self.api_url + "gw_xg_xa",
                data=json.dumps({"game_week": game_week}),
                timeout=5,
            )
            response.raise_for_status()
            return json.loads(response.content.decode("utf-8"))
        except Exception as exc:
            logger.error(exc)
            return exc

    def get_player_xq_xa(self, player_name: str):
        try:
            response = requests.post(
                self.api_url + "player_xg_xa",
                data=json.dumps({"player_name": player_name}),
                timeout=5,
            )
            response.raise_for_status()
            return json.loads(response.content.decode("utf-8"))
        except Exception as exc:
            logger.error(exc)
            return exc
