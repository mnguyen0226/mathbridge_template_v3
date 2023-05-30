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
def rand_exp_layout():
    tabs = html.Div(
        [
            dbc.Tabs(
                id="selected_tab",
                children=[
                    dbc.Tab(
                        label="Theory",
                        tab_id="theory_tab",
                    ),
                    dbc.Tab(
                        label="Playground",
                        tab_id="pg_tab",
                    ),
                    dbc.Tab(
                        label="Source Code",
                        tab_id="code_tab",
                    ),
                ],
                active_tab="theory_tab",
            ),
            html.Br(),
            html.Div(id="tab_layout"),
        ]
    )
    return tabs


#######################################
# Callbacks
#######################################
@my_app.callback(
    Output(component_id="tab_layout", component_property="children"),
    [Input(component_id="selected_tab", component_property="active_tab")],
)
def render_tab_1(tab_choice):
    """Renders the selected subtab's layout

    Args:
        tab_choice (str): selected subtab

    Returns:
        selected subtab's layout
    """
    if tab_choice == "theory_tab":
        return theory_tab_layout()
    if tab_choice == "pg_tab":
        return playground_tab_layout()
    if tab_choice == "code_tab":
        return codeblock_tab_layout()


#######################################
# Theory Layout
#######################################
def theory_tab_layout():
    subtab_layout = html.Div(
        [
            html.H3("Lehman Generator"),
            dcc.Markdown(
                children=read_file_as_str("utils/markdown/tab_1/lehman.md"),
                mathjax=True,
            ),
            html.Hr(),
        ],
    )
    return subtab_layout


#######################################
# Playground Layout
#######################################
def playground_tab_layout():
    """Renders the layout of playground tab

    Returns:
        selected subtab's layout
    """
    subtab_layout = html.Div(
        [
            html.H3("Lehman Generator Visualization"),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("Random Seed"), width="auto"),
                        dbc.Col(
                            dbc.Input(
                                id="r_seed",
                                type="number",
                                value=12345678,
                            ),
                            width="auto",
                        ),
                    ],
                    align="center",
                ),
            ),
            html.Br(),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("M Value"), width="auto"),
                        dbc.Col(
                            dbc.Input(
                                id="m",
                                type="number",
                                value=2147483647,
                            ),
                            width="auto",
                        ),
                    ],
                    align="center",
                ),
            ),
            html.Br(),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("A Value"), width="auto"),
                        dbc.Col(
                            dbc.Input(
                                id="a",
                                type="number",
                                value=48271,
                            ),
                            width="auto",
                        ),
                    ],
                    align="center",
                ),
            ),
            html.Br(),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("Q Value"), width="auto"),
                        dbc.Col(
                            dbc.Input(
                                id="q",
                                type="number",
                                value=44488,
                            ),
                            width="auto",
                        ),
                    ],
                    align="center",
                ),
            ),
            html.Br(),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("R Value"), width="auto"),
                        dbc.Col(
                            dbc.Input(
                                id="r",
                                placeholder="Please enter numerical value",
                                type="number",
                                value=3399,
                            ),
                            width="auto",
                        ),
                    ],
                    align="center",
                ),
            ),
            html.Br(),
            dbc.Label("Number of samples to generate"),
            dcc.Slider(
                id="n_samples",
                min=1,
                max=1000,
                value=150,
                marks={data: str(data) for data in range(0, 1000, 50)},
                step=100,
            ),
            html.Br(),
            dbc.Label("Number of bins to generate"),
            dcc.Slider(
                id="bins_desired",
                min=2,
                max=100,
                value=2,
                marks={data: str(data) for data in range(0, 100, 10)},
                step=10,
            ),
            html.Br(),
            dbc.Label("Choose an appropriate alpha for W:"),
            dcc.Slider(
                id="alpha",
                min=0.01,
                max=1,
                value=0.5,
                marks={data: f"{data:.2f}" for data in np.linspace(0.0, 1, 11)},
                step=0.01,
            ),
            html.Br(),
            html.Hr(),
            html.Div(
                [
                    html.Strong(
                        "Histogram of the value-spread of the uniform distribution"
                    ),
                    dcc.Graph(id="uniform_graph"),
                ],
            ),
            html.Div(
                [
                    html.Strong("Histogram of the value-spread of the V distribution"),
                    dcc.Graph(id="v_graph"),
                ],
            ),
            html.Div(
                [
                    html.Strong("Histogram of the value-spread of the W distribution"),
                    dcc.Graph(id="w_graph"),
                ],
            ),
        ]
    )
    return subtab_layout


#######################################
# Playground Callbacks
#######################################
@my_app.callback(
    Output(component_id="uniform_graph", component_property="figure"),
    Output(component_id="v_graph", component_property="figure"),
    Output(component_id="w_graph", component_property="figure"),
    Input(component_id="n_samples", component_property="value"),
    Input(component_id="bins_desired", component_property="value"),
    Input(component_id="r_seed", component_property="value"),
    Input(component_id="m", component_property="value"),
    Input(component_id="a", component_property="value"),
    Input(component_id="q", component_property="value"),
    Input(component_id="r", component_property="value"),
    Input(component_id="alpha", component_property="value"),
)
def render_playground_tab(n_samples, bins, r_seed, m, a, q, r, scaledown):
    axis_dict = dict(mirror=True, ticks="outside", showline=True, title="")
    randGen = RandTool(m, a, q, r, r_seed)
    a, b, c = randGen.getUniformUVW(n_samples, scaledown)
    U = px.histogram(a, nbins=bins, template="simple_white")
    V = px.histogram(b, nbins=bins, template="simple_white")
    W = px.histogram(c, nbins=bins, template="simple_white")

    U.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    V.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    W.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    return U, V, W


#######################################
# Codeblock Layout
#######################################
def codeblock_tab_layout():
    subtab_layout = html.Div(
        [
            html.H3("Source Code"),
            dbc.Label(
                "In this section, we will see how to generate the histograms with a simple Python Program."
            ),
            dbc.Label("We recommend you to download and try running the code!"),
            dcc.Markdown(
                id="code_block_md",
                children=read_file_as_str(
                    "./utils/markdown/tab_1/code_markdown_rand.md"
                ),
                mathjax=True,
            ),
            dbc.Button(
                "Download Code",
                color="success",
                className="me-1",
                id="btn_download_rand",
            ),
            dcc.Download(id="download_py"),
        ]
    )
    return subtab_layout


#######################################
# Codeblock Callbacks
#######################################
@my_app.callback(
    Output(component_id="download_py", component_property="data"),
    Input(component_id="btn_download_rand", component_property="n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file("./utils/download_codes/tab_1/random_gen.py")
