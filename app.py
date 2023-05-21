from maindash import my_app
from dash import html

# dash constructor
server = my_app.server

# dash layout
my_app.layout = html.Div([
    html.H3("Hello")
])

if __name__ == "__main__":
    my_app.run_server(debug=True,host='0.0.0.0',port=80)