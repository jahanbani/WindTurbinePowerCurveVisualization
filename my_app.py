import os
from dash import dcc, html, Dash

app = Dash(__name__)
server = app.server  # WSGI server for Gunicorn

app.layout = html.Div("Hello Render!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run_server(host="0.0.0.0", port=port)
