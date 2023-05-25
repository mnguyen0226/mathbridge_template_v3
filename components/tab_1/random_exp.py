from dash import dcc
from dash import html
import numpy as np
from maindash import my_app
from dash.dependencies import Input, Output
from utils.stats.random_tool import RandTool

import plotly.express as px


def readFileasStr(filename):
    with open(filename, "r") as file:
        data = file.read()
    return data


def tab1Sel1Layout():
    tab1_sel1_layout = html.Div(
        [
            html.H3("Visualizing Random Expressions"),
            html.Strong("Basic Lehmer generator:"),
            html.Br(),
            dcc.Markdown(id="lehman_md", className="markdown-view", mathjax=True),
            html.Strong(id="Number of Samples:"),
            html.Div(
                [
                    html.H4("R_seed"),
                    dcc.Input(
                        id="r_seed",
                        type="number",
                        value=12345678,
                        className="standard-gen-ip",
                    ),
                ],
                className="grouped-label-class",
            ),
            html.Div(
                [
                    html.H4("m(prime Number)"),
                    dcc.Input(
                        id="m",
                        type="number",
                        value=2147483647,
                        className="standard-gen-ip",
                    ),
                ],
                className="grouped-label-class",
            ),
            html.Div(
                [
                    html.H4("a"),
                    dcc.Input(
                        id="a", type="number", value=48271, className="standard-gen-ip"
                    ),
                ],
                className="grouped-label-class",
            ),
            html.Div(
                [
                    html.H4("q"),
                    dcc.Input(
                        id="q", type="number", value=44488, className="standard-gen-ip"
                    ),
                ],
                className="grouped-label-class",
            ),
            html.Div(
                [
                    html.H4("r"),
                    dcc.Input(
                        id="r", type="number", value=3399, className="standard-gen-ip"
                    ),
                ],
                className="grouped-label-class",
            ),
            html.Br(),
            html.Div(
                [
                    html.Div([], className="row-pane"),
                    html.Div(
                        [
                            html.H4("No of samples to generate:"),
                            dcc.Slider(
                                id="n_samples",
                                min=1,
                                max=1000,
                                value=150,
                                marks={data: str(data) for data in range(0, 1000, 50)},
                                step=100,
                            ),
                            # dcc.Input(id='n_samples', type="number", value=10),
                            html.H4("No of bins to generate:"),
                            # dcc.Input(id='bins-desired', type="number", value=10),
                            dcc.Slider(
                                id="bins-desired",
                                min=2,
                                max=100,
                                value=2,
                                marks={data: str(data) for data in range(0, 100, 10)},
                                step=10,
                            ),
                            html.Br(),
                            html.H4("Choose an appropriate alpha for W:"),
                            # dcc.Input(id='bins-desired', type="number", value=10),
                            dcc.Slider(
                                id="alpha",
                                min=0.01,
                                max=1,
                                value=0.5,
                                marks={
                                    data: f"{data:.2f}"
                                    for data in np.linspace(0.0, 1, 11)
                                },
                                step=0.01,
                            ),
                        ],
                        className="grouped-sliders",
                    ),
                    html.Div(
                        [
                            html.Strong(
                                "Histogram of the value-spread of the uniform distribution"
                            ),
                            dcc.Graph(id="uniform-graph"),
                        ],
                        className="grouped-graphs",
                    ),
                ],
                className="graphs-and-sliders",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Strong(
                                "Histogram of the value-spread of the V distribution"
                            ),
                            dcc.Graph(id="v-graph"),
                        ],
                        className="grouped-graphs",
                    ),
                    html.Div(
                        [
                            html.Strong(
                                "Histogram of the value-spread of the W distribution"
                            ),
                            dcc.Graph(id="w-graph"),
                        ],
                        className="grouped-graphs",
                    ),
                ],
                className="row-pane",
            ),
        ]
    )
    return tab1_sel1_layout


def tab1_sel2_layout():
    tab1_sel2_layout = html.Div(
        [
            dcc.Markdown(
                id="code_block_md",
                children=readFileasStr("./utils/markdown/tab_1/code_markdown_rand.md"),
                className="code-markdown-view",
                mathjax=True,
            ),
            html.Button(
                "Download Code", id="btn-download-rand", className="btn-download"
            ),
            dcc.Download(id="download-py"),
        ]
    )
    return tab1_sel2_layout


def rand_exp_layout():
    tab1Layout = html.Div(
        [
            dcc.Tabs(
                id="viz_random",
                children=[
                    dcc.Tab(label="Playground", value="pg_rnd"),
                    dcc.Tab(label="Code Blocks", value="pg_code"),
                ],
                value="pg_rnd",
            ),
            html.Div(id="layout_tab1"),
        ]
    )
    return tab1Layout


############################################
@my_app.callback(
    Output(component_id="layout_tab1", component_property="children"),
    Input(component_id="viz_random", component_property="value"),
)
def Tab1Render(ques):
    if ques == "pg_rnd":
        return tab1Sel1Layout()
        # tab1_sel1_layout

    if ques == "pg_code":
        return tab1_sel2_layout()

    return "The impaler!!!!"


############################################ DONT WORRY ABOUT THIS CODE


@my_app.callback(
    Output(component_id="uniform-graph", component_property="figure"),
    Output(component_id="v-graph", component_property="figure"),
    Output(component_id="w-graph", component_property="figure"),
    Output(component_id="lehman_md", component_property="children"),
    Input(component_id="n_samples", component_property="value"),
    Input(component_id="bins-desired", component_property="value"),
    Input(component_id="r_seed", component_property="value"),
    Input(component_id="m", component_property="value"),
    Input(component_id="a", component_property="value"),
    Input(component_id="q", component_property="value"),
    Input(component_id="r", component_property="value"),
    Input(component_id="alpha", component_property="value"),
)
def randomExpressionsGen(n_samples, bins, r_seed, m, a, q, r, scaledown):
    # a=10 * np.random.randn(1, 10)
    axis_dict = dict(mirror=True, ticks="outside", showline=True, title="")
    randGen = RandTool(m, a, q, r, r_seed)
    a, b, c = randGen.getUniformUVW(n_samples, scaledown)
    lehmanmd = readFileasStr("utils/markdown/tab_1/lehman.md")
    U = px.histogram(a, nbins=bins, template="simple_white")
    V = px.histogram(b, nbins=bins, template="simple_white")
    W = px.histogram(c, nbins=bins, template="simple_white")

    U.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    V.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    W.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    return U, V, W, lehmanmd


@my_app.callback(
    Output("download-py", "data"),
    Input("btn-download-rand", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file("./utils/download_codes/tab_1/random_gen.py")
