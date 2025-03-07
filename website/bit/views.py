from flask import Blueprint, Response, current_app, render_template

blueprint: Blueprint = Blueprint("core", __name__)


@blueprint.get("/robots.txt")
def robots() -> Response:
    """robots.txt file for crawlers.

    Returns
    -------
    Response
        The robots.txt file.
    """
    return current_app.send_static_file("robots.txt")


@blueprint.get("/")
def index() -> str:
    """Landing page.

    Returns
    -------
    str
        The landing page template.
    """
    return render_template("index.html")


@blueprint.get("/about")
def about() -> str:
    """About page for information about the website.

    Returns
    -------
    str
        The about page template.
    """
    return render_template("about.html")


@blueprint.get("/background_reading")
def background_reading() -> str:
    """Page containing all the technical details required to use the website.

    Returns
    -------
    str
        The background reading page template.
    """
    return render_template("background_reading.html")
