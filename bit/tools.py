"""Python file for the tool page.

Here the website user can upload files, use wgd, and view the output.
"""

import os
from http import HTTPMethod
from pathlib import Path
from typing import IO, TYPE_CHECKING, Literal

from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug import Response
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from bit.dirpaths import outdir, tmpdir, uploads_dir
from bit.wgd_manager import WgdManager

if TYPE_CHECKING:
    from subprocess import CompletedProcess  # noqa: S404

    from werkzeug.datastructures.file_storage import FileStorage

blueprint: Blueprint = Blueprint("tools", __name__, url_prefix="/tools")


def get_filepaths_from_dir(directory: str) -> list[str]:
    """Get the filepaths from all files in a directory.

    Parameters
    ----------
    directory : str
        directory

    Returns
    -------
    list[str]
        filepath of each file.
    """
    filepaths_list: list[str] = []
    # for each file in the directory
    for file in Path(directory).iterdir():
        # get the file_name
        file_name = os.fsdecode(file)
        # append it to a list
        filepaths_list.append(directory + file_name)

    return filepaths_list


def validate_file(file: IO[bytes]) -> bool:
    """Check if a file is more "likely" valid.

    Starts with >.

    Parameters
    ----------
    file : IO[bytes]
        File to check.

    Returns
    -------
    bool
        Whether the file is valid.
    """
    return True

    # data_list = []
    # header_list = []
    # header = file.readline()
    # data = file.readlines()
    # # opening file in bytes mode, so made a string
    # header = str(header, encoding="utf-8")
    # if header.startswith(">"):
    #     data_list.append(data)
    #     header_list.append(header)
    #     return True, data_list, header_list


allowed_extensions = ["fasta"]
# sets max upload size to 500mb
max_file_size = 500 * 1024 * 1024


@blueprint.route("/", methods=["GET", "POST"])
def index() -> str | Response:
    """Tools landing page.

    On this page the user can upload files

    Returns
    -------
    str | Response
        The tools landing page template.
    """
    # list of the allowed file types to upload
    allowed_extensions: list[str] = ["fasta"]

    match request.method:
        # if submit button is pressed for the file upload
        case HTTPMethod.POST:
            files: list[FileStorage] = request.files.getlist("files")

            if len(files) == 0:
                return redirect(url_for("tools.index"))

            # validate files
            for file in files:
                # if no files given, return to default tool page
                if not file.filename:
                    return redirect(url_for("tools.index"))

                file_name: str = secure_filename(file.filename)

                # if a file with an incorrect extension was given, return to tools_INVALID.html
                file_extension: str = file_name.split(".")[-1]
                if file_extension not in allowed_extensions:
                    return render_template(
                        "tools/tools_INVALID.html",
                        filename=file_name,
                        file_extension=file_extension,
                    )

                # if a file exceeds the size limit, return to tools_FILE_TOO_LARGE.html
                if file.content_length > max_file_size:
                    return render_template(
                        "tools/tools_FILE_TOO_LARGE.html",
                        filename=file_name,
                        file_extension=file_extension,
                    )

                # if not valid return to tools_INVALID.html
                if not validate_file(file.stream):
                    return render_template(
                        "tools/tools_INVALID.html",
                        filename=file_name,
                        file_extension=file_extension,
                    )

                # save file in upload folder
                file.save(uploads_dir + file_name)

            # when files are uploaded, go to the results page
            return redirect(url_for("tools.results"))
        # default tool page, to upload files
        case _:
            return render_template("tools/tools_GET.html", allowed_extensions=allowed_extensions)


@blueprint.route("/results", methods=["GET", "POST"])
def results() -> str | Response:
    """Tools results page.

    On this page the user can select the tools to run,
    and the files to run the tools on.

    Returns
    -------
    str
        The tools results page template.
    """
    # page where user can select tools and files
    match request.method:
        case HTTPMethod.POST:
            # get the selected files
            selected_files: list[str] = request.form.getlist("uploaded_file")
            if len(selected_files) == 0:
                return redirect(url_for("tools.index"))

            # create the class that can run wgd
            wgd = WgdManager(outdir, tmpdir)
            # run the dmd sub tool for each selected file
            result: CompletedProcess[str] = wgd.run_dmd(*selected_files)

            return render_template("tools/tools_RESULTS.html", files=selected_files, result=result)
        case _:
            filepaths: list[str] = get_filepaths_from_dir(uploads_dir)
            files: list[dict[str, str]] = []
            for filepath in filepaths:
                file: dict[str, str] = {
                    "filepath": filepath,
                    "filename": filepath.split("/")[-1],
                }
                files.append(file)
            return render_template("tools/tools_POST.html", files=files)


@blueprint.errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error: RequestEntityTooLarge) -> tuple[str, Literal[413]]:
    """When a file exceeds maximum allowed size.

    Parameters
    ----------
    error : RequestEntityTooLarge
        Error thrown.

    Returns
    -------
    tuple[str, Literal[413]]
        Error template and status code.
    """
    return render_template("tools/tools_FILE_TOO_LARGE.html"), 413
