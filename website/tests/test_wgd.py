"""
Pytests for WGD.

Tests if all the requirements are installed,
and if the used wgd sub tools work (don't give errors).

Authors: Duncan Huizer, Johanna Veenstra, Pascal Reumer, Sven Staats
Date last modified: 1-4-2025
"""

# Pytest
import pytest

# Subprocess
import subprocess

# WGD Class
from bit.wgd_manager import WgdManager


def test_conda() -> None:
    """Check if conda is installed.

    Returns
    -------
    None
    """
    result = subprocess.run("which conda", capture_output=True, text=True, shell=True)
    output = result.stdout
    error = result.stderr
    assert error is ""
    assert output is not ""


@pytest.mark.parametrize("requirement", [
    "wgd",
    "diamond",
    "mcl",
    "codeml",
    "fasttree",
    "mafft",
    "i-adhore"
])
def test_requirements(requirement):
    """Check if the all the requirements are installed.

    Parameters
    ----------
    requirement: str
        the requirement to check for

    Returns
    -------
    None
    """
    conda_cmd = "conda run -n wgd "
    requirement_cmd = f"which {requirement}"
    command = conda_cmd + requirement_cmd
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    output = result.stdout
    error = result.stderr
    assert error is ""
    assert output is not ""


def test_wgd_help() -> None:
    """Test if the wgd -h command works.

    Returns
    -------
    None
    """
    command = "conda run -n wgd wgd -h"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    output = result.stdout
    error = result.stderr
    assert error is ""
    assert output is not ""


@pytest.mark.parametrize("fasta_file", [
    "tests/test_files/wgd/input/egu1000.fasta"
])
def test_dmd(fasta_file: str) -> None:
    """Test the wgd sub tool dmd.

    Parameters
    ----------
    fasta_file: str
        file to run the tool on

    Returns
    -------
    None
    """
    outdir = "tests/test_files/wgd/outpdir"
    tmpdir = "tests/test_files/wgd/tmpdir"

    wgd = WgdManager(outdir, tmpdir)
    result = wgd.run_dmd(fasta_file)
    error = result.stderr
    assert error is "" or "BiopythonWarning: Partial codon" in error


@pytest.mark.parametrize("fasta_file", [
    "tests/test_files/wgd/input/egu1000.fasta"])
@pytest.mark.parametrize("tsv_file", [
    "tests/test_files/wgd/input/egu1000.fasta.tsv"
])
def test_ksd(fasta_file: str, tsv_file: str) -> None:
    """Test the wgd sub tool ksd.

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
    outdir = "tests/test_files/wgd/outpdir"
    tmpdir = "tests/test_files/wgd/tmpdir"

    wgd = WgdManager(outdir, tmpdir)
    result = wgd.run_ksd(fasta_file, tsv_file)
    error = result.stderr
    assert error is ""


@pytest.mark.parametrize("ks_file", [
    "tests/test_files/wgd/input/egu1000.fasta.tsv.ks.tsv"
])
def test_viz(ks_file: str) -> None:
    """Test the wgd sub tool viz.

    Parameters
    ----------
    ks_file: str
        file to run the tool on

    Returns
    -------
    None
    """
    outdir = "tests/test_files/wgd/outpdir"
    tmpdir = "tests/test_files/wgd/tmpdir"

    wgd = WgdManager(outdir, tmpdir)
    result = wgd.run_viz(ks_file)
    error = result.stderr
    assert error is "" or "BiopythonWarning: Partial codon" in error


@pytest.mark.parametrize("", [])
def test_syn():
    #TODO
    pass
