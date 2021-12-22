import os
import warnings
# API
import numpy as np
# Dash configuration
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from server import app

warnings.filterwarnings("ignore")

dashboard_colors = {
    "graph_bg": "#ffffff",
    "graph_line": "#1FCFE4"
}
GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 750)
init_error = (2*np.random.random(200) - 1)

# Create success layout
layout = html.Div(
            className="row",
            children=[
            html.Div(
                [
                    html.Div(
                        [html.H6("Water Level (m)", className="graph-title")]
                    ),
                    dcc.Graph(
                        id="wind-speed",
                        figure=dict(
                            # layout=dict(
                            #     plot_bgcolor=dashboard_colors["graph_bg"],
                            #     paper_bgcolor=dashboard_colors["graph_bg"],
                            # )
                        ),
                    ),
                    dcc.Interval(
                        id="wind-speed-update",
                        interval=int(GRAPH_INTERVAL),
                        n_intervals=0,
                    ),
                ],
                className="two-thirds column container",
            ),
            ])

@app.callback(
    Output("wind-speed", "figure"), [Input("wind-speed-update", "n_intervals")]
)
def gen_wind_speed(interval):
    """
    Generate the wind speed graph.
    :params interval: update the graph based on an interval
    """
    t = (np.arange(100) + interval)/130
    speed = np.sin(2*np.pi * t )
    error = np.roll(init_error, -1*interval)*0.4
    trace = dict(
        type="scatter",
        y=speed,
        line={"color": "#42C4F7"},
        hoverinfo="skip",
        error_y={
            "type": "data",
            "array": error,
            "thickness": 1.5,
            "width": 2,
            "color": "#B4E8FC",
        },
        mode="lines",
    )

    layout = dict(
        plot_bgcolor=dashboard_colors["graph_bg"],
        paper_bgcolor=dashboard_colors["graph_bg"],
        font={"color": "#000"},
        height=700,
        xaxis={
            "range": [0, 100],
            "showline": True,
            "zeroline": False,
            "fixedrange": True,
            "tickvals": [0, 50, 100],
            "ticktext": ["100", "50", "0"],
            "title": "Time Elapsed (sec)",
        },
        yaxis={
            "range": [-1.1, 1.1],
            "showgrid": True,
            "showline": True,
            "fixedrange": True,
            "zeroline": False,
            "gridcolor": dashboard_colors["graph_line"]
            #"nticks": max(6, round(speed.iloc[-1] / 10)),
        },
    )

    return dict(data=[trace], layout=layout)
