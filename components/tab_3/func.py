from dash import dcc
from dash import html
import numpy as np
from maindash import my_app
from dash.dependencies import Input, Output
import plotly.express as px
from utils.ml import coor_gen


def readFileasStr(filename):
    with open(filename, "r") as file:
        data = file.read()
    return data


def func_layout():
    tab4Layout = html.Div(
        [
            dcc.Tabs(
                id="viz_funcs",
                children=[
                    dcc.Tab(label="Visualization", value="visualization"),
                    dcc.Tab(label="Derivatives", value="derivatives"),
                ],
                value="visualization",
            ),
            html.Div(id="layout_tab4"),
        ]
    )
    return tab4Layout


def functionVizLayout():
    tab4Layout = html.Div(
        [
            html.H4("Visualizing Functions"),
            html.Div(
                [
                    html.Div(
                        [
                            html.H4("X-Range"),
                            dcc.RangeSlider(
                                min=-20,
                                max=20,
                                step=1,
                                value=[-10, 10],
                                marks={data: str(data) for data in range(-20, 20, 2)},
                                id="range_x",
                            ),
                            # html.H4("Y-Range:"),
                            # dcc.RangeSlider(min=-100, max=100, step=1, value=[-10, 10],
                            #                 marks={data: str(data) for data in range(-10, 10, 2)},
                            #                 id='range_y'),
                            html.H4("Select function"),
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
                        ],
                        className="grouped-sliders",
                    ),
                    html.Div(
                        [
                            html.Br(),
                            html.Strong("Plot of the Function"),
                            dcc.Graph(id="function-plot"),
                        ],
                        className="grouped-graphs",
                    ),
                ],
                className="graphs-and-sliders",
            ),
        ]
    )
    return tab4Layout


##############################3
def functionDerivativeLayout():
    tab5Layout = [
        html.H4("Visualizing Derivatives"),
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
        html.Div(
            [
                html.Div(
                    [html.Strong("Original Function"), dcc.Graph(id="functions-graph")],
                    className="grouped-graphs",
                ),
                html.Div(
                    [
                        html.Strong("Function Derivative Graphed"),
                        dcc.Graph(id="derivative-graph"),
                    ],
                    className="grouped-graphs",
                ),
            ],
            className="row-pane",
        ),
        dcc.Markdown(
            id="binom_block_md",
            children=readFileasStr(
                "./utils/markdown/tab_3/code_markdown_derivatives.md"
            ),
            className="code-markdown-view",
            mathjax=True,
        ),
        html.Button(
            "Download Code", id="btn-download-derivatives", className="btn-download"
        ),
        dcc.Download(id="download-derivatives"),
    ]

    return tab5Layout


@my_app.callback(
    Output(component_id="layout_tab4", component_property="children"),
    Input(component_id="viz_funcs", component_property="value"),
)
def Tab4Render(ques):
    if ques == "visualization":
        return functionVizLayout()
        # tab1_sel1_layout

    if ques == "derivatives":
        return functionDerivativeLayout()
    return "The impaler!!!!"


# Function Plotted Visualization Callback
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


# Function Plot Derivative Callbacks
def square(x):
    return x**2


def cube(x):
    return x**3


def poly(x):
    return 2 * (x**2) + 4


def log(x):
    return np.log(x)


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
