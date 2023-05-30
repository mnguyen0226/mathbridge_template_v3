# dash imports
from dash import dcc
from dash import html
from dash import Input
from dash import Output

# other imports
import numpy as np
import plotly.express as px

# file imports
from maindash import my_app
from utils.stats.random_tool import RandTool
from utils.others.file_operations import read_file_as_str


#######################################
# Dash Layout
#######################################
def rand_exp_layout():
    """Renders the layout of tab 1

    Returns:
        selected subtab's layout
    """
    tab_1_layout = html.Div(
        [
            dcc.Tabs(
                id="selected_tab",
                children=[
                    dcc.Tab(label="Playground", value="pg_tab"),
                    dcc.Tab(label="Code Blocks", value="code_tab"),
                ],
                value="pg_tab",
            ),
            html.Div(id="tab_layout"),
        ]
    )
    return tab_1_layout


#######################################
# Dash Callbacks
#######################################
@my_app.callback(
    Output(component_id="tab_layout", component_property="children"),
    Input(component_id="selected_tab", component_property="value"),
)
def render_tab_1(tab_choice):
    """Renders the selected subtab's layout

    Args:
        tab_choice (str): selected subtab

    Returns:
        selected subtab's layout
    """
    if tab_choice == "pg_tab":
        return playground_tab_layout()
    if tab_choice == "code_tab":
        return codeblock_tab_layout()


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
            html.H3("Visualizing Random Expressions"),
            html.Strong("Basic Lehman Generator:"),
            html.Br(),
            dcc.Markdown(id="lehman_md", className="markdown-view", mathjax=True),
            html.Div(
                [
                    html.H4("Random Seed"),
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
                            html.H4("No of bins to generate:"),
                            dcc.Slider(
                                id="bins_desired",
                                min=2,
                                max=100,
                                value=2,
                                marks={data: str(data) for data in range(0, 100, 10)},
                                step=10,
                            ),
                            html.Br(),
                            html.H4("Choose an appropriate alpha for W:"),
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
                            dcc.Graph(id="uniform_graph"),
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
                            dcc.Graph(id="v_graph"),
                        ],
                        className="grouped-graphs",
                    ),
                    html.Div(
                        [
                            html.Strong(
                                "Histogram of the value-spread of the W distribution"
                            ),
                            dcc.Graph(id="w_graph"),
                        ],
                        className="grouped-graphs",
                    ),
                ],
                className="row-pane",
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
    Output(component_id="lehman_md", component_property="children"),
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
    lehman_text = read_file_as_str("utils/markdown/tab_1/lehman.md")
    U = px.histogram(a, nbins=bins, template="simple_white")
    V = px.histogram(b, nbins=bins, template="simple_white")
    W = px.histogram(c, nbins=bins, template="simple_white")

    U.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    V.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    W.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    return U, V, W, lehman_text


#######################################
# Codeblock Layout
#######################################
def codeblock_tab_layout():
    """Renders the layout of codeblock tab

    Returns:
        selected subtab's layout
    """
    subtab_layout = html.Div(
        [
            dcc.Markdown(
                id="code_block_md",
                children=read_file_as_str(
                    "./utils/markdown/tab_1/code_markdown_rand.md"
                ),
                className="code-markdown-view",
                mathjax=True,
            ),
            html.Button(
                "Download Code", id="btn_download_rand", className="btn-download"
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
