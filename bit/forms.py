from wtforms import (
    BooleanField,
    FloatField,
    Form,
    IntegerField,
    MultipleFileField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.validators import InputRequired, NumberRange, Optional


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
    cscore = FloatField("C-score", validators=[Optional(), NumberRange(0, 1)])
    prot = BooleanField("Is protein sequence", validators=[Optional()])
    inflation = FloatField("MCL Inflation Factor", validators=[Optional()])
    eval = FloatField("E-value Cutoff", validators=[Optional()])
    to_stop = BooleanField("Translate Through STOP Codons")
    cds = BooleanField("Only Translate Complete cds")
    focus = StringField("Focus Species", validators=[Optional()])
    anchorpoints = SelectField("Anchorpoints File", validators=[Optional()])
    segments = SelectField("Segments File", validators=[Optional()])
    listelements = SelectField("Listsegments File", validators=[Optional()])
    genetable = SelectField("Gene Table File", validators=[Optional()])
    collinearcoalescence = BooleanField("Initiate Collinear Coalescence Analysis")
    keepfasta = BooleanField("Output Sequence Information")
    keepduplicates = BooleanField("Allow Duplicate Genes in Different MRBHs")
    globalmrbh = BooleanField("Initiate Global MRBH Construction")
    orthoinfer = BooleanField("Initiate Orthogroup Inference")
    onlyortho = BooleanField("Only Conduct Orthogroup Inference")
    getnsog = BooleanField("Search for Nested Single-Copy Gene Families")
    msogcut = FloatField(
        "Ratio Cutoff for Mostly Single-Copy Family and Species Representation",
        validators=[Optional()],
    )
    geneassign = BooleanField("Initiate Gene-to-Family Assignment Analysis")
    seq2assign = SelectMultipleField("Queried Sequence Data Files", validators=[Optional()])
    fam2assign = SelectField("Queried Family Data File", validators=[Optional()])
    concat = BooleanField("Initiate Concatenation Pipeline for Orthogroup Inference")
    testsog = BooleanField("Initiate Unbiased Test of Single-Copy Gene Families")
    bins = IntegerField(
        "Number of Bins Divided in Gene Length Normalisation", validators=[Optional()]
    )
    normalizedpercent = IntegerField(
        "Percentage of Upper Hits Used for Gene Length Normalisation", validators=[Optional()]
    )
    nonormalization = BooleanField("No Normalisation")
    ogformat = BooleanField("Add Index to RBH Families")

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
