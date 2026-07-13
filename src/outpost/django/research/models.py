import logging
from textwrap import shorten

from django.contrib.gis.db import models
from django.contrib.postgres.fields import (
    ArrayField,
    HStoreField,
)
from django.db.models.signals import post_save
from django.utils.translation import get_language, gettext_lazy as _
from ordered_model.models import OrderedModel
from treebeard.al_tree import AL_Node

from .conf import settings

logger = logging.getLogger(__name__)


class MultiLanguage:
    @staticmethod
    def empty_default():
        return {lang: "" for lang, _ in settings.LANGUAGES}


class PredominantFunder(models.Model):
    """
    Predominant funder.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of predominant funder, defined by language.
    """

    name = HStoreField()

    def __str__(self):
        return self.name.get("de")


class LegalBasis(models.Model):
    """
    Legal basis.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of legal basis, defined by language.
    """

    name = HStoreField()
    active = models.BooleanField()

    def __str__(self):
        return self.name.get("de")


class Field(models.Model):
    """
    Research field.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of research field, defined by language.

    ### `short` (`string`)
    Short identifier.
    """

    name = HStoreField()
    active = models.BooleanField()

    def __str__(self):
        return self.name.get("de")


class ResearchType(models.Model):
    """
    Research type.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of research field, defined by language.
    """

    name = HStoreField()

    def __str__(self):
        return self.name.get("de")


class Classification(AL_Node):
    """
    Classification of a person as per (ÖFOS2012)[https://www.data.gv.at/katalog/dataset/stat_ofos-2012].

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of classification, defined by language.

    ### `persons` (`integer[]`)
    List of foreign keys to `campusonline/person`.
    """

    name = HStoreField()
    parent = models.ForeignKey(
        "self",
        models.SET_NULL,
        related_name="children_set",
        null=True,
        blank=True,
    )
    persons = models.ManyToManyField(
        "campusonline.Person",
        db_constraint=False,
        db_table="research_classification_person",
        related_name="classifications",
    )
    level = models.PositiveSmallIntegerField()

    node_order_by = ["id"]

    def __str__(self):
        return self.name.get("de")


class Expertise(models.Model):
    """
    Expertise of a person.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of expertise, defined by language.

    ### `person` (`integer`)
    Foreign key to `campusonline/person` this expertise applies to.
    """

    name = HStoreField()
    person = models.ForeignKey(
        "campusonline.Person",
        models.DO_NOTHING,
        db_constraint=False,
        related_name="expertise",
    )

    def __str__(self):
        return self.name.get("de")


class Knowledge(models.Model):
    """
    Knowledge of a person.data.gv.at/katalog/dataset/stat_ofos-2012].

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of knowledge, defined by language.

    ### `person` (`integer`)
    Foreign key to `campusonline/person` this knowledge applies to.
    """

    name = HStoreField()
    person = models.ForeignKey(
        "campusonline.Person",
        models.DO_NOTHING,
        db_constraint=False,
        related_name="knowledge",
    )

    def __str__(self):
        return self.name.get("de")


class Education(models.Model):
    """
    Education of a person.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of education, defined by language.

    ### `person` (`integer`)
    Foreign key to `campusonline/person` this education applies to.
    """

    name = HStoreField()
    person = models.ForeignKey(
        "campusonline.Person",
        models.DO_NOTHING,
        db_constraint=False,
        related_name="education",
    )

    def __str__(self):
        return self.name.get("de")


class Country(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of country, defined by language.

    ### `iso` (`object`)
    ISO codes of country.
    """

    name = HStoreField()
    iso = HStoreField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class Language(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of language.

    ### `iso` (`string`)
    ISO code of language.
    """

    name = HStoreField()
    iso = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self):
        return self.name.get("de")


class FunderCategory(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of funder category, defined by language.

    ### `short` (`string`)
    Short name of funder category.
    """

    name = models.CharField(max_length=256, blank=True, null=True)
    short = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return self.name


class Funder(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of funder, defined by language.

    ### `street` (`string`)
    Street address.

    ### `zipcode` (`string`)
    ZIP code.

    ### `city` (`string`)
    City.

    ### `country` (`integer`)
    Foreign key to [countries](../country).

    ### `category` (`integer`)
    Foreign key to [category](../funder:category).

    ### `url` (`string`)
    URL to website.

    ### `telephone` (`string`)
    Telephone number.

    ### `email` (`string`)
    Email address.

    ### `active` (`boolean`)
    Is funder active.

    ### `patron` (`boolean`)
    Has funder been classified as a sponsor at the Medical University of Graz (can be assigned as a sponsor to a research funding project).

    ### `patron_peer_review` (`boolean`)
    Is funder a provider with scientific peer review procedure, which at the Medical University of Graz is regarded as a sponsor of competitively acquired third-party funding for research funding projects.

    ### `patron_associate_professor` (`boolean`)
    Is funder a provider that is regarded at the Medical University of Graz as a funding provider of competitively acquired third-party funds for research funding projects (especially for the crediting of projects in evaluations of Assoz. Professors and the like).

    ### `typeintellectualcapitalaccounting` (`integer`)
    Foreign key to [type according to intellectual capital accounting](../funder:type:intellectualcapitalaccounting).

    ### `typestatisticsaustria` (`integer`)
    Foreign key to [type according to Statistic Austria](../funder:type:statisticsaustria).
    """

    name = models.CharField(max_length=256, blank=True, null=True)
    street = models.CharField(max_length=256, blank=True, null=True)
    zipcode = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    country = models.ForeignKey("Country", models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(
        "FunderCategory", models.SET_NULL, null=True, blank=True
    )
    url = models.CharField(max_length=256, blank=True, null=True)
    telephone = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    active = models.BooleanField()
    patron = models.BooleanField()
    patron_peer_review = models.BooleanField()
    patron_associate_professor = models.BooleanField()
    typeintellectualcapitalaccounting = models.ForeignKey(
        "FunderTypeIntellectualCapitalAccounting",
        models.SET_NULL,
        null=True,
        blank=True,
    )
    typestatisticsaustria = models.ForeignKey(
        "FunderTypeStatisticsAustria",
        models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        permissions = (
            ("view_funder_non_patron", _("View funders that are not a patron")),
        )

    def __str__(self):
        return self.name


class ProjectCategory(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project Category, defined by language.
    """

    name = HStoreField()
    third_party_funding_policy = models.BooleanField()

    def __str__(self):
        return self.name.get("de")


class ProjectType(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project Type, defined by language.
    """

    name = HStoreField()
    public = models.BooleanField()

    def __str__(self):
        return self.name.get("de")


class ProjectResearch(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project research type, defined by language.

    ### `active` (`boolean`)
    Is project research active.
    """

    name = HStoreField()
    active = models.BooleanField()

    def __str__(self):
        return self.name.get("de")


class ProjectFunction(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project function, defined by language.

    ### `active` (`boolean`)
    Is project function active.
    """

    name = HStoreField()
    active = models.BooleanField()

    def __str__(self):
        return self.name.get("de")


class ProjectPerson(models.Model):
    """
    ## Fields

    ### `project` (`integer`)
    Foreign key to [funder](../funder).

    ### `person` (`integer`)
    Foreign key to [funder](../funder).

    ### `function` (`integer`)
    Foreign key to [funder](../funder).
    """

    id = models.TextField(primary_key=True)
    project = models.ForeignKey(
        "Project",
        models.CASCADE,
        null=True,
        blank=True,
        related_name="persons",
    )
    person = models.ForeignKey(
        "campusonline.Person",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    function = models.ForeignKey(
        "ProjectFunction",
        models.CASCADE,
        null=True,
        blank=True,
        related_name="persons",
    )

    def __str__(self):
        return str(self.project)


class ProjectPartnerFunction(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project partner function, defined by language.
    """

    name = HStoreField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class ProjectStudy(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project study, defined by language.
    """

    name = HStoreField()
    active = models.BooleanField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class ProjectEvent(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project event, defined by language.
    """

    name = HStoreField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class ProjectGrant(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project grant, defined by language.
    """

    name = HStoreField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class ProjectStatus(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of project status.
    """

    name = models.CharField(max_length=256, blank=True, null=True)
    public = models.BooleanField()

    def __str__(self):
        return self.name


class Program(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of research program.

    ### `active` (`boolean`)
    Is research program active.

    ### `funder` (`integer`)
    Foreign key to [funder](../funder).
    """

    name = models.CharField(max_length=256, blank=True, null=True)
    active = models.BooleanField()
    funder = models.ForeignKey("Funder", models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.
    """

    organization = models.ForeignKey(
        "campusonline.Organization",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        "ProjectCategory", models.CASCADE, null=True, blank=True
    )
    type = models.ForeignKey("ProjectType", models.CASCADE, null=True, blank=True)
    short = models.CharField(max_length=256, blank=True, null=True)
    title = HStoreField()
    partner_function = models.ForeignKey(
        "ProjectPartnerFunction",
        models.CASCADE,
        null=True,
        blank=True,
    )
    manager = models.ForeignKey(
        "campusonline.Person",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    contact = models.ForeignKey(
        "campusonline.Person",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    status = models.ForeignKey("ProjectStatus", models.CASCADE, null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    abstract = HStoreField()
    begin_planned = models.DateTimeField(blank=True, null=True)
    begin_effective = models.DateTimeField(blank=True, null=True)
    end_planned = models.DateTimeField(blank=True, null=True)
    end_effective = models.DateTimeField(blank=True, null=True)
    grant = models.ForeignKey("ProjectGrant", models.SET_NULL, null=True, blank=True)
    research = models.ForeignKey(
        "ProjectResearch", models.SET_NULL, null=True, blank=True
    )
    event = models.ForeignKey("ProjectEvent", models.SET_NULL, null=True, blank=True)
    study = models.ForeignKey("ProjectStudy", models.SET_NULL, null=True, blank=True)
    language = models.ForeignKey("Language", models.SET_NULL, null=True, blank=True)
    funders = models.ManyToManyField(
        "Funder",
        db_table="research_project_funder",
        related_name="projects",
    )
    assignment = models.DateTimeField(blank=True, null=True)
    program = models.ForeignKey("Program", models.SET_NULL, null=True, blank=True)
    subprogram = models.TextField(blank=True, null=True)
    publish = models.BooleanField()
    visible = models.BooleanField()
    funder_projectcode = models.CharField(max_length=150, null=True, blank=True)
    ethics_committee = models.CharField(max_length=50, null=True, blank=True)
    gender_studies = models.BooleanField()
    clinical_trial = models.BooleanField()
    invesitgator_init = models.BooleanField()
    legalbasis = models.ForeignKey("LegalBasis", models.SET_NULL, null=True, blank=True)
    project_total_requested = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    project_total_approved = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    predominant_funder = models.ForeignKey(
        "PredominantFunder", models.SET_NULL, null=True, blank=True
    )
    project_management_accountable = models.ForeignKey(
        "campusonline.Person",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    internal_order = models.CharField(max_length=20, null=True, blank=True)
    parent = models.ForeignKey(
        "Project",
        models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    co_accountable = models.ForeignKey(
        "campusonline.Person",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    zmf_usage = models.BooleanField()
    biobank_usage = models.BooleanField()
    biomed_research = models.BooleanField()
    commercial = models.BooleanField()
    edudract_number = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class PublicationCategory(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of category, defined by language.
    """

    name = HStoreField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class PublicationDocument(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of publication document, defined by language.
    """

    name = HStoreField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class PublicationAuthorship(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of publication authorship, defined by language.
    """

    name = HStoreField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class PublicationOrganization(models.Model):
    """
    ## Fields

    ### `id` (`string`)
    Primary key.

    ### `name` (`object`)
    Names of publication authorship, defined by language.
    """

    id = models.CharField(max_length=256, primary_key=True)
    publication = models.ForeignKey(
        "Publication",
        models.CASCADE,
        null=True,
        blank=True,
        related_name="organizations",
    )
    organization = models.ForeignKey(
        "campusonline.Organization",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="publication_authorship",
    )
    authorship = models.ForeignKey(
        "PublicationAuthorship",
        models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.publication} ({self.organization})"


class PublicationPerson(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    publication = models.ForeignKey(
        "Publication",
        models.CASCADE,
        null=True,
        blank=True,
        related_name="persons",
    )
    person = models.ForeignKey(
        "campusonline.Person",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="publications",
    )
    authorship = models.ForeignKey(
        "PublicationAuthorship",
        models.SET_NULL,
        null=True,
        blank=True,
    )
    last_author = models.BooleanField()

    def __str__(self):
        return f"{self.publication} ({self.person})"


class Publication(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`string`)
    Name of doctoral school.

    ### `emails` (`string[]`)
    Contact emails.
    """

    title = models.CharField(max_length=1024, blank=True, null=True)
    authors = ArrayField(models.CharField(max_length=256), blank=True, null=True)
    year = models.PositiveSmallIntegerField()
    source = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        "PublicationCategory",
        models.SET_NULL,
        null=True,
        blank=True,
    )
    document_type = models.ForeignKey(
        "PublicationDocument",
        models.SET_NULL,
        null=True,
        blank=True,
    )
    sci = models.CharField(max_length=128, blank=True, null=True)
    pubmed = models.CharField(max_length=128, blank=True, null=True)
    doi = models.CharField(max_length=128, blank=True, null=True)
    pmc = models.CharField(max_length=128, blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    # persons = models.ManyToManyField(
    #    "campusonline.Person",
    #    db_table="research_publication_person",
    #    related_name="publications",
    # )
    imported = models.DateTimeField(blank=True, null=True)
    journal = models.TextField(blank=True, null=True)
    issn = models.CharField(max_length=20, blank=True, null=True)
    collection_publisher = models.TextField(blank=True, null=True)
    collection_title = models.TextField(blank=True, null=True)
    edition = models.CharField(max_length=50, blank=True, null=True)
    university = models.TextField(blank=True, null=True)
    country = models.ForeignKey(
        "Country",
        models.SET_NULL,
        null=True,
        blank=True,
    )
    case_report = models.BooleanField(blank=True, null=True)
    impactfactor = models.FloatField(blank=True, null=True)
    impactfactor_year = models.PositiveSmallIntegerField(blank=True, null=True)
    impactfactor_norm = models.FloatField(blank=True, null=True)
    impactfactor_norm_year = models.PositiveSmallIntegerField(blank=True, null=True)
    impactfactor_norm_category = models.TextField(blank=True, null=True)
    impactfactor_norm_super = models.FloatField(blank=True, null=True)
    impactfactor_norm_super_year = models.PositiveSmallIntegerField(
        blank=True, null=True
    )
    impactfactor_norm_super_category = models.TextField(blank=True, null=True)
    citations = models.PositiveIntegerField(blank=True, null=True)
    conference_name = models.TextField(blank=True, null=True)
    conference_place = models.TextField(blank=True, null=True)
    conference_international = models.BooleanField(blank=True, null=True)
    scientific_event = models.BooleanField(blank=True, null=True)
    invited_lecture = models.BooleanField(blank=True, null=True)
    keynote_speaker = models.BooleanField(blank=True, null=True)
    selected_presentation = models.BooleanField(blank=True, null=True)
    biobank_use = models.BooleanField(blank=True, null=True)
    bmf_use = models.BooleanField(blank=True, null=True)
    zmf_use = models.BooleanField(blank=True, null=True)
    local_affiliation = models.BooleanField(blank=True, null=True)

    def __str__(self):
        if self.title:
            return f"{self.pk}: {self.title}"
        if self.abstract:
            short = shorten(self.abstract, 30)
            return f"{self.pk}: {short}"
        return str(self.pk)


class Bidding(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `title` (`string`)
    Title of bidding.

    ### `short` (`string`)
    Short description of bidding.

    ### `description` (`string`)
    Full description of bidding.

    ### `mode` (`string`)
    Mode of submission.

    ### `url` (`string`)
    URL to web presence.

    ### `short` (`boolean`)
    Bidding running or not.

    ### `funders` (`integer[]`)
    List of foreign keys to funders for this bidding.
    """

    title = models.CharField(max_length=256, blank=True, null=True)
    short = models.TextField()
    description = models.TextField()
    mode = models.CharField(max_length=256, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    running = models.BooleanField()
    funders = models.ManyToManyField(
        "Funder",
        db_table="research_bidding_funder",
        related_name="biddings",
    )
    start = models.DateTimeField()

    def __str__(self):
        return self.title


class BiddingDeadline(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `bidding` (`integer`)
    Foreign key to bidding.

    ### `deadline` (`date`)
    Datetime of deadline.

    ### `time` (`string`)
    Time of deadline.

    ### `comment` (`string`)
    Generic comment.
    """

    bidding = models.ForeignKey("Bidding", models.DO_NOTHING, related_name="deadlines")
    deadline = models.DateTimeField()
    time = models.CharField(max_length=16, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.bidding} (Deadline: {self.deadline})"


class BiddingEndowment(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `bidding` (`integer`)
    Foreign key to bidding.

    ### `information` (`string`)
    Generic textual information.

    ### `amount` (`number`)
    Monetary amount of endowment.

    ### `currency` (`string`)
    Currency used to define amount.
    """

    bidding = models.ForeignKey("Bidding", models.DO_NOTHING, related_name="endowments")
    information = models.TextField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return f"{self.bidding} (Endowment)"


class Partner(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Name of partner.

    ### `short` (`string`)
    Short form of name.

    ### `street` (`string`)
    Street address of partner.

    ### `zipcode` (`string`)
    ZIP code of partner.

    ### `city` (`string`)
    City of partner.

    ### `typeintellectualcapitalaccounting` (`integer`)
    Foreign key to the [type of partner according to intellectual capital accounting](../partnertypeintellectualcapitalaccounting).

    ### `url` (`string`)
    URL to the homepage.

    ### `telephone` (`string`)
    Telephone number.

    ### `email` (`string`)
    Email address.

    ### `information` (`string`)
    General information.
    """

    name = models.CharField(max_length=256, blank=True, null=True)
    short = models.CharField(max_length=128, blank=True, null=True)
    street = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    typeintellectualcapitalaccounting = models.ForeignKey(
        "PartnerTypeIntellectualCapitalAccounting",
        models.CASCADE,
        blank=True,
        null=True,
    )
    url = models.URLField(max_length=512, blank=True, null=True)
    telephone = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    information = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class PartnerTypeIntellectualCapitalAccounting(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Name of the partner type according to intellectual capital accounting in multiple languages.
    """

    name = HStoreField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class FunderTypeIntellectualCapitalAccounting(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Name of the funder type according to intellectual capital accounting in multiple languages.
    """

    name = HStoreField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class FunderTypeStatisticsAustria(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Name of the funder type according to [Statistics Austria](https://www.statistik.at/web_en/statistics/index.html) in multiple languages.
    """

    name = HStoreField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class ServiceProvider(models.Model):
    campusonline = models.ForeignKey(
        "campusonline.Organization",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
    )
    alternate_name = HStoreField(
        default=MultiLanguage.empty_default, blank=True, null=True
    )
    notes = HStoreField(default=MultiLanguage.empty_default, blank=True, null=True)
    active = models.BooleanField()

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return str(self.name)

    @property
    def name(self):
        if self.campusonline:
            return self.campusonline.name
        return self.alternate_name


class ServiceProviderContact(models.Model):
    serviceprovider = models.ForeignKey(
        "ServiceProvider",
        models.CASCADE,
        related_name="contacts",
    )
    campusonline = models.ForeignKey(
        "campusonline.Person",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    alternate_name = models.CharField(max_length=1024, blank=True, null=True)
    alternate_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def name(self):
        if self.campusonline:
            return f"{self.campusonline.last_name}, {self.campusonline.first_name}"
        return self.alternate_name

    @property
    def email(self):
        if self.campusonline:
            return self.campusonline.email
        return self.alternate_email


class ProjectMentorContribution(OrderedModel):
    name = HStoreField(default=MultiLanguage.empty_default)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name.get("de")


class Sponsorship(OrderedModel):
    name = HStoreField(default=MultiLanguage.empty_default)
    active = models.BooleanField(default=False)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))
