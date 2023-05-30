# dash imports
from dash import dcc
from dash import html
from dash import Input
from dash import Output
import dash_bootstrap_components as dbc
from dash import State

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
    tabs = html.Div(
        [
            dbc.Tabs(
                id="viz_dists",
                children=[
                    dbc.Tab(
                        label="Normal",
                        tab_id="normdist",
                    ),
                    dbc.Tab(
                        label="Poisson",
                        tab_id="poissondist",
                    ),
                    dbc.Tab(
                        label="Uniform",
                        tab_id="uniformdist",
                    ),
                    dbc.Tab(
                        label="Binomial",
                        tab_id="binomdist",
                    ),
                ],
                active_tab="normdist",
            ),
            html.Br(),
            html.Div(id="layout_tab3"),
        ]
    )
    return tabs


#######################################
# Dash Callbacks
#######################################
@my_app.callback(
    Output(component_id="layout_tab3", component_property="children"),
    Input(component_id="viz_dists", component_property="active_tab"),
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
            html.H3("Normal Distribution Visualization"),
            html.Br(),
            dbc.Label("Number of samples to generate"),
            dcc.Slider(
                id="n_samples_norm",
                min=1,
                max=1000,
                value=150,
                marks={data: str(data) for data in range(0, 1000, 50)},
                step=100,
            ),
            html.Br(),
            dbc.Label("Number of bins to generate"),
            dcc.Slider(
                id="bins_desired_norm",
                min=2,
                max=100,
                value=2,
                marks={data: str(data) for data in range(0, 100, 10)},
                step=10,
            ),
            html.Br(),
            dbc.Label("Choose an appropriate mean"),
            dcc.Slider(
                id="mean_norm",
                min=-10,
                max=10,
                value=0,
                marks={data: str(data) for data in range(-10, 10, 1)},
                step=1,
            ),
            html.Br(),
            dbc.Label("Choose an appropriate standard deviation"),
            dcc.Slider(
                id="sd_norm",
                min=0,
                max=10,
                value=0.1,
                marks={data: str(data) for data in range(0, 10, 1)},
                step=0.1,
            ),
            html.Br(),
            html.Hr(),
            html.Strong("Histogram of the value-spread of the Normal Distribution"),
            dcc.Graph(id="normal-dist"),
            html.Hr(),
            html.H3("Source Code"),
            html.Br(),
            dbc.Label(
                "Normal distributions can generate a bell curve like distribution given a mean and standard deviation."
            ),
            dbc.Label(
                "The code below generates a normal distribution in Python, try running it to get a feel for this distribution."
            ),
            html.Div(
                [
                    dbc.Button(
                        "View Code",
                        id="collapse-button",
                        className="mb-3",
                        color="primary",
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        dcc.Markdown(
                            id="norm_block_md",
                            children=read_file_as_str(
                                "./utils/markdown/tab_2/code_markdown_norm.md"
                            ),
                            mathjax=True,
                        ),
                        id="collapse",
                        is_open=False,
                    ),
                ]
            ),
            dbc.Button(
                "Download Code",
                color="success",
                className="me-1",
                id="btn-download-norm",
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


@my_app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


#######################################
# Poisson Distribution Layout
#######################################
def poissonDistLayout():
    distributionLayout = html.Div(
        [
            html.H3("Poisson Distribution Visualization"),
            html.Br(),
            dbc.Label("Number of samples to generate"),
            dcc.Slider(
                id="n_samples_poisson",
                min=1,
                max=1000,
                value=150,
                marks={data: str(data) for data in range(0, 1000, 50)},
                step=100,
            ),
            html.Br(),
            dbc.Label("Number of bins to generate"),
            dcc.Slider(
                id="bins_desired_poisson",
                min=2,
                max=100,
                value=10,
                marks={data: str(data) for data in range(0, 100, 10)},
                step=1,
            ),
            html.Br(),
            dbc.Label("Choose an appropriate Lambda (Rate of Events):"),
            dcc.Slider(
                id="lambda",
                min=0,
                max=50,
                value=1,
                marks={data: str(data) for data in range(0, 50, 5)},
                step=1,
            ),
            html.Br(),
            html.Hr(),
            html.Strong("Histogram of the value-spread of the Poisson Distribution"),
            dcc.Graph(id="poisson-dist"),
            html.Hr(),
            html.H3("Source Code"),
            html.Br(),
            dbc.Label(
                "Poisson Distribution estimates the number of times an event may occur at every instance of time, given a rate of occurence $\lambda$."
            ),
            dbc.Label(
                "The code below generates a Poisson distribution in Python, try running it to get a feel for this distribution."
            ),
            html.Div(
                [
                    dbc.Button(
                        "View Code",
                        id="collapse-button",
                        className="mb-3",
                        color="primary",
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        dcc.Markdown(
                            id="poisson_block_md",
                            children=read_file_as_str(
                                "./utils/markdown/tab_2/code_markdown_poisson.md"
                            ),
                            mathjax=True,
                        ),
                        id="collapse",
                        is_open=False,
                    ),
                ]
            ),
            dbc.Button(
                "Download Code",
                color="success",
                className="me-1",
                id="btn-download-poisson",
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
            html.H3("Uniform Distribution Visualization"),
            html.Br(),
            dbc.Label("Number of samples to generate"),
            dcc.Slider(
                id="n_samples_uni",
                min=1,
                max=1000,
                value=150,
                marks={data: str(data) for data in range(0, 1000, 50)},
                step=100,
            ),
            html.Br(),
            dbc.Label("Number of bins to generate"),
            dcc.Slider(
                id="bins_desired_uni",
                min=2,
                max=100,
                value=2,
                marks={data: str(data) for data in range(0, 100, 10)},
                step=10,
            ),
            html.Br(),
            dbc.Label("Choose an appropriate low value"),
            dcc.Slider(
                id="un_low",
                min=0,
                max=100,
                value=0,
                marks={data: str(data) for data in range(0, 100, 5)},
                step=0.1,
            ),
            html.Br(),
            dbc.Label("Choose an appropriate high value:"),
            dcc.Slider(
                id="un_high",
                min=0,
                max=100,
                value=1,
                marks={data: str(data) for data in range(0, 100, 5)},
                step=0.1,
            ),
            html.Br(),
            html.Hr(),
            html.Strong("Histogram of the value-spread of the uniform distribution"),
            dcc.Graph(id="uni-dist"),
            html.Hr(),
            html.H3("Source Code"),
            html.Br(),
            dbc.Label(
                "Uniform distribution gives an uniformly distributed set of values within a lower bound and upper bound for a specified number of samples."
            ),
            dbc.Label(
                "The code below generates a Uniform distribution in Python, try running it to get a feel for this distribution."
            ),
            html.Div(
                [
                    dbc.Button(
                        "View Code",
                        id="collapse-button",
                        className="mb-3",
                        color="primary",
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        dcc.Markdown(
                            id="uni_block_md",
                            children=read_file_as_str(
                                "./utils/markdown/tab_2/code_markdown_uniform.md"
                            ),
                            mathjax=True,
                        ),
                        id="collapse",
                        is_open=False,
                    ),
                ]
            ),
            dbc.Button(
                "Download Code",
                color="success",
                className="me-1",
                id="btn-download-uni",
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
            html.H3("Binomial Distribution Visualization"),
            html.Br(),
            dbc.Label("Number of samples to generate"),
            dcc.Slider(
                id="n_samples_binom",
                min=1,
                max=1000,
                value=150,
                marks={data: str(data) for data in range(0, 1000, 50)},
                step=100,
            ),
            html.Br(),
            dbc.Label("Choose an appropriate Number of events in each trial(n)"),
            dcc.Slider(
                id="trials",
                min=0,
                max=50,
                value=3,
                marks={data: str(data) for data in range(0, 50, 5)},
                step=1,
            ),
            html.Br(),
            dbc.Label("Choose an appropriate chance of success (p):"),
            dcc.Slider(
                id="p_binom",
                min=0,
                max=1,
                value=0.1,
                marks={data: str(float(data) // 10) for data in range(0, 10, 1)},
                step=0.1,
            ),
            html.Br(),
            html.Hr(),
            html.Strong("Histogram of the value-spread of the binomial distribution"),
            dcc.Graph(id="binom-dist"),
            html.Hr(),
            html.H3("Source Code"),
            html.Br(),
            dbc.Label(
                "Binomial Distribution generates a distribution of successes of events, given that an event has n outcomes, and p probability of success."
            ),
            dbc.Label(
                "The code below generates a Binomial distribution in Python, try running it to get a feel for this distribution."
            ),
            html.Div(
                [
                    dbc.Button(
                        "View Code",
                        id="collapse-button",
                        className="mb-3",
                        color="primary",
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        dcc.Markdown(
                            id="binom_block_md",
                            children=read_file_as_str(
                                "./utils/markdown/tab_2/code_markdown_binom.md"
                            ),
                            mathjax=True,
                        ),
                        id="collapse",
                        is_open=False,
                    ),
                ]
            ),
            dbc.Button(
                "Download Code",
                color="success",
                className="me-1",
                id="btn-download-binom",
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
