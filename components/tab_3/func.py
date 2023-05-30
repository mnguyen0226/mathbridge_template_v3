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
from utils.ml import coor_gen
from utils.others.file_operations import read_file_as_str
from utils.stats.non_linear import square
from utils.stats.non_linear import cube
from utils.stats.non_linear import poly
from utils.stats.non_linear import log


#######################################
# Dash Layout
#######################################
def func_layout():
    tabs = html.Div(
        [
            dbc.Tabs(
                id="viz_funcs",
                children=[
                    dbc.Tab(
                        label="Nonlinear",
                        tab_id="visualization",
                    ),
                    dbc.Tab(
                        label="Derivatives",
                        tab_id="derivatives",
                    ),
                ],
                active_tab="visualization",
            ),
            html.Br(),
            html.Div(id="layout_tab4"),
        ]
    )
    return tabs


#######################################
# Dash Callbacks
#######################################
@my_app.callback(
    Output(component_id="layout_tab4", component_property="children"),
    Input(component_id="viz_funcs", component_property="active_tab"),
)
def Tab4Render(ques):
    if ques == "visualization":
        return functionVizLayout()
        # tab1_sel1_layout

    if ques == "derivatives":
        return functionDerivativeLayout()


#######################################
# Visualization Layout
#######################################
def functionVizLayout():
    tab4Layout = html.Div(
        [
            html.H3("Nonlinear Functions Visualization"),
            html.Br(),
            dbc.Label("X range"),
            dcc.RangeSlider(
                min=-20,
                max=20,
                step=1,
                value=[-10, 10],
                marks={data: str(data) for data in range(-20, 20, 2)},
                id="range_x",
            ),
            html.Br(),
            dbc.Label("Select function"),
            dcc.Dropdown(
                id="function-selection",
                options=[
                    {"label": "x^2", "value": 1},
                    {"label": "x^3", "value": 2},
                    {"label": "x^4", "value": 3},
                    {"label": "e^x", "value": 4},
                    {"label": "log(x)", "value": 5},
                ],
                value=1,
                clearable=False,
            ),
            html.Br(),
            html.Hr(),
            html.Strong("Plot of the Function"),
            dcc.Graph(id="function-plot"),
            html.Hr(),
        ]
    )
    return tab4Layout


#######################################
# Visualization Callbacks
#######################################
@my_app.callback(
    Output(component_id="function-plot", component_property="figure"),
    [Input("range_x", "value")],
    Input(component_id="function-selection", component_property="value"),
)
def plotFunctions(range_x, function_selected):
    # print(range_x,function_selected)
    X = np.linspace(range_x[0], range_x[1], 1000, endpoint=True)
    axis_dict = dict(mirror=True, ticks="outside", showline=True, title="")
    if function_selected == 1:
        Y = X**2
        fig = px.line(x=X, y=Y, template="simple_white")
        fig.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    elif function_selected == 2:
        Y = X**3
        fig = px.line(x=X, y=Y, template="simple_white")
        fig.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    elif function_selected == 3:
        Y = X**4
        fig = px.line(x=X, y=Y, template="simple_white")
        fig.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    elif function_selected == 4:
        Y = np.exp(X)
        fig = px.line(x=X, y=Y, template="simple_white")
        fig.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    elif function_selected == 5:
        clipped_X = X[X > 0]
        Y = np.log(clipped_X)
        Y = np.nan_to_num(Y)
        fig = px.line(x=clipped_X, y=Y, template="simple_white")
        fig.update_layout(xaxis=axis_dict, yaxis=axis_dict, showlegend=False)
    else:
        return "The impaler"
    return fig


#######################################
# Derivatives Layout
#######################################
def functionDerivativeLayout():
    tab5Layout = [
        html.H3("Function Derivatives Visualization"),
        html.Br(),
        dbc.Label("Select function"),
        dcc.Dropdown(
            options=[
                {"label": "f(x)=x^2", "value": "square"},
                {"label": "f(x)=x^3", "value": "cube"},
                {"label": "f(x)=2x^2+4", "value": "poly"},
                {"label": "f(x)=log(x)", "value": "log"},
            ],
            value="square",
            id="fn-select-grad",
        ),
        html.Br(),
        html.Hr(),
        html.Strong("Original Function"),
        dcc.Graph(id="functions-graph"),
        html.Br(),
        html.Strong("Function Derivative Graphed"),
        dcc.Graph(id="derivative-graph"),
        html.Hr(),
        html.H3("Source Code"),
        html.Br(),
        dcc.Markdown(
            id="binom_block_md",
            children=read_file_as_str(
                "./utils/markdown/tab_3/code_markdown_derivatives.md"
            ),
            mathjax=True,
        ),
        dbc.Button(
            "Download Code",
            color="success",
            className="me-1",
            id="btn-download-derivatives",
        ),
        dcc.Download(id="download-derivatives"),
        html.Hr(),
    ]

    return tab5Layout


#######################################
# Derivatives Callbacks
#######################################
@my_app.callback(
    Output(component_id="functions-graph", component_property="figure"),
    Output(component_id="derivative-graph", component_property="figure"),
    Input(component_id="fn-select-grad", component_property="value"),
)
def plotDerivatives(selection):
    x = np.linspace(-10, 10, 1000)
    if selection == "square":
        fx = x**2
        dfxdx = coor_gen.generatedydx(x, square)
        a = px.line(x=x, y=fx, template="simple_white", title="f(x)=x^2")
        b = px.line(x=x, y=dfxdx, template="simple_white", title="f(x)=2x")
        return a, b
    if selection == "cube":
        fx = x**3
        dfxdx = coor_gen.generatedydx(x, cube)
        a = px.line(x=x, y=fx, template="simple_white", title="f(x)=x^3")
        b = px.line(x=x, y=dfxdx, template="simple_white", title="f(x)=3x^2")
        return a, b
    if selection == "poly":
        fx = 2 * (x**2) + 4
        dfxdx = coor_gen.generatedydx(x, poly)
        a = px.line(x=x, y=fx, template="simple_white", title="f(x)=2x^2+4")
        b = px.line(x=x, y=dfxdx, template="simple_white", title="f(x)=4x")
        return a, b
    if selection == "log":
        x = np.linspace(1, 10, 1000)
        fx = np.log(x)
        dfxdx = coor_gen.generatedydx(x, log)
        a = px.line(x=x, y=fx, template="simple_white", title="f(x)=log(x)")
        b = px.line(x=x, y=dfxdx, template="simple_white", title="f(x)=(1/x)")
        return a, b
    return "", ""


@my_app.callback(
    Output("download-derivatives", "data"),
    Input("btn-download-derivatives", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_file("./utils/download_codes/tab_3/derivatives_gen.py")
