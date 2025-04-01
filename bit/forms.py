from wtforms import Form, MultipleFileField, SelectField, SelectMultipleField, SubmitField
from wtforms.validators import InputRequired


class FileUploadForm(Form):
    """Upload any file."""

    files = MultipleFileField("Files")
    submit = SubmitField("Submit")


class SelectToolForm(Form):
    """Selection for a wgd subtool."""

    tool = SelectField(
        "Tool",
        choices=[("dmd", "dmd"), ("ksd", "ksd"), ("viz", "viz")],
        validators=[InputRequired()],
    )
    submit = SubmitField("Submit")


class DmdOptionsForm(Form):
    """Options for the dmd subtool."""

    sequences = SelectMultipleField("Genome cds Files", validators=[InputRequired()])
    submit = SubmitField("Submit")


class KsdOptionsForm(Form):
    """Options for the ksd subtool."""

    families = SelectField("Families File", validators=[InputRequired()])
    sequences = SelectMultipleField("Genome cds Files", validators=[InputRequired()])
    submit = SubmitField("Submit")


class VizOptionsForm(Form):
    """Options for the viz subtool."""

    data_file = SelectField("Data File", validators=[InputRequired()])
    submit = SubmitField("Submit")
