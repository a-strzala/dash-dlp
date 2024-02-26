import logging
from pathlib import Path

import appdirs
import yaml
from dash import dcc, html, callback, Output, Input, State

logger = logging.getLogger("dash_dlp.config")
logging.basicConfig(level=logging.DEBUG)
logger.debug("Loading configuration...")

APP_NAME = "dash_dlp"
APP_AUTHOR = "dash_dlp"

app_dirs = appdirs.AppDirs(APP_NAME, APP_AUTHOR)
DATA_DIR = Path(app_dirs.user_data_dir).resolve()
CONFIG_DIR = Path(app_dirs.user_config_dir).resolve()
CACHE_DIR = Path(app_dirs.user_cache_dir).resolve()
DEFAULT_CONFIG_VALUES = {
    "collection_dir": DATA_DIR / "collection",
}

CONFIG_FILE = CONFIG_DIR / "config.yaml"
initial_setup = False if CONFIG_FILE.exists() else True
logger.debug(f"Checking {CONFIG_FILE}, {initial_setup=}")

if not initial_setup:
    with open(CONFIG_FILE, "r") as f:
        settings = yaml.safe_load(f)
        logger.debug(f"Found settings: {settings}")
    for key, value in DEFAULT_CONFIG_VALUES.items():
        if key not in settings:
            settings[key] = value
        logger.debug(f"Setting {key} not found, falling back to: {settings[key]}")

DATABASE_FILE = DATA_DIR / "app_data.db"
if not DATABASE_FILE.exists():
    logger.debug(f"Creating database file at {DATABASE_FILE}")
    DATABASE_FILE.touch()

DATA_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

SETUP_LAYOUT = html.Div(
    children=[
        html.H1("Initial configuration"),
        html.P(
            f"It seems that this is the first time you run the application. This setup will guide you through the most important settings. If you want to change these settings later, or access more advance configuration options, you can do so by editing the configuration file, located at: {CONFIG_FILE}"
        ),
        html.H2("Collection directory"),
        html.P(
            "This is where the downloaded audio and video files will be stored after processing."
        ),
        dcc.Input(
            id="collection_dir",
            type="text",
            value=str(DEFAULT_CONFIG_VALUES["collection_dir"]),
        ),
        html.H2("Save configuration"),
        html.P("If you are happy with the settings, click the button below to save the configuration, then restart the application."),
        html.Button("Save", id="config_save_button"),
    ]
)

APPLICATION_LAYOUT = html.Div(
    [
        html.H1("Dash-DLP"),
        html.P("Welcome to Dash-DLP!"),
    ]
)

@callback(
    Output("config_save_button", "n_clicks"),
    [Input("config_save_button", "n_clicks")],
    [State("collection_dir", "value")],
)
def save_config(n_clicks, collection_dir):
    if n_clicks:
        logger.debug(f"Saving configuration: {collection_dir=}")
        with open(CONFIG_FILE, "w") as f:
            yaml.dump({"collection_dir": collection_dir}, f)
        return n_clicks
    return 0

layout = SETUP_LAYOUT if initial_setup else APPLICATION_LAYOUT

logger.debug("Configuration loaded")
