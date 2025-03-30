"""
Class that can run some wgd sub tools

The sub tools it can run are: dmd, ksd and viz

authors: Duncan Huizer, Johanna Veenstra, Pascal Reumer, Sven Staats
date last modified: 30-3-2025
"""

import subprocess
import os


class WgdManager:
    def __init__(self, path_to_tool: str, outdir: str, tmpdir: str):
        """
        Class that runs the wgd sub tools.
        The sub tools it can run are: dmd, ksd and viz.

        :param path_to_tool: path to the directory where the wgd tool is
        :param outdir: path to the directory for the tool output
        :param tmpdir: temporary directory for temporary files the tool uses
        """
        # store the path to the tool
        self.path_to_tool = path_to_tool
        self.run_wgd = ["uv", "run", "wgd"]
        self.outdir = ["--outdir", outdir]
        self.tmpdir = ["--tmpdir", tmpdir]

    def __str__(self) -> str:
        """
        Called when the class is converted to a string.

        :return: all the directories the tool uses
        """
        return f"""
        paths to directories used by the tool:
        directory for the tool: {self.path_to_tool}
        directory for output: {self.outdir[1]}
        directory for temporary files: {self.tmpdir[1]}
        """

    def run_command(self, command: str) -> str:
        """
        Move the current working directory to the wgd tool directory.
        Then run a terminal command with subprocess.run()

        :param command: terminal command to run, as a list of strings

        :return: result of subprocess.run()
        """
        # store the current working directory
        cwd = os.getcwd()
        # if the current directory is not the wgd tool directory
        if cwd != self.path_to_tool:
            # go to directory where the tool is
            os.chdir(self.path_to_tool)
        
        # run the command and store the result
        result = subprocess.run(command, capture_output=True, text=True)

        # go back to the old working directory
        os.chdir(cwd)

        return result

    def run_dmd(self, fasta_file: str) -> str:
        """
        Run the wgd sub tool dmd.

        :param fasta_file: path to fasta file with coding DNA sequences

        Outputs a paralogous/orthologous gene family as a .tsv file
        This file can be used by the sub tool ksd

        :return: result of subprocess.run()
        """
        # command ran through subprocess to use dmd
        command = self.run_wgd + ["dmd", fasta_file] + self.outdir + self.tmpdir

        # run the command and store the result
        result = self.run_command(command)

        return result

    def run_ksd(self, tsv_file: str , fasta_file: str) -> str:
        """
        Run the wgd sub tool ksd.
        ksd is used to construct Ks distributions (Ks being synonymous substitutions).

        :param tsv_file: path to .tsv file containing a paralogous/orthologous gene family (output of dmd)
        :param fasta_file: path to fasta file with coding DNA sequences

        Outputs a .tsv.ks.tsv file
        Also utputs multiple .pdf and .svg files
        This file can be visualized by the sub tool viz

        :return: result of subprocess.run()
        """
        # command ran through subprocess to use ksd
        command = self.run_wgd + ["ksd", tsv_file, fasta_file] + self.outdir + self.tmpdir

        # run the command and store the result
        result = self.run_command(command)

        return result

    def run_viz(self, ks_file: str) -> str:
        """
        Run the wgd sub tool viz
        Used to visualize Ks distributions (output of the sub tool ksd)

        :param ks_file: path to the ks file (.ks.tsv)

        Outputs .png images?

        :return: result of subprocess.run()
        """
        # command ran through subprocess to use viz
        command = self.run_wgd + ["viz", "-d", ks_file] + self.outdir

        # run the command and store the result
        result = self.run_command(command)

        return result
