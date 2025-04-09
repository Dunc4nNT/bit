"""Python file for the tool page.

Here the website user can upload files, use wgd, and view the output.
"""

from http import HTTPMethod
from pathlib import Path
from subprocess import CalledProcessError
from typing import TYPE_CHECKING, Literal

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from werkzeug import Response
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from bit.dirpaths import outdir, tmpdir, uploads_dir
from bit.forms import (
    DmdOptionsForm,
    FileUploadForm,
    KsdOptionsForm,
    SelectToolForm,
    VizOptionsForm,
)
from bit.wgd_manager import WgdManager

if TYPE_CHECKING:
    from subprocess import CompletedProcess


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
    # for each file in the directory
    # append it to a list
    filepaths_list: list[str] = [directory + file.name for file in Path(directory).iterdir()]

    return filepaths_list


def is_file_valid(file: FileStorage) -> bool:
    """Check if a file is more "likely" valid.

    Starts with >.

    Parameters
    ----------
    file : FileStorage
        File to check.

    Returns
    -------
    bool
        Whether the file is valid.
    """
    data: bytes = file.stream.read()
    file.stream.seek(0)

    return data.startswith(b">")


class InvalidFileError(Exception):
    """Uploaded file is invalid."""


@blueprint.route("/", methods=["GET", "POST"])
def index() -> str | Response:
    """Tools landing page.

    On this page the user can upload files

    Returns
    -------
    str | Response
        The tools landing page template.

    Raises
    ------
    RequestEntityTooLarge
        When the uploaded file is too large.
    InvalidFileError
        When the uploaded file invalid.
    """
    form = FileUploadForm(request.form)

    # get the already uploaded files
    filepaths: list[str] = get_filepaths_from_dir(uploads_dir)
    uploaded_files: list[dict[str, str]] = []
    for filepath in filepaths:
        uploaded_file: dict[str, str] = {
            "filepath": filepath,
            "filename": filepath.split("/")[-1],
        }
        uploaded_files.append(uploaded_file)

    # list of the allowed file types to upload
    if request.method == HTTPMethod.POST and form.validate():
        # if submit button is pressed for the file upload
        files: list[FileStorage] = request.files.getlist("files")

        if len(files) == 0:
            return redirect(url_for("tools.index"))

        # validate files
        for file in files:
            # if no files given, return to default tool page
            if not file.filename:
                flash("You must upload a file.", category="error")
                return redirect(url_for("tools.index"))

            file_name: str = secure_filename(file.filename)

            # if a file exceeds the size limit, return to tools_FILE_TOO_LARGE.html
            if file.content_length > current_app.config["MAX_CONTENT_LENGTH"]:
                raise RequestEntityTooLarge

            # if not valid return to tools_INVALID.html
            if not is_file_valid(file):
                raise InvalidFileError

            # save file in upload folder
            file.save(uploads_dir + file_name)

        # when files are uploaded, go to the results page
        return redirect(url_for("tools.select_tool"))

    # default tool page, to upload files
    return render_template("tools/index.html", form=form, uploaded_files=uploaded_files)


@blueprint.route("/select_tool", methods=["GET", "POST"])
def select_tool() -> str | Response:
    """Select which subtool to use.

    Returns
    -------
    str | Response
        The select tool page or the result from selecting one.
    """
    form = SelectToolForm(request.form)

    if request.method == HTTPMethod.POST and form.validate():
        redirects: dict[str, str] = {
            "dmd": "tools.dmd",
            "ksd": "tools.ksd",
            "viz": "tools.viz",
        }

        return redirect(url_for(redirects[form.tool.data]))

    return render_template("tools/select_tool.html", form=form)


@blueprint.route("/dmd", methods=["GET", "POST"])
def dmd() -> str | Response:
    """Run the dmd subtool.

    Returns
    -------
    str | Response
        Page to configure dmd, or see results from a run.
    """
    form = DmdOptionsForm(request.form)

    filepaths: list[str] = get_filepaths_from_dir(uploads_dir) + get_filepaths_from_dir(outdir)
    files: list[dict[str, str]] = []
    for filepath in filepaths:
        file: dict[str, str] = {
            "filepath": filepath,
            "filename": filepath.split("/")[-1],
        }
        files.append(file)

    form.sequences.choices = [(file["filepath"], file["filename"]) for file in files]
    form.anchorpoints.choices = [
        (None, ""),
        *[(file["filepath"], file["filename"]) for file in files],
    ]
    form.segments.choices = form.anchorpoints.choices
    form.listelements.choices = form.anchorpoints.choices
    form.genetable.choices = form.anchorpoints.choices
    form.seq2assign.choices = form.sequences.choices
    form.fam2assign.choices = form.anchorpoints.choices

    if request.method == HTTPMethod.POST and form.validate():
        selected_files: list[str] | None = form.sequences.data
        if not selected_files or len(selected_files) == 0:
            return redirect(url_for("tools.dmd"))

        # create the class that can run wgd
        wgd = WgdManager(outdir, tmpdir)
        # run the dmd sub tool for each selected file
        result: CompletedProcess[str] = wgd.run_dmd(
            *selected_files,
            **{
                key: value
                for key, value in form.data.items()
                if value is not None
                and key not in {"sequences", "submit"}
                and value != "None"
                and value
            },
        )

        output_files: list[str] = get_filepaths_from_dir(outdir)
        files: list[dict[str, str]] = []
        for filepath in output_files:
            if not filepath.endswith(".tsv"):
                continue

            file: dict[str, str] = {
                "filepath": filepath,
                "filename": filepath.split("/")[-1],
            }
            files.append(file)

        return render_template("tools/dmd_results.html", output_files=files, result=result)

    return render_template("tools/dmd.html", form=form)


@blueprint.route("/ksd", methods=["GET", "POST"])
def ksd() -> str | Response:
    """Run the ksd subtool.

    Returns
    -------
    str | Response
        Page to configure ksd, or see results from a run.
    """
    form = KsdOptionsForm(request.form)

    filepaths: list[str] = get_filepaths_from_dir(uploads_dir) + get_filepaths_from_dir(outdir)
    files: list[dict[str, str]] = []
    for filepath in filepaths:
        file: dict[str, str] = {
            "filepath": filepath,
            "filename": filepath.split("/")[-1],
        }
        files.append(file)

    form.families.choices = [(file["filepath"], file["filename"]) for file in files]
    form.sequences.choices = [(file["filepath"], file["filename"]) for file in files]

    form.speciestree.choices = [
        (None, ""),
        *[(file["filepath"], file["filename"]) for file in files],
    ]
    form.extraparanomeks.choices = form.speciestree.choices
    form.anchorpoints.choices = form.speciestree.choices

    if request.method == HTTPMethod.POST and form.validate():
        selected_files: list[str] | None = form.sequences.data
        if not selected_files or len(selected_files) == 0:
            return redirect(url_for("tools.ksd"))

        # create the class that can run wgd
        wgd = WgdManager(outdir, tmpdir)
        # run the dmd sub tool for each selected file
        result: CompletedProcess[str] = wgd.run_ksd(
            form.families.data,
            *selected_files,
            **{
                key: value
                for key, value in form.data.items()
                if value is not None
                and key not in {"families", "sequences", "submit"}
                and value != "None"
                and value
            },
        )

        output_files: list[str] = get_filepaths_from_dir(outdir)
        files: list[dict[str, str]] = []
        for filepath in output_files:
            if not filepath.endswith(".ks.tsv"):
                continue

            file: dict[str, str] = {
                "filepath": filepath,
                "filename": filepath.split("/")[-1],
            }
            files.append(file)

        return render_template("tools/ksd_results.html", output_files=files, result=result)

    return render_template("tools/ksd.html", form=form)


@blueprint.route("/viz", methods=["GET", "POST"])
def viz() -> str | Response:
    """Run the viz subtool.

    Returns
    -------
    str | Response
        Page to configure viz, or see results from a run.
    """
    form = VizOptionsForm(request.form)

    filepaths: list[str] = get_filepaths_from_dir(uploads_dir) + get_filepaths_from_dir(outdir)
    files: list[dict[str, str]] = []
    for filepath in filepaths:
        file: dict[str, str] = {
            "filepath": filepath,
            "filename": filepath.split("/")[-1],
        }
        files.append(file)

    form.data_file.choices = [(file["filepath"], file["filename"]) for file in files]

    form.gsmap.choices = [
        (None, ""),
        *[(file["filepath"], file["filename"]) for file in files],
    ]
    form.speciestree.choices = form.gsmap.choices
    form.segments.choices = form.gsmap.choices
    form.anchorpoints.choices = form.gsmap.choices
    form.multiplicon.choices = form.gsmap.choices
    form.genetable.choices = form.gsmap.choices
    form.extraparanomeks.choices = form.gsmap.choices

    if request.method == HTTPMethod.POST and form.validate():
        # create the class that can run wgd
        wgd = WgdManager(outdir, tmpdir)
        # run the dmd sub tool for each selected file
        result: CompletedProcess[str] | None = None
        try:
            result = wgd.run_viz(
                form.data_file.data,
                **{
                    key: value
                    for key, value in form.data.items()
                    if value is not None
                    and key not in {"data_file", "submit"}
                    and value != "None"
                    and value
                },
            )
        except CalledProcessError:
            pass

        output_files: list[str] = get_filepaths_from_dir(outdir)
        files: list[dict[str, str]] = []
        for filepath in output_files:
            if not filepath.endswith(".svg"):
                continue

            file: dict[str, str] = {
                "filepath": "/".join(filepath.split("/")[2:]),
                "filename": filepath.split("/")[-1],
            }
            files.append(file)

        return render_template("tools/viz_results.html", output_files=files, result=result)

    return render_template("tools/viz.html", form=form)


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
    flash("File is too large.", category="error")

    return render_template("errors/file_too_large.html"), 413


@blueprint.errorhandler(InvalidFileError)
def invalid_file_error(error: InvalidFileError) -> tuple[str, Literal[415]]:
    """When an uploaded file is invalid.

    Parameters
    ----------
    error : InvalidFileError
        Error thrown.

    Returns
    -------
    tuple[str, Literal[415]]
        Error template and status code.
    """
    flash("file is invalid.", category="error")

    return render_template("errors/invalid_file.html"), 415
  