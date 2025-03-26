from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from bit.WgdManager import WgdManager

blueprint: Blueprint = Blueprint("tools", __name__, url_prefix="/tools")

# TODO dynamisch maken uiteindelijk ofso
path_to_tool = "/homes/sstaats/jaar_1/kwartaal_3/bin_toolbox/website/bit/tools/wgd/"
upload_dir = "/homes/sstaats/jaar_1/kwartaal_3/bin_toolbox/website/bit/website/bit/upload/"


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
            }

            # if no files given, return to default tool page
            if kwargs["filename"] == "":
                #return render_template("tools/tools_GET.html", allowed_extensions=allowed_extensions)
                return redirect(url_for("tools.index"))

            # if a file with an incorrect extension was given, return to tools_INVALID.html
            if kwargs["file_extension"] not in allowed_extensions:
                return render_template("tools/tools_INVALID.html", **kwargs)

            # save file in upload folder
            file.save(upload_dir + kwargs["filename"])

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
    # Page where user can select tools and files
    if request.method == "GET":
        filepaths = get_filepaths_from_dir(upload_dir)
        files = []
        for filepath in filepaths:
            file = {
                "filepath": filepath,
                "filename": filepath.split("/")[-1],
            }
            files.append(file)
        return render_template("tools/tools_POST.html", files=files)

    # When the submit button is pressed
    elif request.method == "POST":
        # get the selected files
        selected_files = request.form.getlist("uploaded_file")
        # create the class that can run wgd
        wgd = WgdManager(path_to_tool)
        # run the dmd sub tool for each selected file
        for file in selected_files:
            result = wgd.run_dmd(file)

        return render_template("tools/tools_RESULTS.html", files=selected_files, result=result)
