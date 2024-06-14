import streamlit as st
import sys

from data.data import Data

sys.path.insert(0, "..")
from utils.config import get_config

CONFIG = get_config()
data = Data(api_url=CONFIG["api"]["endpoint_url"])

# TODO: get latest game week
gw = 38
game_week_points = data.get_game_week_points(gw)["gw_points"][:5]
gw_points_ownership = data.get_game_week_points_ownership(gw)["player_points_ownership"][:5]
gw_xg_xa = data.get_game_week_xg_xa(gw)["gw_xg_xa"][:5]

# Streamlit App
st.title("Fantasy Premier League Dashboard")

menu = ["General Overview", "Player Comparison", "Points Prediction"]
choice = st.sidebar.selectbox("Select a View", menu)

if choice == "General Overview":
    st.subheader("Top 5 Players by Category")
    # TODO: show stats per position
    st.title("Game week Points")
    st.table(game_week_points)
    st.title("Game week Points per 90 minutes and ownership")
    st.table(gw_points_ownership)
    st.title("Game week expected Goals and Assists")
    st.table(gw_xg_xa)
