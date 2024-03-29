import json
import sys

import requests
import streamlit as st

sys.path.insert(0, "..")

from utils.config import get_config

# todo: modular structure

CONFIG = get_config()

player_positions = {
    "GKP": [0, 0, 1, 0],
    "DEF": [1, 0, 0, 0],
    "MID": [0, 0, 0, 1],
    "FWD": [0, 1, 0, 0],
}  # todo: ref, impl dict vectorizer

match = {"home": 1, "away": 0}


def send_request(input: list):  # todo: impl send request
    return requests.post(
        url=CONFIG["api"]["endpoint_url"],
        data=json.dumps({"input": input}),
    )


player_position_selector = st.selectbox(
    "FPL Player Position", tuple(player_positions.keys())
)
player_position = player_positions[player_position_selector]

player_value_input = st.number_input("FPL player value")  # todo: set min, max value
player_value = player_value_input * 10  # note: may change based on model, ref impl

home_away_input = st.selectbox("match location", tuple(match.keys()))
home_away = match[home_away_input]

player_data = player_position

player_data.append(player_value)
player_data.append(home_away)

if st.button("Ok", type="primary"):
    prediction = send_request(player_data)
    if prediction:
        st.caption(f":blue[FPL projected points: {prediction.json()['forecast']}]")
