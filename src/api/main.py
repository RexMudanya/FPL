from model import predict, train
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException

# pydantic models


class PlayerDataIn(BaseModel):
    input: list


class PointsPrediction(PlayerDataIn):
    forecast: int


class FPLModel(BaseModel):
    trainedModel: tuple[str, dict]


app = FastAPI()


@app.get("/ping")
def pong():
    return {"ping": "pong!"}


@app.post("/predict", response_model=PointsPrediction, status_code=200)
def get_prediction(payload: PlayerDataIn):
    input = payload.input

    prediction = predict(input)

    if not prediction:
        raise HTTPException(status_code=400, detail="Model not found")

    response_object: dict = {"input": input, "forecast": prediction}
    return response_object


@app.post("/train", response_model=FPLModel, status_code=200)
def train_model():
    model_file, metrics = train()

    if not model_file and metrics:
        raise HTTPException(status_code=400, detail="Training failed, check logs")

    response_object = {"model_location": model_file, "metrics": metrics}

    return response_object
