# dash imports
import dash
from dash import html
from dash import Input
from dash import Output
from dash import dcc

# other imports
import numpy as np
import plotly.io as pio
import plotly.express as px
import pandas as pd
import math
import json

# file imports
from maindash import my_app
from src.helper_functions.helpers import read_file_as_str

#######################################
# Initial Settings
#######################################
pio.templates
server = my_app.server
external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "assets/custom.css",
]


#######################################
# Dash Layout
#######################################
my_app.layout = html.Div(
    [
        html.H2("Mathbridge Course"),
        dcc.Tabs(
            id="viz_tabs",
            children=[
                dcc.Tab(label="Random Expressions", value="rand_exp"),
                dcc.Tab(label="Neural Networks", value="nn"),
                dcc.Tab(label="Distributions", value="dist"),
                dcc.Tab(label="Functions Plotted", value="functions"),
                dcc.Tab(label="Eigen Vector & Eigen Values", value="eigen"),
            ],
            value="main_tab",
        ),
        html.Div(id="layout"),
    ],
    className="outer-div",
)  # NOTE: className is for styling

#######################################
# Dash Callbacks
#######################################


if __name__ == "__main__":
    my_app.run_server(debug=True, host="0.0.0.0", port=80)
