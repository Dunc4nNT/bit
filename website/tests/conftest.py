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
    return create_app()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """
    create test app
    :return: test client for the app
    """
    return app.test_client()
