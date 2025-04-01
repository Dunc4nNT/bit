"""Class that can run some wgd sub tools.

The sub tools it can run are: dmd, ksd and viz
"""

import subprocess  # noqa: S404


class WgdManager:
    """Runs the wgd sub tools.

    The sub tools it can run are: dmd, ksd and viz
    """

    def __init__(self, outdir: str, tmpdir: str) -> None:
        # store the path to the tool
        self.run_wgd = ["conda", "run", "-n", "wgd", "wgd"]
        self.outdir = ["--outdir", outdir]
        self.tmpdir = ["--tmpdir", tmpdir]

    def __str__(self):
        """
        This function is called when the class is converted to a string

        :return: all the directories the tool uses
        """
        return f"""
        paths to directories used by the tool:
        directory for output: {self.outdir[1]}
        directory for temporary files: {self.tmpdir[1]}
        """

    def run_command(self, command: list[str]) -> subprocess.CompletedProcess[str]:
        """Run the wgd tool.

        Parameters
        ----------
        command : list[str]
            Terminal command to run

        Returns
        -------
        subprocess.CompletedProcess[str]
            Result of subprocess.run().
        """
        return subprocess.run(command, capture_output=True, text=True, check=False)  # noqa: S603

    def run_dmd(self, *args: str) -> subprocess.CompletedProcess[str]:
        """
        Run the wgd sub tool dmd.

        :param fasta_file: path to fasta file with coding DNA sequences

        Outputs a paralogous/orthologous gene family as a .tsv file
        in the wgd_dmd directory
        This file can be used by the sub tool ksd

        :return: result of subprocess.run()
        """
        # command ran through subprocess to use dmd
        command: list[str] = [*self.run_wgd, "dmd", *args, *self.outdir, *self.tmpdir]

        # run the command and store the result
        result: subprocess.CompletedProcess[str] = self.run_command(command)

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
        command = self.run_wgd + ["ksd", tsv_file, fasta_file] + self.outdir + self.tmpdir

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
        command = self.run_wgd + ["viz", "-d", ks_file] + self.outdir

        # run the command and store the result
        result = self.run_command(command)

        return result
