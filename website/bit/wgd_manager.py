"""
Class that can run some wgd sub tools.

The sub tools it can run are: dmd, ksd and viz

authors: Duncan Huizer, Johanna Veenstra, Pascal Reumer, Sven Staats
date last modified: 1-4-2025
"""

# Subprocess
import subprocess
from subprocess import CompletedProcess


class WgdManager:
    def __init__(self, outdir: str, tmpdir: str):
        """
        Runs the wgd sub tools.
        The sub tools it can run are: dmd, ksd and viz.

        Parameters
        ----------
        outdir: str
            path to the directory for the tool output

        tmpdir: str
            temporary directory for temporary files the tool uses
        """
        # store the path to the tool
        self.run_wgd = "conda run -n wgd wgd "
        self.outdir = f"--outdir {outdir} "
        self.tmpdir = f"--tmpdir {tmpdir} "

    def __str__(self) -> str:
        """
        Called when the class is converted to a string.

        Returns
        -------
        str
            all the directories the tool uses
        """
        return f"""
        paths to directories used by the tool:
        directory for output: {self.outdir}
        directory for temporary files: {self.tmpdir}
        """

    def run_command(self, command: str) -> CompletedProcess[str]:
        """
        Move the current working directory to the wgd tool directory.
        Then run a terminal command with subprocess.run()

        Parameters
        ----------
        command: str
            terminal command to run, as a string

        Returns
        -------
        CompletedProcess[str]
            result of subprocess.run()
        """

        # run the command and store the result
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        return result

    def run_dmd(self, fasta_file: str) -> CompletedProcess[str]:
        """
        Run the wgd sub tool dmd.

        Outputs a paralogous/orthologous gene family as a .tsv file
        This file can be used by the sub tool ksd

        Parameters
        ----------
        fasta_file: str
            path to fasta file with coding DNA sequences

        Returns
        -------
        CompletedProcess[str]
            result of subprocess.run(command)
        """
        # command ran through subprocess to use dmd
        command = self.run_wgd + "dmd " + fasta_file + " " + self.outdir + self.tmpdir

        # run the command and store the result
        result = self.run_command(command)

        return result

    def run_ksd(self, tsv_file: str , fasta_file: str) -> CompletedProcess[str]:
        """
        Run the wgd sub tool ksd.

        ksd is used to construct Ks distributions (Ks being synonymous substitutions).

        Outputs a .tsv.ks.tsv file
        Also outputs multiple .pdf and .svg files
        .tsv.ks.tsv file can be used by the sub tool viz

        Parameters
        ----------
        tsv_file: str
            path to .tsv file containing a paralogous/orthologous
            gene family (output of dmd)

        fasta_file: str
            path to fasta file with coding DNA sequences

        Returns
        -------
        CompletedProcess[str]
            result of subprocess.run()
        """
        # command ran through subprocess to use ksd
        command = (self.run_wgd + "ksd " + tsv_file + " "
                   + fasta_file + " " + self.outdir + self.tmpdir)

        # run the command and store the result
        result = self.run_command(command)

        return result

    def run_viz(self, ks_file: str) -> CompletedProcess[str]:
        """
        Run the wgd sub tool viz.

        Used for (additional) visualisations for the ksd and syn sub tools.
        Outputs .png images

        Parameters
        ----------
        ks_file: str
            path to the ks file (.ks.tsv)

        Returns
        -------
        CompletedProcess[str]
            result of subprocess.run()
        """
        # command ran through subprocess to use viz
        command = self.run_wgd + "viz " + "-d " + ks_file + " " + self.outdir

        # run the command and store the result
        result = self.run_command(command)

        return result

    def run_syn(self, tsv_file, gff_file, ks_file=None):
        pass
