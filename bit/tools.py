"""Python file for the tool page.

Here the website user can upload files, use wgd, and view the output.
"""

from http import HTTPMethod
from pathlib import Path
from subprocess import CalledProcessError
from typing import IO, TYPE_CHECKING, Literal

from flask import Blueprint, current_app, redirect, render_template, request, url_for
from werkzeug import Response
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
    # for each file in the directory
    # append it to a list
    filepaths_list: list[str] = [directory + file.name for file in Path(directory).iterdir()]

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


@blueprint.route("/", methods=["GET", "POST"])
def index() -> str | Response:
    """Tools landing page.

    On this page the user can upload files

    Returns
    -------
    str | Response
        The tools landing page template.
    """
    form = FileUploadForm(request.form)

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
                return redirect(url_for("tools.index"))

            file_name: str = secure_filename(file.filename)

            # if a file with an incorrect extension was given, return to tools_INVALID.html
            file_extension: str = file_name.split(".")[-1]

            # if a file exceeds the size limit, return to tools_FILE_TOO_LARGE.html
            if file.content_length > current_app.config["MAX_CONTENT_LENGTH"]:
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
        return redirect(url_for("tools.select_tool"))

    # default tool page, to upload files
    return render_template("tools/index.html", form=form)


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
        result: CompletedProcess[str] = wgd.run_ksd(form.families.data, *selected_files)

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

    if request.method == HTTPMethod.POST and form.validate():
        # create the class that can run wgd
        wgd = WgdManager(outdir, tmpdir)
        # run the dmd sub tool for each selected file
        result: CompletedProcess[str] | None = None
        try:
            result = wgd.run_viz(form.data_file.data)
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
    return render_template("tools/tools_FILE_TOO_LARGE.html"), 413
