import sys

import plotly.graph_objects as go
import streamlit as st
from data.data import Data

sys.path.insert(0, "..")
from utils.config import get_config

CONFIG = get_config()
data = Data(api_url=CONFIG["api"]["endpoint_url"])

# TODO: get latest game week
gw = 38
game_week_points = data.get_game_week_points(gw)["gw_points"][:5]
gw_points_ownership = data.get_game_week_points_ownership(gw)[
    "player_points_ownership"
][:5]
gw_xg_xa = data.get_game_week_xg_xa(gw)["gw_xg_xa"][:5]

# Streamlit App
st.title("Fantasy Premier League Dashboard")

menu = ["General Overview", "Player Comparison", "Points Prediction"]
choice = st.sidebar.selectbox("Select a View", menu)

if choice == "General Overview":
    st.subheader("Top 5 Players by Category")
    # TODO: show stats per position
    gw_points_table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(game_week_points[0].keys()),
                    # fill_color='paleturquoise',
                    align="left",
                ),
                cells=dict(
                    values=[
                        list(column)
                        for column in zip(
                            *[list(idx.values()) for idx in game_week_points]
                        )
                    ],
                    # fill_color='lavender',
                    align="left",
                ),
            )
        ]
    )
    gw_points_table.update_layout(title="Game week points")
    st.plotly_chart(gw_points_table)

    gw_points_ownership_table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(gw_points_ownership[0].keys()),
                    # fill_color='paleturquoise',
                    align="left",
                ),
                cells=dict(
                    values=[
                        list(column)
                        for column in zip(
                            *[list(idx.values()) for idx in gw_points_ownership]
                        )
                    ],
                    # fill_color='lavender',
                    align="left",
                ),
            )
        ]
    )
    gw_points_ownership_table.update_layout(title="Game week points per 90 & ownership")
    st.plotly_chart(gw_points_ownership_table)

    gw_xg_xa_table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(gw_xg_xa[0].keys()),
                    # fill_color='paleturquoise',
                    align="left",
                ),
                cells=dict(
                    values=[
                        list(column)
                        for column in zip(*[list(idx.values()) for idx in gw_xg_xa])
                    ],
                    # fill_color='lavender',
                    align="left",
                ),
            )
        ]
    )
    gw_xg_xa_table.update_layout(title="Game week expected points and assists")
    st.plotly_chart(gw_xg_xa_table)
