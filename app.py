# dash imports
from dash import html
from dash import Input
from dash import Output
from dash import dcc
import dash_bootstrap_components as dbc

# other imports
import plotly.io as pio

# file imports
from maindash import my_app
from components.tab_1 import random_exp
from components.tab_2 import dist
from components.tab_3 import func
from components.tab_4 import eigen
from components.about import about

#######################################
# Initial Settings
#######################################
pio.templates
server = my_app.server

#######################################
# Styling
#######################################
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",  # grey color
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


#######################################
# Layout
#######################################

# sidebar layout
sidebar = html.Div(
    [
        html.H2("Virginia Tech MathBridge", className="display-6"),
        html.Hr(),
        html.P(
            "Linear Algebra, Statistics, & Machine Learning Visualization",
            className="lead",
        ),
        # Nav component
        dbc.Nav(
            [
                dbc.NavLink("About", href="/", active="exact"),
                dbc.NavLink("Random Expressions", href="/rand_exp", active="exact"),
                dbc.NavLink("Distributions", href="/dist", active="exact"),
                dbc.NavLink("Functions Plotted", href="/func", active="exact"),
                dbc.NavLink("Eigen", href="/eigen", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# main page layout
content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

# binding sidebar and content
my_app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


#######################################
# Callbacks
#######################################
@my_app.callback(
    Output(component_id="page-content", component_property="children"),
    [Input(component_id="url", component_property="pathname")],
)
def render_page_content(pathname):
    if pathname == "/":
        return about.about_layout()
    elif pathname == "/rand_exp":
        return random_exp.rand_exp_layout()

    elif pathname == "/dist":
        return dist.dist_layout()

    elif pathname == "/func":
        return func.func_layout()

    elif pathname == "/eigen":
        return eigen.eigen_layout()

    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    my_app.run_server(debug=True, host="0.0.0.0", port=80)
