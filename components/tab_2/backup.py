# dash imports
from dash import dcc
from dash import html
from dash import Input
from dash import Output

# other imports
import plotly.express as px
import numpy as np


# file imports
from maindash import my_app
from utils.others.file_operations import read_file_as_str


#######################################
# Dash Layout
#######################################
def dist_layout():
    """Renders the layout of tab 3

    Returns:
        selected subtab's layout
    """
    tab3Layout = html.Div(
        [
            dcc.Tabs(
                id="viz_dists",
                children=[
                    dcc.Tab(label="Normal", value="normdist"),
                    dcc.Tab(label="Poisson", value="poissondist"),
                    dcc.Tab(label="Uniform", value="uniformdist"),
                    dcc.Tab(label="Binomial", value="binomdist"),
                ],
                value="normdist",
            ),
            html.Div(id="layout_tab3"),
        ]
    )
    return tab3Layout


#######################################
# Dash Callbacks
#######################################
@my_app.callback(
    Output(component_id="layout_tab3", component_property="children"),
    Input(component_id="viz_dists", component_property="value"),
)
def render_tab_2(tab_choice):
    """Renders the selected subtab's layout

    Args:
        tab_choice (str): selected subtab

    Returns:
        selected subtab's layout
    """
    if tab_choice == "normdist":
        return normDistLayout()
    if tab_choice == "poissondist":
        return poissonDistLayout()
    if tab_choice == "binomdist":
        return binomialDistLayout()
    if tab_choice == "uniformdist":
        return uniformDistLayout()


#######################################
# Normal Distribution Layout
#######################################
def normDistLayout():
    distributionLayout = html.Div(
        [
            html.H4("Visualizing Normal Distributions"),
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("No of samples to generate:"),
                            dcc.Slider(
                                id="n_samples_norm",
                                min=1,
                                max=1000,
                                value=150,
                                marks={data: str(data) for data in range(0, 1000, 50)},
                                step=100,
                            ),
                            html.H4("No of bins to generate:"),
                            dcc.Slider(
                                id="bins_desired_norm",
                                min=2,
                                max=100,
                                value=2,
                                marks={data: str(data) for data in range(0, 100, 10)},
                                step=10,
                            ),
                            html.Br(),
                            html.H4("Choose an appropriate Mean:"),
                            dcc.Slider(
                                id="mean_norm",
                                min=-10,
                                max=10,
                                value=0,
                                marks={data: str(data) for data in range(-10, 10, 1)},
                                step=1,
                            ),
                            html.Br(),
                            html.H4("Choose an appropriate Standard Deviation:"),
                            dcc.Slider(
                                id="sd_norm",
                                min=0,
                                max=10,
                                value=0.1,
                                marks={data: str(data) for data in range(0, 10, 1)},
                                step=0.1,
                            ),
                        ],
                        className="grouped-sliders",
                    ),
                    html.Div(
                        [
                            html.Br(),
                            html.Strong(
                                "Histogram of the value-spread of the Normal distribution"
                            ),
                            dcc.Graph(id="normal-dist"),
                        ],
                        className="grouped-graphs",
                    ),
                ],
                className="graphs-and-sliders",
            ),
            dcc.Markdown(
                id="norm_block_md",
                children=read_file_as_str(
                    "./utils/markdown/tab_2/code_markdown_norm.md"
                ),
                className="code-markdown-view",
                mathjax=True,
            ),
            html.Button(
                "Download Code", id="btn-download-norm", className="btn-download"
            ),
            dcc.Download(id="download-norm"),
        ]
    )

    return distributionLayout


#######################################
# Normal Distribution Callbacks
#######################################
@my_app.callback(
    Output(component_id="normal-dist", component_property="figure"),
    Input(component_id="n_samples_norm", component_property="value"),
    Input(component_id="bins_desired_norm", component_property="value"),
    Input(component_id="mean_norm", component_property="value"),
    Input(component_id="sd_norm", component_property="value"),
)
def render_normal_dist(n_samples, bins, mean_norm, sd_norm):
    dist = np.random.normal(mean_norm, sd_norm, n_samples)
    axis_dict = dict(mirror=True, ticks="outside", showline=True, title="")
    fig = px.histogram(dist, nbins=bins, template="simple_white")
    fig.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    return fig


@my_app.callback(
    Output("download-norm", "data"),
    Input("btn-download-norm", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file("./utils/download_codes/tab_2/normal_gen.py")


#######################################
# Poisson Distribution Layout
#######################################
def poissonDistLayout():
    distributionLayout = html.Div(
        [
            html.H4("Visualizing Poisson Distributions"),
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("No of samples to generate:"),
                            dcc.Slider(
                                id="n_samples_poisson",
                                min=1,
                                max=1000,
                                value=150,
                                marks={data: str(data) for data in range(0, 1000, 50)},
                                step=100,
                            ),
                            html.H4("No of bins to generate:"),
                            dcc.Slider(
                                id="bins_desired_poisson",
                                min=2,
                                max=100,
                                value=10,
                                marks={data: str(data) for data in range(0, 100, 10)},
                                step=1,
                            ),
                            html.Br(),
                            html.H4("Choose an appropriate Lambda (Rate of Events):"),
                            dcc.Slider(
                                id="lambda",
                                min=0,
                                max=50,
                                value=1,
                                marks={data: str(data) for data in range(0, 50, 5)},
                                step=1,
                            ),
                        ],
                        className="grouped-sliders",
                    ),
                    html.Div(
                        [
                            html.Br(),
                            html.Strong(
                                "Histogram of the value-spread of the Poisson distribution"
                            ),
                            dcc.Graph(id="poisson-dist"),
                        ],
                        className="grouped-graphs",
                    ),
                ],
                className="graphs-and-sliders",
            ),
            dcc.Markdown(
                id="poisson_block_md",
                children=read_file_as_str(
                    "./utils/markdown/tab_2/code_markdown_poisson.md"
                ),
                className="code-markdown-view",
                mathjax=True,
            ),
            html.Button(
                "Download Code", id="btn-download-poisson", className="btn-download"
            ),
            dcc.Download(id="download-poisson"),
        ]
    )

    return distributionLayout


#######################################
# Poisson Distribution Callbacks
#######################################
@my_app.callback(
    Output(component_id="poisson-dist", component_property="figure"),
    Input(component_id="n_samples_poisson", component_property="value"),
    Input(component_id="bins_desired_poisson", component_property="value"),
    Input(component_id="lambda", component_property="value"),
)
def render_poisson_dist(n_samples, bins, lambdaPoisson):
    dist = np.random.poisson(lambdaPoisson, n_samples)
    axis_dict = dict(mirror=True, ticks="outside", showline=True, title="")
    fig = px.histogram(dist, nbins=bins, template="simple_white")
    fig.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    return fig


@my_app.callback(
    Output("download-poisson", "data"),
    Input("btn-download-poisson", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file("./utils/download_codes/tab_2/poisson_gen.py")


#######################################
# Uniform Distribution Layout
#######################################
def uniformDistLayout():
    distributionLayout = html.Div(
        [
            html.H4("Visualizing binomial Distributions"),
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("No of samples to generate:"),
                            dcc.Slider(
                                id="n_samples_uni",
                                min=1,
                                max=1000,
                                value=150,
                                marks={data: str(data) for data in range(0, 1000, 50)},
                                step=100,
                            ),
                            html.H4("No of bins to generate:"),
                            dcc.Slider(
                                id="bins_desired_uni",
                                min=2,
                                max=100,
                                value=2,
                                marks={data: str(data) for data in range(0, 100, 10)},
                                step=10,
                            ),
                            html.Br(),
                            html.H4("Choose an appropriate low value:"),
                            dcc.Slider(
                                id="un_low",
                                min=0,
                                max=100,
                                value=0,
                                marks={data: str(data) for data in range(0, 100, 5)},
                                step=0.1,
                            ),
                            html.Br(),
                            html.H4("Choose an appropriate high value:"),
                            dcc.Slider(
                                id="un_high",
                                min=0,
                                max=100,
                                value=1,
                                marks={data: str(data) for data in range(0, 100, 5)},
                                step=0.1,
                            ),
                        ],
                        className="grouped-sliders",
                    ),
                    html.Div(
                        [
                            html.Br(),
                            html.Strong(
                                "Histogram of the value-spread of the uniform distribution"
                            ),
                            dcc.Graph(id="uni-dist"),
                        ],
                        className="grouped-graphs",
                    ),
                ],
                className="graphs-and-sliders",
            ),
            dcc.Markdown(
                id="uni_block_md",
                children=read_file_as_str(
                    "./utils/markdown/tab_2/code_markdown_uniform.md"
                ),
                className="code-markdown-view",
                mathjax=True,
            ),
            html.Button(
                "Download Code", id="btn-download-uni", className="btn-download"
            ),
            dcc.Download(id="download-uni"),
        ]
    )

    return distributionLayout


#######################################
# Uniform Distribution Callbacks
#######################################
@my_app.callback(
    Output(component_id="uni-dist", component_property="figure"),
    Output(component_id="un_high", component_property="min"),
    Input(component_id="n_samples_uni", component_property="value"),
    Input(component_id="bins_desired_uni", component_property="value"),
    Input(component_id="un_high", component_property="value"),
    Input(component_id="un_low", component_property="value"),
)
def render_uniform_dist(n_samples, bins, high, low):
    dist = np.random.uniform(low, high, n_samples)
    axis_dict = dict(mirror=True, ticks="outside", showline=True, title="")
    fig = px.histogram(dist, nbins=bins, template="simple_white")
    fig.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)

    return fig, low


@my_app.callback(
    Output("download-uni", "data"),
    Input("btn-download-uni", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file("./utils/download_codes/tab_2/uniform_gen.py")


#######################################
# Binomial Distribution Layout
#######################################
def binomialDistLayout():
    distributionLayout = html.Div(
        [
            html.H4("Visualizing binomial Distributions"),
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("No of samples to generate:"),
                            dcc.Slider(
                                id="n_samples_binom",
                                min=1,
                                max=1000,
                                value=150,
                                marks={data: str(data) for data in range(0, 1000, 50)},
                                step=100,
                            ),
                            html.H4(
                                "Choose an appropriate Number of events in each trial(n):"
                            ),
                            dcc.Slider(
                                id="trials",
                                min=0,
                                max=50,
                                value=3,
                                marks={data: str(data) for data in range(0, 50, 5)},
                                step=1,
                            ),
                            html.Br(),
                            html.H4("Choose an appropriate chance of success (p):"),
                            dcc.Slider(
                                id="p_binom",
                                min=0,
                                max=1,
                                value=0.1,
                                marks={
                                    data: str(float(data) // 10)
                                    for data in range(0, 10, 1)
                                },
                                step=0.1,
                            ),
                        ],
                        className="grouped-sliders",
                    ),
                    html.Div(
                        [
                            html.Br(),
                            html.Strong(
                                "Histogram of the value-spread of the binomial distribution"
                            ),
                            dcc.Graph(id="binom-dist"),
                        ],
                        className="grouped-graphs",
                    ),
                ],
                className="graphs-and-sliders",
            ),
            dcc.Markdown(
                id="binom_block_md",
                children=read_file_as_str(
                    "./utils/markdown/tab_2/code_markdown_binom.md"
                ),
                className="code-markdown-view",
                mathjax=True,
            ),
            html.Button(
                "Download Code", id="btn-download-binom", className="btn-download"
            ),
            dcc.Download(id="download-binom"),
        ]
    )

    return distributionLayout


#######################################
# Binomial Distribution Callbacks
#######################################
@my_app.callback(
    Output(component_id="binom-dist", component_property="figure"),
    Input(component_id="n_samples_binom", component_property="value"),
    Input(component_id="trials", component_property="value"),
    Input(component_id="p_binom", component_property="value"),
)
def render_binom_dist(n_samples, trials, p):
    dist = np.random.binomial(trials, p, n_samples)
    axis_dict = dict(mirror=True, ticks="outside", showline=True, title="")
    fig = px.histogram(dist, nbins=trials, template="simple_white")
    fig.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    return fig


@my_app.callback(
    Output("download-binom", "data"),
    Input("btn-download-binom", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file("./utils/download_codes/tab_2/binom_gen.py")
