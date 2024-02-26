import logging

from dash import Dash

import dash_dlp.config

logger = logging.getLogger("dash_dlp")
logging.basicConfig(level=logging.DEBUG)

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Dash-DLP"
app.layout = dash_dlp.config.layout


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
