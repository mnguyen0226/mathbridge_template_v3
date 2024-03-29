# dash imports
from dash import dcc
from dash import html
from dash import Input
from dash import Output
import dash_bootstrap_components as dbc

# other imports
import numpy as np
import plotly.graph_objects as go

# file imports
from maindash import my_app
from utils.others.file_operations import read_file_as_str


#######################################
# Dash Layout
#######################################
def eigen_layout():
    tabs = html.Div(
        [
            dbc.Tabs(
                id="selected_tab_4",
                children=[
                    dbc.Tab(
                        label="Theory",
                        tab_id="theory_tab_4",
                    ),
                    dbc.Tab(
                        label="Playground",
                        tab_id="pg_tab_4",
                    ),
                ],
                active_tab="theory_tab_4",
            ),
            html.Br(),
            html.Div(id="tab_layout_4"),
        ]
    )
    return tabs


#######################################
# Callbacks
#######################################
@my_app.callback(
    Output(component_id="tab_layout_4", component_property="children"),
    [Input(component_id="selected_tab_4", component_property="active_tab")],
)
def render_tab_4(tab_choice):
    """Renders the selected subtab's layout

    Args:
        tab_choice (str): selected subtab

    Returns:
        selected subtab's layout
    """
    if tab_choice == "theory_tab_4":
        return eigen_theory_tab_layout()
    if tab_choice == "pg_tab_4":
        return eigen_playground_tab_layout()


#######################################
# Theory Layout
#######################################
def eigen_theory_tab_layout():
    subtab_layout = html.Div(
        [
            html.H3("Eigen Vector & Eigen Values"),
            html.Br(),
            dcc.Markdown(
                children=read_file_as_str(
                    "./utils/markdown/tab_4/code_markdown_eigen.md"
                ),
                mathjax=True,
            ),
            html.Hr(),
        ],
    )
    return subtab_layout


#######################################
# Playground Layout
#######################################
def eigen_playground_tab_layout():
    tab5Layout = html.Div(
        [
            html.H3("Eigen Vector & Eigen Values Visualization"),
            html.Br(),
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(dbc.Label("A Value"), width="auto"),
                        dbc.Col(
                            dbc.Input(
                                id="first_val",
                                type="number",
                                value=3,
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
                        dbc.Col(dbc.Label("B Value"), width="auto"),
                        dbc.Col(
                            dbc.Input(
                                id="second_val",
                                type="number",
                                value=0,
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
                        dbc.Col(dbc.Label("C Value"), width="auto"),
                        dbc.Col(
                            dbc.Input(
                                id="third_val",
                                type="number",
                                value=1,
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
                        dbc.Col(dbc.Label("D Value"), width="auto"),
                        dbc.Col(
                            dbc.Input(
                                id="fourth_val",
                                type="number",
                                value=2,
                            ),
                            width="auto",
                        ),
                    ],
                    align="center",
                ),
            ),
            html.Br(),
            html.Hr(),
            html.Strong("Calculated Eigen Value 1"),
            html.Plaintext(children="text", id="eigen-val-output1"),
            html.Br(),
            html.Strong("Calculated Eigen Value 2"),
            html.Plaintext(children="text", id="eigen-val-output2"),
            html.Hr(),
            html.Strong("Original Eigen Vectors"),
            dcc.Graph(id="eigen-origin"),
            html.Br(),
            html.Strong("Transformed Eigen Vectors"),
            dcc.Graph(id="eigen-transform"),
            html.Br(),
            html.Strong("Eigen Vectors Transformation Animation"),
            dcc.Graph(id="eigen-play"),
            html.Hr(),
        ]
    )
    return tab5Layout


selected_points = []


#######################################
# Playground Callbacks
#######################################
@my_app.callback(
    Output(component_id="eigen-val-output1", component_property="children"),
    Output(component_id="eigen-val-output2", component_property="children"),
    Output(component_id="eigen-origin", component_property="figure"),
    Output(component_id="eigen-transform", component_property="figure"),
    Output(component_id="eigen-play", component_property="figure"),
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
    # print(f"Matrix: \n{T}\n ")
    # print("Eigenvectors: \n%s" % eigenvectors)
    # print("\nEigenvalues: \n%s" % eigenvalues)

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

    return cal_eigen_val1, cal_eigen_val2, fig1, fig2, fig3
