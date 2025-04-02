"""
Python file for the tool page

Here the website user can upload files, use wgd, and view the output.

authors: Duncan Huizer, Johanna Veenstra, Pascal Reumer, Sven Staats
date last modified: 1-4-2025
"""

# Flask
from flask import Blueprint, render_template, request, redirect, url_for

# Werkzeug
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.datastructures import FileStorage

# Os
import os

# Wgd Class
from bit.wgd_manager import WgdManager

blueprint: Blueprint = Blueprint("tools", __name__, url_prefix="/tools")

# TODO instelbaar maken voor de gebruiker uiteindelijk ofso
from bit.dirpaths import *


def get_filepaths_from_dir(directory: str) -> list[str]:
    """
    Get the filepaths from all files in a directory.

    :param directory: directory as string
    :return: filepath of each file as a list of strings
    """
    # list to return
    filepaths_list = []
    # for each file in the directory
    for file in os.listdir(directory):
        # get the file_name
        file_name = os.fsdecode(file)
        # append it to a list
        filepaths_list.append(directory + file_name)

    return filepaths_list
 

def valid_file(file: FileStorage) -> (bool, list, list):
    """
    check if a file is more "likely" valid.
    starts with >
    :param file:
    :return: True if file is valid and saves data, else False
    """
    file = file.stream
    data_list = []
    header_list = []
    header = file.readline()
    data = file.readlines()
    # opening file in bytes mode, so made a string
    header = str(header, encoding="utf-8")
    if header.startswith(">"):
        data_list.append(data)
        header_list.append(header)
        return True, data_list, header_list


# list of the allowed file types to upload
allowed_extensions = ["fasta"]
# sets max upload size to 500mb
max_file_size = 500 * 1024 * 1024
# max_file_size = 98_816


@blueprint.route("/", methods=["GET", "POST"])
def index() -> str:
    """Tools landing page.

    On this page the user can upload files

    Returns
    -------
    str
        The tools landing page template.
    """
    # default tool page, to upload files
    if request.method == "GET":
        return render_template("tools/tools_GET.html", allowed_extensions=allowed_extensions)

    # if submit button is pressed for the file upload
    elif request.method == "POST":
        files = request.files.getlist("files")

        # validate files
        for file in files:
            # properties for each file
            current_file = {
                "file": file,
                "filename": secure_filename(file.filename),  # SECURE filename
                "file_extension": file.filename.split(".")[-1],
                "file_size": file.content_length,
            }

            # if no files given, return to default tool page
            if current_file["filename"] == "":
                return redirect(url_for("tools.index")), 302

            # if a file with an incorrect extension was given, return to tools_INVALID.html
            if current_file["file_extension"] not in allowed_extensions:
                return render_template("tools/tools_INVALID.html", **current_file), 415
              
            # if a file exceeds the size limit, return to tools_FILE_TOO_LARGE.html
            if current_file["file_size"] > max_file_size:
                return render_template("tools/tools_FILE_TOO_LARGE.html", **current_file), 413

            # TODO this function causes uploaded files to be empty
            # if not valid return to tools_INVALID.html
            if not valid_file(file):
                return render_template("tools/tools_INVALID.html", **current_file), 415

            # try to save file in upload folder
            try:
                file.save(uploads_dir + current_file["filename"])
            except FileNotFoundError:
                return render_template("tools/tools_INVALID_PATH.html", dir=uploads_dir), 409

        # when files are uploaded, go to the results page
        return redirect(url_for("tools.results")), 302


@blueprint.route("/results", methods=["GET", "POST"])
def results() -> str:
    """Tools results page.

    On this page the user can select the tools to run,
    and the files to run the tools on.

    Returns
    -------
    str
        The tools results page template.
    """

    # list of used wgd sub tools
    tools_list = ["dmd", "ksd", "viz", "syn"]

    # page where user can select tools and files
    if request.method == "GET":

        # try to get all uploaded files
        try:
            filepaths = get_filepaths_from_dir(uploads_dir)

        # if the file path is invalid, return to error page
        except FileNotFoundError:
            return render_template("tools/tools_INVALID_PATH.html", dir=uploads_dir), 409

        # create empty list and loop over each file
        files = []
        for filepath in filepaths:
            # save the path and name for each file in a dict
            file = {
                "filepath": filepath,
                "filename": filepath.split("/")[-1],
            }
            # append the dict to a list (except the .gitignore)
            if file["filename"] != ".gitignore":
                files.append(file)

        return render_template("tools/tools_POST.html",
                               files=files, tools=tools_list)

    # when the submit button is pressed
    elif request.method == "POST":
        # get the selected files and tools
        selected_files = request.form.getlist("uploaded_files")
        selected_tools = request.form.getlist("selected_tools")
        # create the class that can run wgd
        wgd = WgdManager(outdir, tmpdir)
        # run the dmd sub tool for each selected file

        # TODO moet check of wel een file is geupload
        result = ""
        for fasta_file in selected_files:
            result = wgd.run_dmd(fasta_file)

            # TODO dit werkt niet echt bepaald
            # if "dmd" in selected_tools:
            #     result = wgd.run_dmd(fasta_file)
            # if "ksd" in selected_tools:
            #     result = wgd.run_ksd(fasta_file + ".tsv", fasta_file)
            #
            # if "viz" in selected_tools:
            #     result = wgd.run_viz(fasta_file + ".tsv.ks.tsv")

            # TODO bestaat nog niet
            # if "syn" in selected_tools:
            #     result = wgd.run_syn(file)

        return render_template("tools/tools_RESULTS.html",
                               files=selected_files, tools=selected_tools, result=result)


@blueprint.errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error):
    return render_template('tools/tools_FILE_TOO_LARGE.html'), 413
