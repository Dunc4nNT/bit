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
    Test the tools home page.

    Parameters
    ----------
    client: FlaskClient
        client used for testing

    Returns
    -------
    None
    """
    response: TestResponse = client.get("/tools", follow_redirects=True)

    assert response.status_code == HTTPStatus.OK
    assert "<h1>Upload files</h1>" in response.text


def get_test_files(dir_path: str) -> list[Path]:
    """
    Get all test files from a directory, used for pytest.

    Parameters
    ----------
    dir_path: str
        Directory path to get all files from

    Returns
    -------
    list[dict]
        all test files in the directory
    """
    return [file for file in Path("tests", dir_path).iterdir() if file.is_file()]


@pytest.mark.parametrize("data_file", get_test_files("test_files/file_upload/valid/"))
def test_tools_post_valid(client: FlaskClient, data_file: Path) -> None:
    """
    Test valid file uploads.

    Parameters
    ----------
    client: FlaskClient
        client used for testing

    data: dict
        Valid file used for testing post request

    Returns
    -------
    None
    """
    response: TestResponse = client.post(
        "/tools",
        data={"files": [(data_file.open("rb"), data_file.name)]},
        follow_redirects=True,
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize("data_file", get_test_files("test_files/file_upload/invalid/"))
def test_tools_post_invalid(client: FlaskClient, data_file: Path) -> None:
    """
    Test invalid file uploads.

    Parameters
    ----------
    client: FlaskClient
        client used for testing

    data: dict
        Invalid file used for testing post request

    Returns
    -------
    None
    """
    response: TestResponse = client.post(
        "/tools", data={"files": [(data_file.open("rb"), data_file.name)]}, follow_redirects=True
    )

    assert response.status_code == HTTPStatus.UNSUPPORTED_MEDIA_TYPE
    assert "<h2>Invalid file</h2>" in response.text
