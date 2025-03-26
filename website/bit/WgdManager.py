"""
This python file contains a Class that can run some wgd sub tools
The sub tools it can run are: dmd, ksd and viz

authors: <names>
date last modified: 26-3-2025
"""

import subprocess
import os


class WgdManager:
    def __init__(self, path_to_tool):
        """
        This class runs the wgd sub tools.
        The sub tools it can run are: dmd, ksd and viz
        """
        # store the path to the tool
        self.path_to_tool = path_to_tool
        self.run_wgd = ["uv", "run", "wgd"]


    def run_command(self, command):
        """
        This function moves the current working directory to the wgd tool directory
        Then runs a terminal command with subprocess.run()

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


    def run_dmd(self, fasta_file):
        """
        Runs the wgd sub tool dmd

        :param fasta_file: path to fasta file with coding DNA sequences

        Outputs a paralogous/orthologous gene family as a .tsv file
        in the wgd_dmd directory
        This file can be used by the sub tool ksd

        :return: result of subprocess.run()
        """

        # command ran through subprocess to use dmd
        command = self.run_wgd + ["dmd", fasta_file]

        # run the command and store the result
        result = self.run_command(command)

        return result


    def run_ksd(self, tsv_file, fasta_file):
        """
        Runs the wgd sub tool ksd
        ksd is used to construct Ks distributions (Ks being synonymous substitutions).

        :param tsv_file: path to .tsv file containing a paralogous/orthologous gene family (output of dmd)
        :param fasta_file: patho to fasta file with coding DNA sequences

        Outputs a .tsv.ks.tsv file in the wgd_ksd directory
        This file can be visualized by the sub tool viz

        :return: result of subprocess.run()
        """

        # command ran through subprocess to use ksd
        command = self.run_wgd + ["ksd", tsv_file, fasta_file]

        # run the command and store the result
        result = self.run_command(command)

        return result


    def run_viz(self, ks_file):
        """
        Runs the wgd sub tool viz
        Used to visualize Ks distributions (output of the sub tool ksd)

        :param ks_file: path to the ks file (.ks.tsv)

        Outputs multiple .pdf and .svg files in the wgd_viz directory

        :return: result of subprocess.run()
        """

        # command ran through subprocess to use viz
        command = self.run_wgd + ["viz", "-d", ks_file]

        # run the command and store the result
        result = self.run_command(command)

        return result


if __name__ == "__main__":

    # path to the wgd tool
    # TODO should probably be configurable through a config file or input or something
    path_to_tool = "/homes/sstaats/jaar_1/kwartaal_3/bin_toolbox/website/bit/tools/wgd/"

    # create instance of wgd class
    wgd = WgdManager(path_to_tool)

    # paths to files used
    fasta_file = "test/data/egu1000.fasta"
    tsv_file = "wgd_dmd/egu1000.fasta.tsv"
    ks_file = "wgd_ksd/egu1000.fasta.tsv.ks.tsv"

    # run the dmd command
    wgd_result = wgd.run_dmd(fasta_file)
    # show the result of the command in the terminal
    print(wgd_result.stdout)

    # run the ksd command
    ksd_result = wgd.run_ksd(tsv_file, fasta_file)
    # show the result of the command in the terminal
    print(ksd_result.stdout)

    # run the viz command
    viz_result = wgd.run_viz(ks_file)
    # show the result of the command in the terminal
    print(viz_result.stdout)
