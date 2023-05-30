import dash
import dash_bootstrap_components as dbc

my_app = dash.Dash('Dashapp', external_stylesheets=[dbc.themes.BOOTSTRAP])
server = my_app.server
