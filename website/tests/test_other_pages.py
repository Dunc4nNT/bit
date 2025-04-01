"""
Pytests for the tool page.

authors: Duncan Huizer, Johanna Veenstra, Pascal Reumer, Sven Staats
date last modified: 1-4-2025
"""

# Pytest
import pytest

# Flask
from flask.testing import FlaskClient

def test_home_page(client: FlaskClient) -> None:
    """
    test home page
    """
    ok_status_code = 200
    response = client.get("/")
    assert response.status_code == ok_status_code
    assert "<h2>Welcome to WGD Wizard</h2>" in response.text


def test_background_reading_page(client: FlaskClient) -> None:
    """
    test background reading page
    """
    ok_status_code = 200
    response = client.get("/background_reading")
    assert response.status_code == ok_status_code
    assert "<h2>WGD Tools</h2>" in response.text


def test_about_page(client: FlaskClient) -> None:
    """
    test about page
    """
    ok_status_code = 200
    response = client.get("/about")
    assert response.status_code == ok_status_code
    assert "<title>About - bit</title>" in response.text
