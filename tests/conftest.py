import pytest
from flask import Flask
from flask.testing import FlaskClient

from bit.app import create_app


@pytest.fixture
def app() -> Flask:
    """
    create app
    :return: app
    """

    app: Flask = create_app()
    app.testing = True
    app.secret_key = "TESTING_KEY"  # noqa: S105

    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """
    create test app
    :return: test client for the app
    """
    return app.test_client()
