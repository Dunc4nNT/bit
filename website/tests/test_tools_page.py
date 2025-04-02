"""
Pytests for the tool page.

authors: Duncan Huizer, Johanna Veenstra, Pascal Reumer, Sven Staats
date last modified: 1-4-2025
"""

# Pytest
import pytest

# Flask
from flask.testing import FlaskClient

# Function from other module
from bit.tools import get_filepaths_from_dir


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
    ok_status_code = 200
    response = client.get("/tools/")
    assert response.status_code == ok_status_code
    assert "<h2>Upload files</h2>" in response.text


def get_test_files(dir_path: str) -> list[dict]:
    """
    Get all test files from a directory, used for pytest

    It is formatted as a list of dictionaries.
    This way it can be put in the pytest.mark.parametrize directly.

    Parameters
    ----------
    dir_path: str
        Directory path to get all files from

    Returns
    -------
    list[dict]
        all test files in the directory
    """
    files = get_filepaths_from_dir(dir_path)
    return_list = []
    for file in files:
        filename = file.split("/")[-1]
        current_file = {"files": (open(file, "rb"), filename)}
        return_list.append(current_file)

    return return_list


@pytest.mark.parametrize("data",
    get_test_files("tests/test_files/valid/")
)
def test_tools_post_valid(client: FlaskClient, data: dict) -> None:
    """
    Test if clients gets redirected after pressing
    submit with valid file uploads.

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
    redirect_code = 302
    response = client.post("/tools/", data=data)
    assert response.status_code == redirect_code


@pytest.mark.parametrize("data",
    get_test_files("tests/test_files/invalid/")
)
def test_tools_post_invalid(client: FlaskClient, data: dict) -> None:
    """
    Test if invalid file uploads get redirected with an error code.

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
    invalid_file_code = 415
    response = client.post("/tools/", data=data, follow_redirects=False)
    assert response.status_code == invalid_file_code
    assert "<h2>Invalid file type</h2>" in response.text


def test_tools_results_get(client: FlaskClient) -> None:
    """
    Test tools default results page

    Parameters
    ----------
    client: FlaskClient
        client used for testing

    Returns
    -------
    None
    """
    ok_status_code = 200
    response = client.get("/tools/results")
    assert response.status_code == ok_status_code
    assert "<h2>Files uploaded</h2>" in response.text


@pytest.mark.parametrize("data", [
    {},
    {"uploaded_files": "test_files/wgd/input/egu1000.fasta"}
])
def test_tools_results_post(client: FlaskClient, data: dict) -> None:
    """
    Test tools results page after selecting files and tools.

    Parameters
    ----------
    client: FlaskClient
        Client used for testing

    data: dict
        File used for testing post request

    Returns
    -------
    None
    """
    # TODO no redirect when selecting no files
    ok_status_code = 200
    redirect_code = 302
    response = client.post("/tools/results")
    if len(data) == 0:
        assert response.status_code == redirect_code
    else:
        assert response.status_code == ok_status_code
        assert "<h2>Files selected</h2>" in response.text
