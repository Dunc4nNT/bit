from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

blueprint: Blueprint = Blueprint("tools", __name__, url_prefix="/tools")

allowed_extensions = ["fasta"]
# sets max upload size to 500mb
max_file_size = 500 * 1024 * 1024
# max_file_size = 98_816

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


@blueprint.route("/", methods=["GET", "POST"])
def index() -> str:
    """Tools landing page.

    Returns
    -------
    str
        The tools landing page template.
    """
    # default tool page, to upload file(s)
    if request.method == "GET":
        return render_template("tools/tools_GET.html", allowed_extensions=allowed_extensions)

    # if submit button is pressed
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

    return render_template("tools/tools_POST.html", files=files)

@blueprint.errorhandler(RequestEntityTooLarge)
def request_entity_too_large(error):
    return render_template('tools/tools_FILE_TOO_LARGE.html'), 413
