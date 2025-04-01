import tomllib

from flask import Flask

from .tools import blueprint as tools_blueprint
from .views import blueprint as core_blueprint


def create_app() -> Flask:
    """Create the bit Flask application.

    Parameters
    ----------
    config_file : str
        The name of the configuration file.

    Returns
    -------
    Flask
        The bit Flask application.
    """
    app: Flask = Flask(__name__)
    app.config.from_file("../settings.toml", load=tomllib.load, text=False)
    # sets max upload size to 500mb
    app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024
    register_blueprints(app)

    return app


def register_blueprints(app: Flask) -> None:
    """Register blueprints for Flask."""
    app.register_blueprint(core_blueprint)
    app.register_blueprint(tools_blueprint)
