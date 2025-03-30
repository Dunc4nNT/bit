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


def test_tools_results_get(client):
    """
    test tools default results page
    """
    response = client.get("/tools/results")
    print(response.text)
    assert response.status_code == 200


def test_tools_results_post(client):
    """
    test tools results page after selecting files and tools
    """
    response = client.post("/tools/results")
    assert response.status_code == 200
