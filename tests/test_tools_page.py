"""
Pytests for the tool page.

authors: Duncan Huizer, Johanna Veenstra, Pascal Reumer, Sven Staats
date last modified: 1-4-2025
"""

from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from flask.testing import FlaskClient

if TYPE_CHECKING:
    from werkzeug.test import TestResponse


def test_tools_get(client: FlaskClient) -> None:
    """
    test tools home page
    """
    response: TestResponse = client.get("/tools", follow_redirects=True)

    assert response.status_code == HTTPStatus.OK
    assert "<h1>Upload files</h1>" in response.text


def get_test_files(dir_path: str) -> list[Path]:
    """
    Get all test files from a directory, used for pytest

    It is formatted as a list of dictionaries.
    This way it can be put in the pytest.mark.parametrize directly.

    :param dir_path: directory path
    :return:
    """
    return [file for file in Path("tests", dir_path).iterdir() if file.is_file()]


@pytest.mark.parametrize("data_file", get_test_files("test_files/valid/"))
def test_tools_post_valid(client: FlaskClient, data_file: Path) -> None:
    """
    test if clients gets redirected after pressing
    submit with valid file uploads
    """
    response: TestResponse = client.post(
        "/tools",
        data={"files": [(data_file.open("rb"), data_file.name)]},
        follow_redirects=True,
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("data_file", get_test_files("test_files/invalid/"))
def test_tools_post_invalid(client: FlaskClient, data_file: Path) -> None:
    """
    test if invalid file uploads get redirected with an error code
    """
    response: TestResponse = client.post(
        "/tools", data={"files": [(data_file.open("rb"), data_file.name)]}, follow_redirects=True
    )

    assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE
    assert "<h2>Invalid file</h2>" in response.text
