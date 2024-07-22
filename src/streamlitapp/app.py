import sys
from statistics import mean

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

player_list = data.get_players()
random_players = ["Eberechi Eze", "Cole Palmer"]  # TODO: ref with top 2 players

player_positions = {
    "GKP": [0, 0, 1, 0],
    "DEF": [1, 0, 0, 0],
    "MID": [0, 0, 0, 1],
    "FWD": [0, 1, 0, 0],
}  # todo: ref, impl dict vectorizer

match = {"home": 1, "away": 0}

# Streamlit App
st.title("Fantasy Premier League Dashboard")

menu = ["General Overview", "Player Comparison", "Points Prediction"]
choice = st.sidebar.selectbox("Select a View", menu)

gw_points_table = go.Figure(
    data=[
        go.Table(
            header=dict(
                values=list(game_week_points[0].keys()),
                # fill_color='paleturquoise',
                align="left",
                line_color="white",
            ),
            cells=dict(
                values=[
                    list(column)
                    for column in zip(*[list(idx.values()) for idx in game_week_points])
                ],
                # fill_color='lavender',
                align="left",
                line_color="white",
            ),
        )
    ]
)  # TODO: styling updates
gw_points_table.update_layout(title="Game week points")

gw_points_ownership_table = go.Figure(
    data=[
        go.Table(
            header=dict(
                values=list(gw_points_ownership[0].keys()),
                # fill_color='paleturquoise',
                align="left",
                line_color="white",
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
                line_color="white",
            ),
        )
    ]
)
gw_points_ownership_table.update_layout(title="Game week points per 90 & ownership")

gw_xg_xa_table = go.Figure(
    data=[
        go.Table(
            header=dict(
                values=list(gw_xg_xa[0].keys()),
                # fill_color='paleturquoise',
                align="left",
                line_color="white",
            ),
            cells=dict(
                values=[
                    list(column)
                    for column in zip(*[list(idx.values()) for idx in gw_xg_xa])
                ],
                # fill_color='lavender',
                align="left",
                line_color="white",
            ),
        )
    ]
)
gw_xg_xa_table.update_layout(title="Game week expected points and assists")

points_comparison = go.Figure()
points_per_90_comparison = go.Figure()
expected_goals_comparison = go.Figure()
expected_assists_comparison = go.Figure()

if choice == "General Overview":
    st.subheader("Top 5 Players by Category")
    # TODO: show stats per position
    st.plotly_chart(gw_points_table)
    st.plotly_chart(gw_points_ownership_table)
    st.plotly_chart(gw_points_ownership_table)
    st.plotly_chart(gw_xg_xa_table)

elif choice == "Player Comparison":
    st.subheader("Player Comparison")

    players_selected = st.multiselect(
        "Select Players to Compare", player_list["players"], default=random_players
    )

    if players_selected:
        # stats = {name: {} for name in players_selected}
        for player in players_selected:
            points_per_gw = data.get_player_points_per_game_week(player)[
                "points_per_gw"
            ]
            points_ownership_per_gw = data.get_player_90_points_ownership(player)[
                "points_ownership"
            ]
            player_xg_xa_per_gw = data.get_player_xq_xa(player)["player_xg_xa"]

            game_weeks = [entry["GW"] for entry in points_per_gw]
            total_points = [entry["total_points"] for entry in points_per_gw]
            # add a trace for each player
            points_comparison.add_trace(
                go.Scatter(
                    x=game_weeks,
                    y=total_points,
                    mode="lines",
                    name=player,
                    hovertemplate="GW=%{x}<br>total points=%{y}<extra></extra>",
                )
            )

            points_per_90_comparison.add_trace(
                go.Bar(
                    x=[player],
                    y=[
                        mean(
                            [
                                entry["points_per_90"]
                                for entry in points_ownership_per_gw
                            ]
                        )
                    ],
                    name=player,
                    hovertemplate="Aggregated Points per 90=%{y}<extra></extra>",
                )
            )

            game_weeks_expected = [entry["GW"] for entry in player_xg_xa_per_gw]
            player_expected_goals = [
                entry["expected_goals"] for entry in player_xg_xa_per_gw
            ]
            player_expected_assists = [
                entry["expected_assists"] for entry in player_xg_xa_per_gw
            ]

            expected_goals_comparison.add_trace(
                go.Bar(
                    x=game_weeks_expected,
                    y=player_expected_goals,
                    name=player,
                    hovertemplate="GW=%{x}<br>xG=%{y}<extra></extra>",
                )
            )
            expected_assists_comparison.add_trace(
                go.Bar(
                    x=game_weeks_expected,
                    y=player_expected_assists,
                    name=player,
                    hovertemplate="GW=%{x}<br>xA=%{y}<extra></extra>",
                )
            )

        points_comparison.update_layout(
            title="Points per Game week",
            xaxis_title="Game Week (GW)",
            yaxis_title="Total points",
            legend_title="Players",
        )
        points_per_90_comparison.update_layout(
            title="Aggregated Points per 90",
            xaxis_title="Game Week(GW)",
            yaxis_title="Aggregated Points Per 90 minutes",
            # barmode="group",
            showlegend=False,
        )
        expected_goals_comparison.update_layout(
            title="Player expected Goals per Game week",
            xaxis_title="Game Week(GW)",
            yaxis_title="expected goals (xG)",
            barmode="group",
            legend_title="Players",
        )
        expected_assists_comparison.update_layout(
            title="Player expected Assists per Game week",
            xaxis_title="Game Week(GW)",
            yaxis_title="expected assists (xA)",
            barmode="group",
            legend_title="Players",
        )

        st.plotly_chart(points_comparison)
        st.plotly_chart(points_per_90_comparison)
        st.plotly_chart(expected_goals_comparison)
        st.plotly_chart(expected_assists_comparison)
    else:
        st.warning("Please select at least one player to compare")

elif choice == "Points Prediction":  # TODO: fix reload bug
    st.subheader(choice)

    player_position_selector = st.selectbox(
        "FPL Player Position", tuple(player_positions.keys())
    )
    player_position = player_positions[player_position_selector]

    player_value_input = st.number_input("FPL Player value")  # TODO: set min, max value
    player_value = player_value_input * 10  # TODO: make dynamic

    home_away_input = st.selectbox("match location", tuple(match.keys()))
    home_away = match[home_away_input]

    player_data = player_position
    player_data.append(player_value)
    player_data.append(home_away)

    if st.button("Predict", type="primary"):
        prediction = data.get_points_prediction(player_data)
        if prediction:
            st.caption(
                f":blue[FPL projected points: {prediction['forecast']}]"
            )  # TODO: ref
