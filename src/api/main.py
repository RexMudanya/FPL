from fastapi import FastAPI, HTTPException
from model import predict, train
from pydantic import BaseModel, PydanticUserError

from ml_system.data_viz import FPLDataStats
from utils.config import get_config

# pydantic models


class PlayerDataIn(BaseModel):
    input: list


class PointsPrediction(PlayerDataIn):
    forecast: int


try:

    class FPLModel(BaseModel):
        trainedModel: any

except PydanticUserError as exc:
    assert exc.code == "schema-for-unknown-type"


class GameWeekDataIn(BaseModel):
    game_week: int


class PlayerNameIn(BaseModel):
    player_name: str


CONFIG = get_config()
fpl_data_stats = FPLDataStats(
    CONFIG["training_data"]["git_repo_url"],
    CONFIG["training_data"]["training_season"],
    CONFIG["training_data"]["data_location"],
)

app = FastAPI(debug=True)  # TODO: ref


@app.post("/predict", response_model=PointsPrediction, status_code=200)
def get_prediction(payload: PlayerDataIn):
    data_input = payload.input

    prediction = predict(data_input)

    if not prediction:
        raise HTTPException(status_code=400, detail="Model not found")

    response_object: dict = {"input": data_input, "forecast": prediction}
    return response_object


@app.get("/train", status_code=200)
def train_model():
    model_file, metrics = train()

    if not model_file and metrics:
        raise HTTPException(status_code=400, detail="Training failed, check logs")

    response_object = {"model_location": model_file, "metrics": metrics}

    return response_object


@app.get("/players", status_code=200)
def players():
    return {"players": fpl_data_stats.player_list}


@app.get("/goals_scored", status_code=200)
def goals_scored():
    return {"goal_data": fpl_data_stats.goal_distribution()}


@app.get("/assists", status_code=200)
def assists():
    return {"assist_data": fpl_data_stats.assist_distribution()}


@app.get("/clean_sheets", status_code=200)
def clean_sheets():
    return {"clean_sheet_table": fpl_data_stats.clean_sheet_table()}


@app.post("/game_week_points", status_code=200)
def game_weeks_points(payload: GameWeekDataIn):
    return {"gw_points": fpl_data_stats.get_points_per_gw_board(payload.game_week)}


@app.post("/point_ownership", status_code=200)
def all_player_points_ownership(payload: GameWeekDataIn):
    return {
        "player_points_ownership": fpl_data_stats.get_points90_ownership_board(
            payload.game_week
        )
    }


@app.post("/player_points_per_gw", status_code=200)
def player_points_per_gw(payload: PlayerNameIn):
    return {
        "points_per_gw": fpl_data_stats.get_player_points_per_gw(payload.player_name)
    }


@app.post("/points_90_ownership", status_code=200)
def player_points_90_ownership(payload: PlayerNameIn):
    return {
        "points_ownership": fpl_data_stats.get_player_points_90_ownership(
            payload.player_name
        )
    }


@app.post("/gw_xg_xa", status_code=200)
def game_week_xg_xa(payload: GameWeekDataIn):
    return {"gw_xg_xa": fpl_data_stats.get_xg_xa(payload.game_week)}


@app.post("/player_xg_xa", status_code=200)
def player_xg_xa(payload: PlayerNameIn):
    return {"player_xg_xa": fpl_data_stats.get_player_xg_xa(payload.player_name)}
