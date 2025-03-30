import pytest
from bit.app import create_app


@pytest.fixture
def app():
    """
    create app
    :return: app
    """
    return create_app()


@pytest.fixture
def client(app):
    """
    create test app
    :return: test client for the app
    """
    return app.test_client()


def test_tools_get(client):
    """
    test tools home page
    """
    response = client.get("/tools/")
    assert response.status_code == 200
    assert "<h2>Upload files</h2>" in response.text


def test_tools_post(client):
    """
    test if clients gets redirected after pressing submit
    """
    response = client.post("/tools/")
    assert 300 <= response.status_code < 400


def test_tools_result_get(client):
    pass


def test_tools_result_post(client):
    pass
