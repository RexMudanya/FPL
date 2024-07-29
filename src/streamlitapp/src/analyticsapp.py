import plotly.graph_objects as go
import streamlit as st


@st.cache_data
def draw_table(table_data, title: str, align="left", line_color="white"):
    table = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(table_data[0].keys()),
                    # fill_color='paleturquoise',
                    align=align,
                    line_color=line_color,
                ),
                cells=dict(
                    values=[
                        list(column)
                        for column in zip(*[list(idx.values()) for idx in table_data])
                    ],
                    # fill_color='lavender',
                    align=align,
                    line_color=line_color,
                ),
            )
        ]
    )  # TODO: styling updates
    table.update_layout(title=title)

    return table


class App:
    def __init__(self):
        pass
