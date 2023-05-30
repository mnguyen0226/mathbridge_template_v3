# dash imports
from dash import dcc
from dash import html
from dash import Input
from dash import Output
import dash_bootstrap_components as dbc

# other imports
import numpy as np
import plotly.express as px

# file imports
from maindash import my_app
from utils.stats.random_tool import RandTool
from utils.others.file_operations import read_file_as_str


#######################################
# Layout
#######################################
def about_layout():
    layout = html.Div(
        [
            html.H3("About", style={"textAlign": "center"}),
            html.Br(),
            dbc.Label("This website is the playground for Linear Algebra, Statistic, & Machine Learning Algorithm."),
            html.Br(),
            dbc.Card(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.CardImg(
                                    src="https://dash-bootstrap-components.opensource.faculty.ai/static/images/portrait-placeholder.png",
                                    className="img-fluid rounded-start",
                                ),
                                className="col-md-4",
                            ),
                            dbc.Col(
                                dbc.CardBody(
                                    [
                                        html.H4("Professor Sara Hooshangi", className="card-title"),
                                        html.P(
                                            "Collegiate Associate Professor "
                                            "Director, Master of Engineering Program "
                                            "at Virginia Tech.",
                                            className="card-text",
                                        ),
                                        html.Small(
                                            "shoosh@vt.edu",
                                            className="card-text text-muted",
                                        ),
                                    ]
                                ),
                                className="col-md-8",
                            ),
                        ],
                        className="g-0 d-flex align-items-center",
                    )
                ],
                className="mb-3",
                style={"maxWidth": "540px"},
            ),
            html.Hr(),
            dbc.Label("© 2023 Mathbridge All Rights Reserved."),
            html.Hr(),
        ]
    )
    return layout
