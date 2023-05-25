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
from components.tab_1 import random_exp

#######################################
# Initial Settings
#######################################
pio.templates
server = my_app.server

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
@my_app.callback(
    Output(
        component_id="layout", component_property="children"
    ),  # children and value are HTML property (W3 school)
    Input(component_id="viz_tabs", component_property="value"),
)
def rendertheRightTabs(ques):
    if ques == "rand_exp":
        return random_exp.randomExpressionLayout()
    if ques == "dist":
        pass
        #  return tab3.tab3Layout()
    if ques == "functions":
        pass
        #  return tab4.functionsLayout()
    if ques == "eigen":
        pass
        #  return tab5.tab5Layout()


if __name__ == "__main__":
    my_app.run_server(debug=True, host="0.0.0.0", port=80)
