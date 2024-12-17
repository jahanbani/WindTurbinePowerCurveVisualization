import os
from dash import Dash, html

app = Dash(__name__)
server = app.server  # This is the WSGI server that Gunicorn will use

app.layout = html.Div(
    children=[
        html.H1(children="Hello from Render!"),
        html.Div(children="This is a Dash app deployed on Render."),
    ]
)

if __name__ == "__main__":
    # For local testing:
    # python app.py
    app.run_server(host="0.0.0.0", port=os.environ.get("PORT", 8080))
