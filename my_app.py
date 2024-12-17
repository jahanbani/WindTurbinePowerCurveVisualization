import os
from dash import dcc, html, Dash

myapp = Dash(__name__)
server = myapp.server  # WSGI server for Gunicorn

myapp.layout = html.Div("Hello Render!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    myapp.run_server(host="0.0.0.0", port=port)
