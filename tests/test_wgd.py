"""
Pytests for WGD.

Tests if all the requirements are installed,
and if the used wgd sub tools work (don't give errors).

Authors: Duncan Huizer, Johanna Veenstra, Pascal Reumer, Sven Staats
Date last modified: 9-4-2025
"""

import subprocess

import pytest

from bit.wgd_manager import WgdManager


def test_conda() -> None:
    """
    Check if conda is installed.

    Returns
    -------
    None
    """
    conda_cmd = ["which", "conda"]

    result = subprocess.run(conda_cmd, capture_output=True, text=True, check=True)

    output = result.stdout
    error = result.stderr
    assert error == ""
    assert output != ""


@pytest.mark.parametrize(
    "requirement",
    [
        "wgd",
        "diamond",
        "mcl",
        "codeml",
        "fasttree",
        "mafft",
    ],
)
def test_requirements(requirement: str) -> None:
    """
    Check if the all the requirements are installed.

    Parameters
    ----------
    requirement: str
        the requirement to check for

    Returns
    -------
    None
    """
    conda_cmd = ["conda", "run", "-n", "wgd"]
    requirement_cmd = ["which", requirement]
    command = conda_cmd + requirement_cmd

    result = subprocess.run(command, capture_output=True, text=True, check=True)

    output = result.stdout
    error = result.stderr
    assert error == ""
    assert output != ""


def test_wgd_help() -> None:
    """
    Test if the wgd -h command works.

    Returns
    -------
    None
    """
    command = ["conda", "run", "-n", "wgd", "wgd", "-h"]

    result = subprocess.run(command, capture_output=True, text=True, check=True)

    output = result.stdout
    error = result.stderr
    assert error == ""
    assert output != ""


@pytest.mark.parametrize(
    "fasta_file",
    ["tests/test_files/wgd/input/egu1000.fasta", "tests/test_files/wgd/input/ugi1000.fasta"],
)
def test_dmd(fasta_file: str) -> None:
    """
    Test the wgd sub tool dmd.

    Parameters
    ----------
    fasta_file: str
        file to run the tool on

    Returns
    -------
    None
    """
    outdir = "tests/test_files/wgd/outdir"
    tmpdir = "tests/test_files/wgd/tmpdir"

    wgd = WgdManager(outdir, tmpdir)
    result = wgd.run_dmd(fasta_file)

    error = result.stderr
    assert error == "" or "BiopythonWarning: Partial codon" in error


@pytest.mark.parametrize("fasta_file", ["tests/test_files/wgd/input/egu1000.fasta"])
@pytest.mark.parametrize("tsv_file", ["tests/test_files/wgd/input/egu1000.fasta.tsv"])
def test_ksd(fasta_file: str, tsv_file: str) -> None:
    """
    Test the wgd sub tool ksd.

    Parameters
    ----------
    fasta_file: str
        file to run the tool on

    tsv_file: str
        file to run the tool on

    Returns
    -------
    None
    """
    outdir = "tests/test_files/wgd/outdir"
    tmpdir = "tests/test_files/wgd/tmpdir"

    wgd = WgdManager(outdir, tmpdir)
    result = wgd.run_ksd(fasta_file, tsv_file)

    error = result.stderr
    assert error == ""


@pytest.mark.parametrize(
    "ks_file",
    [
        "tests/test_files/wgd/input/ath_test.ks.tsv",
    ],
)
def test_viz(ks_file: str) -> None:
    """
    Test the wgd sub tool viz.

    Parameters
    ----------
    ks_file: str
        file to run the tool on

    Returns
    -------
    None
    """
    outdir = "tests/test_files/wgd/outdir"
    tmpdir = "tests/test_files/wgd/tmpdir"

    wgd = WgdManager(outdir, tmpdir)
    result = wgd.run_viz(ks_file)

    error = result.stderr
    assert error == "" or "BiopythonWarning: Partial codon" in error
