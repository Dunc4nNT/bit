"""
Python file for the tool page
Here the website user can upload files, use wgd, and view the output.

authors: <names>
date last modified: 26-3-2025
"""
from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
from bit.WgdManager import WgdManager

blueprint: Blueprint = Blueprint("tools", __name__, url_prefix="/tools")

# TODO instelbaar maken voor de gebruiker uiteindelijk ofso
from bit.dirpaths import *


def get_filepaths_from_dir(directory):
    """
    get the filepaths from all files in a directory

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
 

def valid_file(file):
    """
    This function checks if a file is more "likely" valid.
    starts with >
    :param file:
    :return: True if file is valid and saves data, else False
    """
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
    # list of the allowed file types to upload
    allowed_extensions = ["fasta"]

    # default tool page, to upload files
    if request.method == "GET":
        return render_template("tools/tools_GET.html", allowed_extensions=allowed_extensions)

    # if submit button is pressed for the file upload
    elif request.method == "POST":
        files = request.files.getlist("files")

        # validate files
        for file in files:
            # properties for each file
            kwargs = {
                "file": file,
                "filename": secure_filename(file.filename),  # SECURE filename
                "file_extension": file.filename.split(".")[-1],
                "file_size": file.content_length,
            }

            # if no files given, return to default tool page
            if kwargs["filename"] == "":
                #return render_template("tools/tools_GET.html", allowed_extensions=allowed_extensions)
                return redirect(url_for("tools.index"))

            # if a file with an incorrect extension was given, return to tools_INVALID.html
            if kwargs["file_extension"] not in allowed_extensions:
                return render_template("tools/tools_INVALID.html", **kwargs)
              
            # if a file exceeds the size limit, return to tools_FILE_TOO_LARGE.html
            if kwargs["file_size"] > max_file_size:
                return render_template("tools/tools_FILE_TOO_LARGE.html", **kwargs)

            # if not valid return to tools_INVALID.html
            if not valid_file(file.stream):
                return render_template("tools/tools_INVALID.html", **kwargs)

            # save file in upload folder
            file.save(uploads_dir + kwargs["filename"])

        # when files are uploaded, go to the results page
        return redirect(url_for("tools.results"))


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
    # page where user can select tools and files
    if request.method == "GET":
        filepaths = get_filepaths_from_dir(uploads_dir)
        files = []
        for filepath in filepaths:
            file = {
                "filepath": filepath,
                "filename": filepath.split("/")[-1],
            }
            files.append(file)
        return render_template("tools/tools_POST.html", files=files)

    # when the submit button is pressed
    elif request.method == "POST":
        # get the selected files
        selected_files = request.form.getlist("uploaded_file")
        # create the class that can run wgd
        wgd = WgdManager(path_to_tool, outdir, tmpdir)
        # run the dmd sub tool for each selected file
        for file in selected_files:
            result = wgd.run_dmd(file)

        return render_template("tools/tools_RESULTS.html", files=selected_files, result=result)
  

@blueprint.errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error):
    return render_template('tools/tools_FILE_TOO_LARGE.html'), 413
