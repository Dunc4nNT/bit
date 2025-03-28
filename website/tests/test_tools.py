import pytest
from bit.app import create_app

@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
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
    check if clients gets redirected after pressing submit with no input
    """
    response = client.post("/tools/")
    assert 300 <= response.status_code < 400
    assert "<h2>Upload files</h2>" in response.text


def test_tools_result_get(client):
    pass


def test_tools_result_post(client):
    pass
