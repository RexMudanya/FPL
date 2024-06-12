import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Sample DataFrame (Replace this with actual FPL data)
np.random.seed(42)
players = ["Player A", "Player B", "Player C", "Player D", "Player E"]  # TODO: remove
gameweeks = list(range(1, 39))  # TODO: remove
data = {
    "Player": np.repeat(players, len(gameweeks)),
    "Gameweek": gameweeks * len(players),
    "Points": np.random.randint(0, 15, len(players) * len(gameweeks)),
    "Points_per_90": np.random.uniform(0, 10, len(players) * len(gameweeks)),
    "Ownership_Percentage": np.random.uniform(5, 60, len(players) * len(gameweeks)),
    "Form": np.random.uniform(0, 10, len(players) * len(gameweeks)),
    "Season_Average": np.random.uniform(0, 10, len(players) * len(gameweeks)),
    "xG": np.random.uniform(0, 1, len(players) * len(gameweeks)),
    "xA": np.random.uniform(0, 1, len(players) * len(gameweeks)),
    "Minutes_Played": np.random.randint(0, 90, len(players) * len(gameweeks)),
    "Clean_Sheets": np.random.choice([0, 1], len(players) * len(gameweeks)),
    "Price": np.random.uniform(4.0, 12.0, len(players) * len(gameweeks)),
    "Fixture_Difficulty": np.random.randint(1, 5, len(players) * len(gameweeks)),
}  # TODO: ref
df = pd.DataFrame(data)  # TODO: ref

# Aggregating data for visualizations
agg_data = (
    df.groupby("Player")
    .agg(
        {
            "Points": "sum",
            "Points_per_90": "mean",
            "Ownership_Percentage": "mean",
            "Form": "mean",
            "Season_Average": "mean",
            "xG": "sum",
            "xA": "sum",
            "Minutes_Played": "sum",
            "Clean_Sheets": "sum",
            "Price": "mean",
            "Fixture_Difficulty": "mean",
        }
    )
    .reset_index()
)  # TODO: ref

# Creating sample plots
fig_points_per_gameweek = px.line(
    df, x="Gameweek", y="Points", color="Player", title="Points per Gameweek"
)  # TODO: ref
fig_points_vs_ownership = px.scatter(
    agg_data,
    x="Points_per_90",
    y="Ownership_Percentage",
    text="Player",
    title="Points per 90 Minutes vs. Ownership Percentage",
)  # TODO: ref
fig_form_vs_season = px.bar(
    agg_data, x="Player", y=["Form", "Season_Average"], title="Form vs. Season Average"
)
fig_xg_xa_trends = px.line(
    df.groupby("Gameweek").sum().reset_index(),
    x="Gameweek",
    y=["xG", "xA"],
    title="xG and xA Trends",
)  # TODO: ref
fig_clean_sheets_vs_fdr = px.scatter(
    agg_data,
    x="Clean_Sheets",
    y="Fixture_Difficulty",
    text="Player",
    title="Clean Sheets vs. Fixture Difficulty",
)  # TODO: ref

# Streamlit App
st.title("Fantasy Premier League Dashboard")

menu = ["General Overview", "Player Comparison", "Points Prediction"]
choice = st.sidebar.selectbox("Select a View", menu)

if choice == "General Overview":
    st.subheader("General Overview")
    # TODO: load a table of top players per stat
    # TODO: show stats per position
    st.plotly_chart(fig_points_per_gameweek)
    st.plotly_chart(fig_points_vs_ownership)
    st.plotly_chart(fig_form_vs_season)
    st.plotly_chart(fig_xg_xa_trends)
    st.plotly_chart(fig_clean_sheets_vs_fdr)

elif choice == "Player Comparison":
    st.subheader("Player Comparison")

    players_selected = st.multiselect(
        "Select Players to Compare", players, default=players[:2]
    )  # TODO: set top player

    if players_selected:
        df_selected = df[df["Player"].isin(players_selected)]
        agg_selected = agg_data[agg_data["Player"].isin(players_selected)]

        fig_points_comparison = px.line(
            df_selected,
            x="Gameweek",
            y="Points",
            color="Player",
            title="Points Comparison",
        )
        fig_points_per_90_comparison = px.bar(
            agg_selected,
            x="Player",
            y="Points_per_90",
            title="Points per 90 Minutes Comparison",
        )
        fig_form_vs_season_comparison = px.bar(
            agg_selected,
            x="Player",
            y=["Form", "Season_Average"],
            title="Form vs. Season Average Comparison",
        )
        fig_xg_xa_comparison = px.line(
            df_selected.groupby(["Gameweek", "Player"]).sum().reset_index(),
            x="Gameweek",
            y=["xG", "xA"],
            color="Player",
            title="xG and xA Comparison",
        )
        fig_clean_sheets_vs_fdr_comparison = px.scatter(
            agg_selected,
            x="Clean_Sheets",
            y="Fixture_Difficulty",
            text="Player",
            title="Clean Sheets vs. Fixture Difficulty Comparison",
        )

        st.plotly_chart(fig_points_comparison)
        st.plotly_chart(fig_points_per_90_comparison)
        st.plotly_chart(fig_form_vs_season_comparison)
        st.plotly_chart(fig_xg_xa_comparison)
        st.plotly_chart(fig_clean_sheets_vs_fdr_comparison)
    else:
        st.warning("Please select at least one player to compare.")

elif choice == "Points Prediction":
    # TODO: predictions for top players last GW
    # TODO: option to predict with own inputs
    pass  # TODO: Impl
