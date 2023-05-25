from dash import dcc
from dash import html
import plotly.express as px
import numpy as np
import math
from maindash import my_app
from dash.dependencies import Input, Output
import math, json

import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots


def readFileasStr(filename):
    with open(filename, "r") as file:
        data = file.read()
    return data


def eigen_layout():
    tab5Layout = html.Div(
        [
            html.H3("Visualizing Eigen Vector & Eigen Values"),
            # add markdown
            dcc.Markdown(
                id="code-markdown-eigen", className="markdown-view", mathjax=True
            ),
            # set matrix example
            # set input value for matrix
            html.Div(
                [
                    html.H4("A"),
                    dcc.Input(
                        id="first_val",
                        type="number",
                        value=3,
                        className="standard-gen-ip",
                    ),
                ],
                className="grouped-label-class",
            ),
            html.Div(
                [
                    html.H4("B"),
                    dcc.Input(
                        id="second_val",
                        type="number",
                        value=0,
                        className="standard-gen-ip",
                    ),
                ],
                className="grouped-label-class",
            ),
            html.Div(
                [
                    html.H4("C"),
                    dcc.Input(
                        id="third_val",
                        type="number",
                        value=1,
                        className="standard-gen-ip",
                    ),
                ],
                className="grouped-label-class",
            ),
            html.Div(
                [
                    html.H4("D"),
                    dcc.Input(
                        id="fourth_val",
                        type="number",
                        value=2,
                        className="standard-gen-ip",
                    ),
                ],
                className="grouped-label-class",
            ),
            html.Div(
                [
                    html.H4("Calculated Eigen Value 1"),
                    html.Plaintext(children="text", id="eigen-val-output1"),
                ],
                className="grouped-label-class",
            ),
            html.Div(
                [
                    html.H4("Calculated Eigen Value 2"),
                    html.Plaintext(children="text", id="eigen-val-output2"),
                ],
                className="grouped-label-class",
            ),
            html.Div(
                [
                    html.H4("Eigen Vectors & Transformation"),
                ],
                className="grouped-label-class",
            ),
            html.Div(
                [
                    # set hook for input graph
                    dcc.Graph(id="eigen-origin"),
                    # set hook for transformation graph
                    dcc.Graph(id="eigen-transform"),
                ],
                className="grouped-label-class-horizontal",
            ),
            html.Div(
                [
                    html.H4("Transformation Animation"),
                ],
                className="grouped-label-class",
            ),
            # # set hook for graph
            dcc.Graph(id="eigen-play"),
        ]
    )
    return tab5Layout


selected_points = []


@my_app.callback(
    Output(component_id="eigen-val-output1", component_property="children"),
    Output(component_id="eigen-val-output2", component_property="children"),
    Output(component_id="eigen-origin", component_property="figure"),
    Output(component_id="eigen-transform", component_property="figure"),
    Output(component_id="eigen-play", component_property="figure"),
    Output(component_id="code-markdown-eigen", component_property="children"),
    Input(component_id="first_val", component_property="value"),
    Input(component_id="second_val", component_property="value"),
    Input(component_id="third_val", component_property="value"),
    Input(component_id="fourth_val", component_property="value"),
)
def record_coords(A, B, C, D):
    n = m = 10
    # set up  the lists  of  vertical line x and y-end coordinates

    xv = []
    yv = []
    for k in range(-n, n + 1):
        xv.extend([k, k, np.nan])
        yv.extend([-m, m, np.nan])

    # set up  the lists  of  horizontal line x and y-end coordinates

    xh = []
    yh = []
    for k in range(-m, m + 1):
        xh.extend([-m, m, np.nan])
        yh.extend([k, k, np.nan])

    x = np.array(xv + xh)
    y = np.array(yv + yh)

    # Linear transformation
    T = np.array([[A, B], [C, D]], dtype=float)
    eigenvalues, eigenvectors = np.linalg.eig(T)
    print(f"Matrix: \n{T}\n ")
    print("Eigenvectors: \n%s" % eigenvectors)
    print("\nEigenvalues: \n%s" % eigenvalues)

    xy = np.stack((x, y))
    xy_T = T.T @ xy

    # calculated eigen values
    cal_eigen_val1 = eigenvalues[0]
    cal_eigen_val2 = eigenvalues[1]

    fig1 = go.Figure(
        data=[
            go.Scatter(x=x, y=y, line_width=1),
            # go.Scatter(x=x, y=y, line_width=1, line=dict(color='silver')),
            go.Scatter(
                x=[0, 1], y=[0, 0], line_width=3, line=dict(color="red")
            ),  # i=[1,0]
            go.Scatter(
                x=[0, 0], y=[0, 1], line_width=3, line=dict(color="red")
            ),  # j=[0,1]
            go.Scatter(
                x=[0, (-eigenvalues[0] * eigenvectors[1, 0])],
                y=[0, (eigenvalues[0] * eigenvectors[0, 0])],
                line_width=3,
                line=dict(color="gold"),
            ),
            go.Scatter(
                x=[0, (-eigenvalues[1] * eigenvectors[1, 1])],
                y=[0, (eigenvalues[1] * eigenvectors[0, 1])],
                line_width=3,
                line=dict(color="gold"),
            ),
        ],
        layout=go.Layout(
            showlegend=False,
            xaxis=dict(range=[-n, n], autorange=False),
            yaxis=dict(range=[-m, m], autorange=False),
            width=500,
            height=500,
            updatemenus=[
                dict(
                    type="buttons",
                    # buttons=[dict(label="Play",method="animate",args=[None])]
                )
            ],
        ),
    )

    fig2 = go.Figure(
        # init data
        data=[
            go.Scatter(x=xy_T[0], y=xy_T[1], line_width=1),
            # go.Scatter(x=x, y=y, line_width=1, line=dict(color='silver')),
            go.Scatter(
                x=[0, T[0][0]], y=[0, T[0][1]], line_width=3, line=dict(color="red")
            ),  # i=[3,-2]
            go.Scatter(
                x=[0, T[1][0]], y=[0, T[1][1]], line_width=3, line=dict(color="red")
            ),  # j=[2,1]
            go.Scatter(
                x=[0, (-eigenvalues[0] * eigenvectors[1, 0]) * eigenvalues[1]],
                y=[0, (eigenvalues[0] * eigenvectors[0, 0]) * eigenvalues[1]],
                line_width=3,
                line=dict(color="gold"),
            ),
            go.Scatter(
                x=[0, (-eigenvalues[1] * eigenvectors[1, 1]) * eigenvalues[0]],
                y=[0, (eigenvalues[1] * eigenvectors[0, 1]) * eigenvalues[0]],
                line_width=3,
                line=dict(color="gold"),
            ),
        ],
        layout=go.Layout(
            showlegend=False,
            xaxis=dict(range=[-n, n], autorange=False),
            yaxis=dict(range=[-m, m], autorange=False),
            width=500,
            height=500,
            updatemenus=[
                dict(
                    type="buttons",
                    # buttons=[dict(label="Play",method="animate",args=[None])]
                )
            ],
        ),
    )

    fig3 = go.Figure(
        # init data
        data=[
            go.Scatter(x=x, y=y, line_width=1),
            # go.Scatter(x=x, y=y, line_width=1, line=dict(color='silver')),
            go.Scatter(x=[0, 0.01], y=[0, 0], line_width=3, line=dict(color="red")),
            go.Scatter(x=[0, 0], y=[0, 0.01], line_width=3, line=dict(color="red")),
            # eigen vector
            go.Scatter(x=[0, 0], y=[0, 0.01], line_width=3, line=dict(color="gold")),
            go.Scatter(x=[0, 0], y=[0, 0.01], line_width=3, line=dict(color="gold")),
        ],
        layout=go.Layout(
            showlegend=False,
            xaxis=dict(range=[-n, n], autorange=False),
            yaxis=dict(range=[-m, m], autorange=False),
            width=500,
            height=500,
            updatemenus=[
                dict(
                    type="buttons",
                    buttons=[dict(label="Play", method="animate", args=[None])],
                )
            ],
        ),
        # init frames
        frames=[
            # init point
            go.Frame(
                data=[
                    go.Scatter(x=x, y=y, line_width=1),
                    # go.Scatter(x=x, y=y, line_width=1, line=dict(color='silver')),
                    go.Scatter(
                        x=[0, 0.01], y=[0, 0], line_width=3, line=dict(color="red")
                    ),
                    go.Scatter(
                        x=[0, 0], y=[0, 0.01], line_width=3, line=dict(color="red")
                    ),
                    go.Scatter(
                        x=[0, 0], y=[0, 0.01], line_width=3, line=dict(color="gold")
                    ),
                    go.Scatter(
                        x=[0, 0], y=[0, 0.01], line_width=3, line=dict(color="gold")
                    ),
                ]
            ),
            # draw line
            go.Frame(
                data=[
                    go.Scatter(x=x, y=y, line_width=1),
                    # go.Scatter(x=x, y=y, line_width=1, line=dict(color='silver')),
                    go.Scatter(
                        x=[0, 1], y=[0, 0], line_width=3, line=dict(color="red")
                    ),  # i=[1,0]
                    go.Scatter(
                        x=[0, 0], y=[0, 1], line_width=3, line=dict(color="red")
                    ),  # j=[0,1]
                    go.Scatter(
                        x=[0, (-eigenvalues[0] * eigenvectors[1, 0])],
                        y=[0, (eigenvalues[0] * eigenvectors[0, 0])],
                        line_width=3,
                        line=dict(color="gold"),
                    ),
                    go.Scatter(
                        x=[0, (-eigenvalues[1] * eigenvectors[1, 1])],
                        y=[0, (eigenvalues[1] * eigenvectors[0, 1])],
                        line_width=3,
                        line=dict(color="gold"),
                    ),
                ]
            ),
            # do the transformation
            go.Frame(
                data=[
                    go.Scatter(x=xy_T[0], y=xy_T[1], line_width=1),
                    # go.Scatter(x=x, y=y, line_width=1, line=dict(color='silver')),
                    go.Scatter(
                        x=[0, T[0][0]],
                        y=[0, T[0][1]],
                        line_width=3,
                        line=dict(color="red"),
                    ),  # i=[3,-2]
                    go.Scatter(
                        x=[0, T[1][0]],
                        y=[0, T[1][1]],
                        line_width=3,
                        line=dict(color="red"),
                    ),  # j=[2,1]
                    go.Scatter(
                        x=[0, (-eigenvalues[0] * eigenvectors[1, 0]) * eigenvalues[1]],
                        y=[0, (eigenvalues[0] * eigenvectors[0, 0]) * eigenvalues[1]],
                        line_width=3,
                        line=dict(color="gold"),
                    ),
                    go.Scatter(
                        x=[0, (-eigenvalues[1] * eigenvectors[1, 1]) * eigenvalues[0]],
                        y=[0, (eigenvalues[1] * eigenvectors[0, 1]) * eigenvalues[0]],
                        line_width=3,
                        line=dict(color="gold"),
                    ),
                ]
            ),
        ],
    )

    # add mark down
    code_eigen_markdown = readFileasStr("./utils/markdown/tab_4/code_markdown_eigen.md")

    return cal_eigen_val1, cal_eigen_val2, fig1, fig2, fig3, code_eigen_markdown
