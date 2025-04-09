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
        choices=[("", "choose tool"), ("dmd", "dmd"), ("ksd", "ksd"), ("viz", "viz")],
        validators=[InputRequired()],
    )
    submit = SubmitField("Submit")


class SelectVisualisationsForm(Form):
    """Select files to visualise."""

    files = SelectMultipleField("Files", validators=[InputRequired()])
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

    to_stop = BooleanField("Translate Through STOP Codons")
    cds = BooleanField("Only Translate Complete cds")
    pairwise = BooleanField("Initiate Pairwise Ks Estimation")
    strip_gaps = BooleanField("Drop Gaps in Multiple Sequence Alignment")
    aln_options = StringField("Alignment Options (comma separated)", validators=[Optional()])
    tree_options = StringField("Tree Inference Options (comma separated)", validators=[Optional()])
    node_average = BooleanField("Initiate Node-Average De-Redundancy")
    speciestree = SelectField("Speciestree File", validators=[Optional()])
    reweight = BooleanField("Recalculate Weight per Species Pair")
    onlyrootout = BooleanField("Only Use Outgroup at Root")
    extraparanomeks = SelectField("Extra Paranome Ks Data File", validators=[Optional()])
    anchorpoints = SelectField("Anchorpoints File", validators=[Optional()])
    plotkde = BooleanField("Plot kde Curve of Orthologous Ks Distribution over Histogram")
    plotapgmm = BooleanField("Perform and Plot Mixture Modeling of Anchor Ks")
    plotelmm = BooleanField("Perform and Plot ELMM Mixture Modeling of Paranome Ks")
    adjustortho = BooleanField("Adjust Histogram Height to Match Height of Paralogous Ks")
    adjustfactor = FloatField("Adjustment Factor of Orthologous Ks", validators=[Optional()])
    okalpha = FloatField("Opacity of Orthologous Ks Distribution", validators=[Optional()])
    kstree = BooleanField("Infer Ks Tree")
    onlyconcatkstree = BooleanField("Only Infer Ks Tree Under Concatenated Alignment")
    classic = BooleanField("Draw Full Orthologous Ks Distribution")
    toparrow = BooleanField(
        "Adjust the Arrow at the Top of the Plot, Instead of Being Coordinated as the KDE"
    )
    bootstrap = IntegerField("Number of Bootstrap Replicates", validators=[Optional()])

    submit = SubmitField("Submit")


class VizOptionsForm(Form):
    """Options for the viz subtool."""

    data_file = SelectField("Data File", validators=[InputRequired()])

    gsmap = SelectField("Gene Name-Species Name Map File", validators=[Optional()])
    speciestree = SelectField("Speciestree File", validators=[Optional()])
    plotkde = BooleanField("Plot kde Curve of Orthologous Ks Distribution over Histogram")
    reweight = BooleanField("Recalculate Weight per Species Pair")
    onlyrootout = BooleanField("Only Use Outgroup at Root")
    em_iterations = IntegerField("Maximum EM Iterations", validators=[Optional()])
    em_initializations = IntegerField("Maximum EM Initialisations", validators=[Optional()])
    prominence_cutoff = FloatField(
        "Prominance Cutoff of Acceptable Peaks", validators=[Optional()]
    )
    rel_height = FloatField(
        "Relative Height at Which Peak Width is Measured", validators=[Optional()]
    )
    segments = SelectField("Segments File", validators=[Optional()])
    minlen = IntegerField(
        "Minimum Length of a Scaffold to be Included in Dotplot", validators=[Optional()]
    )
    maxsize = IntegerField("Maximum Family Size to be Included", validators=[Optional()])
    anchorpoints = SelectField("Anchorpoints File", validators=[Optional()])
    multiplicon = SelectField("Multiplicons File", validators=[Optional()])
    genetable = SelectField("Gene Table File", validators=[Optional()])
    minseglen = IntegerField("Minimum Length of Segments to Include", validators=[Optional()])
    mingenenum = IntegerField(
        "Minimum Amount of Genes for a Segment to be Considered", validators=[Optional()]
    )
    keepredun = BooleanField("Keep Redundant Multiplicons")
    extraparanomeks = SelectField("Extra Paranome Ks Data File", validators=[Optional()])
    plotapgmm = BooleanField("Perform and Plot Mixture Modeling of Anchor Ks")
    plotelmm = BooleanField("Perform and Plot ELMM Mixture Modeling of Paranome Ks")
    plotsyn = BooleanField("Initiate Synteny Plotting")
    dotsize = FloatField("Dot Size", validators=[Optional()])
    apalpha = FloatField("Opacity of Anchor Dots", validators=[Optional()])
    hoalpha = FloatField("Opacity of Homolog Dots", validators=[Optional()])
    showrealtick = BooleanField("Show Real Tick in Genes or Bases")
    ticklabelsize = FloatField("Label Size of Tick", validators=[Optional()])
    adjustortho = BooleanField("Adjust Histogram Height to Match Height of Paralogous Ks")
    adjustfactor = FloatField("Adjustment Factor of Orthologous Ks", validators=[Optional()])
    okalpha = FloatField("Opacity of Orthologous Ks Distribution", validators=[Optional()])
    classic = BooleanField("Draw Full Orthologous Ks Distribution")
    toparrow = BooleanField(
        "Adjust the Arrow at the Top of the Plot, Instead of Being Coordinated as the KDE"
    )
    nodeaveraged = BooleanField("Use Node-Averaged De-Redundancy")
    bootstrap = IntegerField("Number of Bootstrap Replicates", validators=[Optional()])
    gistrb = BooleanField("Use gist_rainbow as Colourmap")

    submit = SubmitField("Submit")
