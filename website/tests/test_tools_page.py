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
    test tools home page
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

    :param dir_path: directory path
    :return:
    """
    files = get_filepaths_from_dir(dir_path)
    return_list = []
    for file in files:
        filename = file.split("/")[-1]
        current_file = {"files": (open(file, "rb"), filename)}
        return_list.append(current_file)

    return return_list


@pytest.mark.parametrize("data",
    get_test_files("test_files/valid/")
)
def test_tools_post_valid(client: FlaskClient, data: dict) -> None:
    """
    test if clients gets redirected after pressing
    submit with valid file uploads
    """
    redirect_code = 302
    response = client.post("/tools/", data=data)
    assert response.status_code == redirect_code


@pytest.mark.parametrize("data",
    get_test_files("test_files/invalid/")
)
def test_tools_post_invalid(client: FlaskClient, data: dict) -> None:
    """
    test if invalid file uploads get redirected with an error code
    """
    invalid_file_code = 415
    response = client.post("/tools/", data=data, follow_redirects=False)
    assert response.status_code == invalid_file_code
    assert "<h2>Invalid file type</h2>" in response.text


def test_tools_results_get(client: FlaskClient) -> None:
    """
    test tools default results page
    """
    ok_status_code = 200
    response = client.get("/tools/results")
    assert response.status_code == ok_status_code
    assert "<h2>Files uploaded</h2>" in response.text


@pytest.mark.parametrize("data", [
    {},
    {"uploaded_files": "tests/test_files/wgd/input/egu1000.fasta",
     "selected_tools": "dmd"}
])
def test_tools_results_post(client: FlaskClient, data: dict) -> None:
    """
    test tools results page after selecting files and tools
    """
    # TODO nog niet alle tools doen het,
    #  en er is nog geen redirect als er geen file of tool is geselecteerd
    ok_status_code = 200
    redirect_code = 302
    response = client.post("/tools/results")
    if len(data) == 0:
        assert response.status_code == redirect_code
    else:
        assert response.status_code == ok_status_code
        assert "<h2>Files selected</h2>" in response.text
