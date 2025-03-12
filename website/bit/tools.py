from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
blueprint: Blueprint = Blueprint("tools", __name__, url_prefix="/tools")

@blueprint.route("/", methods=["GET", "POST"])
def index() -> str:
    """Tools landing page.

    Returns
    -------
    str
        The tools landing page template.
    """
    # default tool page, to upload file
    if request.method == "GET":
        return render_template("tools/tools_GET.html")

    # if file is uploaded
    elif request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)  # SECURE filename
        file_extension = filename.split(".")[-1]
        # if no file uploaded, return to default tool page
        if filename == "":
            return render_template("tools/tools_GET.html")
        if file_extension != "fasta":
            return render_template("tools/tools_INVALID.html", file_extension=file_extension)
        return render_template("tools/tools_POST.html", filename=filename)
