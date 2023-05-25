# dash imports
import dash
from dash import html
from dash import Input
from dash import Output
from dash import dcc

# other imports
import plotly.io as pio

# file imports
from maindash import my_app
from components.tab_1 import random_exp
from components.tab_2 import dist
from components.tab_3 import func
from components.tab_4 import eigen

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
        html.H2("Mathbridge @ Virginia Tech"),
        dcc.Tabs(
            id="tab_bar",
            children=[
                dcc.Tab(label="Random Expressions", value="rand_exp_tab"),
                dcc.Tab(label="Distributions", value="dist_tab"),
                dcc.Tab(label="Functions Plotted", value="func_tab"),
                dcc.Tab(label="Eigen", value="eigen_tab"),
            ],
            value="rand_exp_tab", # default page
        ),
        html.Div(id="layout"),
    ],
    className="outer-div",
)

#######################################
# Dash Callbacks
#######################################
@my_app.callback(
    Output(
        component_id="layout", component_property="children"
    ), 
    Input(component_id="tab_bar", component_property="value"),
)
def render_main_page(tab_choice):
    """Renders the selected tab

    Args:
        tab_choice (str): dash Tab component's value

    Returns:
        _type_: selected tab
    """
    if tab_choice == "rand_exp_tab":
        return random_exp.rand_exp_layout()
    if tab_choice == "dist_tab":
        return dist.dist_layout()
    if tab_choice == "func_tab":
        return func.func_layout()
    if tab_choice == "eigen_tab":
        return eigen.eigen_layout()


if __name__ == "__main__":
    my_app.run_server(debug=True, host="0.0.0.0", port=80)
