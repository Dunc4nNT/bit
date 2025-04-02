"""Class that can run some wgd sub tools.

The sub tools it can run are: dmd, ksd and viz
"""

import subprocess
from subprocess import CompletedProcess
from typing import override


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

    def run_dmd(self, *sequences: str) -> CompletedProcess[str]:
        """Run the wgd sub tool dmd.

        Outputs a paralogous/orthologous gene family as a .tsv file
        in the wgd_dmd directory
        This file can be used by the sub tool ksd

        Parameters
        ----------
        *sequences : str
            Path to files containing a genome's DNA coding sequences.
            Gene IDs must be unique, e.g. like you get from RefSeq Select.

        Returns
        -------
        CompletedProcess[str]
            Result of subprocess.run().
        """
        # command ran through subprocess to use dmd
        command: list[str] = [*self.run_wgd, "dmd", *sequences, *self.outdir, *self.tmpdir]

        # run the command and store the result
        result: CompletedProcess[str] = self.run_command(command)

        return result

    def run_ksd(self, families: str, *sequences: str) -> CompletedProcess[str]:
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
        ]

        # run the command and store the result
        result: CompletedProcess[str] = self.run_command(command)

        return result

    def run_viz(self, data: str) -> CompletedProcess[str]:
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
        command: list[str] = [*self.run_wgd, "viz", "-d", data, *self.outdir, *self.tmpdir]

        # run the command and store the result
        result: CompletedProcess[str] = self.run_command(command)

        return result
