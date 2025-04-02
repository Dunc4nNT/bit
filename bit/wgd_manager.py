"""Class that can run some wgd sub tools.

The sub tools it can run are: dmd, ksd and viz
"""

import subprocess
from subprocess import CompletedProcess
from typing import Any, Literal, TypedDict, Unpack, override


def _parse_kwargs(kwargs: Any) -> list[Any]:  # noqa: ANN401
    parsed: list[Any] = []

    for key, value in kwargs.items():
        if isinstance(value, list):
            parsed.extend(_format_kwarg(key, item) for item in value)  # type: ignore[reportUnknownVariableType]
        else:
            parsed.extend(_format_kwarg(key, value))

    return parsed


def _format_kwarg(key: str, value: Any) -> list[Any]:  # noqa: ANN401
    if isinstance(value, bool) and value:
        return [f"--{key}"]

    return [f"--{key}", str(value)]


class Dmd(TypedDict, total=False):
    """Accepted kwargs for wgd dmd."""

    outdir: str
    tmpdir: str
    prot: bool
    cscore: float
    inflation: float
    eval: float
    to_stop: bool
    cds: bool
    focus: str
    anchorpoints: str
    segments: str
    listelements: str
    genetable: str
    collinearcoalescence: bool
    keepfasta: bool
    keepduplicates: bool
    globalmrbh: bool
    nthreads: int
    orthoinfer: bool
    onlyortho: bool
    getnsog: bool
    tree_method: Literal["fasttree", "iqtree", "mrbayes"]
    treeset: list[str]
    msogcut: float
    geneassign: bool
    seq2assign: list[str]
    fam2assign: str
    concat: bool
    testsog: bool
    bins: int
    normalizedpercent: int
    nonormalization: bool
    buscosog: bool
    buscohmm: str
    buscocutoff: str
    ogformat: bool


class Ksd(TypedDict, total=False):
    """Accepted kwargs for wgd ksd."""

    outdir: str
    tmpdir: str
    nthreads: int
    to_stop: bool
    cds: bool
    pairwise: bool
    strip_gaps: bool
    aligner: Literal["muscle", "prank", "mafft"]
    aln_options: str
    tree_method: Literal["cluster", "fasttree", "iqtree"]
    tree_options: str
    node_average: bool
    spair: list[str]
    speciestree: str
    reweight: bool
    onlyrootout: bool
    extraparanomeks: str
    anchorpoints: str
    plotkde: bool
    plotapgmm: bool
    plotelmm: bool
    components: tuple[int]
    xlim: tuple[int | None]
    ylim: tuple[int | None]
    adjustortho: bool
    adjustfactor: float
    okalpha: float
    focus2all: str
    kstree: bool
    onlyconcatkstree: bool
    classic: bool
    toparrow: bool
    bootstrap: int


class Viz(TypedDict, total=False):
    """Accepted kwargs for wgd viz."""

    data_file: str
    outdir: str
    spair: list[str]
    focus2all: str
    gsmap: str
    speciestree: str
    plotkde: bool
    reweight: bool
    onlyrootout: bool
    em_iterations: int
    em_initializations: int
    prominence_cutoff: float
    rel_height: float
    segments: str
    minlen: int
    maxsize: int
    anchorpoints: str
    multiplicon: str
    genetable: str
    minseglen: int
    mingenenum: int
    keepredun: bool
    extraparanomeks: str
    plotapgmm: bool
    plotelmm: bool
    components: tuple[int]
    plotsyn: bool
    dotsize: float
    apalpha: float
    hoalpha: float
    showrealtick: bool
    ticklabelsize: float
    xlim: tuple[int | None]
    ylim: tuple[int | None]
    adjustortho: bool
    adjustfactor: float
    okalpha: float
    classic: bool
    toparrow: bool
    nodeaveraged: bool
    bootstrap: int
    gistrb: bool
    nthreads: int


class WgdManager:
    """Runs the wgd sub tools.

    The sub tools it can run are: dmd, ksd and viz
    """

    def __init__(self, outdir: str, tmpdir: str) -> None:
        # store the path to the tool
        self.run_wgd = ["conda", "run", "-n", "wgd", "wgd"]
        self.outdir = ["--outdir", outdir]
        self.tmpdir = ["--tmpdir", tmpdir]

    @override
    def __str__(self) -> str:
        return f"""
        paths to directories used by the tool:
        directory for output: {self.outdir[1]}
        directory for temporary files: {self.tmpdir[1]}
        """

    def run_command(self, command: list[str]) -> CompletedProcess[str]:
        """Run the wgd tool.

        Parameters
        ----------
        command : list[str]
            Terminal command to run

        Returns
        -------
        CompletedProcess[str]
            Result of subprocess.run().
        """
        return subprocess.run(command, capture_output=True, text=True, check=True)

    def run_dmd(self, *sequences: str, **kwargs: Unpack[Dmd]) -> CompletedProcess[str]:
        """Run the wgd sub tool dmd.

        Outputs a paralogous/orthologous gene family as a .tsv file
        in the wgd_dmd directory
        This file can be used by the sub tool ksd

        Parameters
        ----------
        *sequences : str
            Path to files containing a genome's DNA coding sequences.
            Gene IDs must be unique, e.g. like you get from RefSeq Select.
        **kwargs : Dmd
            Kwargs to parse to wgd dmd.

        Returns
        -------
        CompletedProcess[str]
            Result of subprocess.run().
        """
        # command ran through subprocess to use dmd
        command: list[str] = [
            *self.run_wgd,
            "dmd",
            *sequences,
            *self.outdir,
            *self.tmpdir,
            *_parse_kwargs(kwargs),
        ]

        # run the command and store the result
        result: CompletedProcess[str] = self.run_command(command)

        return result

    def run_ksd(self, families: str, *sequences: str, **kwargs: Ksd) -> CompletedProcess[str]:
        """Run the wgd sub tool ksd.

        ksd is used to construct Ks distributions (Ks being synonymous substitutions).

        Outputs a .tsv.ks.tsv file in the wgd_ksd directory
        This file can be visualized by the sub tool viz

        Parameters
        ----------
        families : str
            Path to a families file, constructed by wgd dmd.
        *sequences : str
            Path to files containing a genome's DNA coding sequences.
            These genomes should match the genomes in the families file.
            Gene IDs must be unique, e.g. like you get from RefSeq Select.

        Returns
        -------
        CompletedProcess[str]
            Result of subprocess.run().
        """
        # command ran through subprocess to use ksd
        command: list[str] = [
            *self.run_wgd,
            "ksd",
            families,
            *sequences,
            *self.outdir,
            *self.tmpdir,
            *_parse_kwargs(kwargs),
        ]

        # run the command and store the result
        result: CompletedProcess[str] = self.run_command(command)

        return result

    def run_viz(self, data: str, **kwargs: Viz) -> CompletedProcess[str]:
        """Run the wgd sub tool viz.

        Used to visualize Ks distributions (output of the sub tool ksd)

        Outputs multiple .pdf and .svg files in the wgd_viz directory

        Parameters
        ----------
        data : str
            Path to a data file, for example the one constructed by wgd ksd.

        Returns
        -------
        CompletedProcess[str]
            Result of subprocess.run().
        """
        # command ran through subprocess to use viz
        command: list[str] = [
            *self.run_wgd,
            "viz",
            "-d",
            data,
            *self.outdir,
            *_parse_kwargs(kwargs),
        ]

        # run the command and store the result
        result: CompletedProcess[str] = self.run_command(command)

        return result
