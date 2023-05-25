import dash

my_app = dash.Dash("Dashapp")
server = my_app.server
external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    "src/assets/assets.css",
]
