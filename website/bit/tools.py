from flask import Blueprint, render_template

blueprint: Blueprint = Blueprint("tools", __name__, url_prefix="/tools")


@blueprint.get("/")
def index() -> str:
    """Tools landing page.

    Returns
    -------
    str
        The tools landing page template.
    """
    return render_template("tools/index.html")
