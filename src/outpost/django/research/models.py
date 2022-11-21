import logging
from textwrap import shorten

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField, HStoreField
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from memoize import memoize

logger = logging.getLogger(__name__)


class Classification(models.Model):
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
    persons = models.ManyToManyField(
        "campusonline.Person",
        db_table="research_classification_person",
        db_constraint=False,
        related_name="classifications",
    )

    class Meta:
        managed = False
        db_table = "research_classification"

    class Refresh:
        interval = 86400

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

    class Meta:
        managed = False
        db_table = "research_expertise"

    class Refresh:
        interval = 86400

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

    class Meta:
        managed = False
        db_table = "research_knowledge"

    class Refresh:
        interval = 86400

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

    class Meta:
        managed = False
        db_table = "research_education"

    class Refresh:
        interval = 86400

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

    class Meta:
        managed = False
        db_table = "research_country"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


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

    name = models.CharField(max_length=256, blank=True, null=True)
    iso = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "research_language"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


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

    class Meta:
        managed = False
        db_table = "research_fundercategory"

    class Refresh:
        interval = 86400

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

    ### `patron` (`boolean`)
    Has funder been classified as a sponsor at the Medical University of Graz (can be assigned as a sponsor to a research funding project).

    ### `patron_peer_review` (`boolean`)
    Is funder a provider with scientific peer review procedure, which at the Medical University of Graz is regarded as a sponsor of competitively acquired third-party funding for research funding projects.

    ### `patron_ssociate_professor` (`boolean`)
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
    country = models.ForeignKey(
        "Country", models.SET_NULL, db_constraint=False, null=True, blank=True
    )
    category = models.ForeignKey(
        "FunderCategory", models.SET_NULL, db_constraint=False, null=True, blank=True
    )
    url = models.CharField(max_length=256, blank=True, null=True)
    telephone = models.CharField(max_length=256, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    patron = models.BooleanField()
    patron_peer_review = models.BooleanField()
    patron_associate_professor = models.BooleanField()
    typeintellectualcapitalaccounting = models.ForeignKey(
        "FunderTypeIntellectualCapitalAccounting",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
    )
    typestatisticsaustria = models.ForeignKey(
        "FunderTypeStatisticsAustria",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
    )

    class Meta:
        managed = False
        db_table = "research_funder"
        permissions = (
            ("view_funder_non_patron", _("View funders that are not a patron")),
        )

    class Refresh:
        interval = 86400

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

    name = models.CharField(max_length=256, blank=True, null=True)
    public = models.BooleanField()

    class Meta:
        managed = False
        db_table = "research_projectcategory"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


class DjangoProjectCategory(models.Model):
    id = models.OneToOneField(
        "ProjectCategory",
        models.DO_NOTHING,
        db_column="id",
        db_constraint=False,
        related_name="+",
        primary_key=True,
    )
    public = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @classmethod
    def update(cls, **kwargs):
        from outpost.django.base.models import MaterializedView
        from outpost.django.base.tasks import MaterializedViewTasks

        try:
            mv = MaterializedView.objects.get(name=cls.id.field.related_model._meta.db_table)
        except MaterializedView.DoesNotExist:
            logger.warn(f"No materialized view object found for {cls.id.field.related_model._meta.db_table}")
            return
        MaterializedViewTasks.refresh.apply_async((mv.pk,), queue="maintainance")


post_save.connect(DjangoProjectCategory.update, sender=DjangoProjectCategory)


class ProjectResearch(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project research type, defined by language.
    """

    name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "research_projectresearch"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


class ProjectPartnerFunction(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project partner function, defined by language.
    """

    name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "research_projectpartnerfunction"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


class ProjectStudy(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project study, defined by language.
    """

    name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "research_projectstudy"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


class ProjectEvent(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project event, defined by language.
    """

    name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "research_projectevent"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


class ProjectGrant(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project grant, defined by language.
    """

    name = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "research_projectgrant"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


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

    class Meta:
        managed = False
        db_table = "research_projectstatus"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


class DjangoProjectStatus(models.Model):
    id = models.OneToOneField(
        "ProjectStatus",
        models.DO_NOTHING,
        db_column="id",
        db_constraint=False,
        related_name="+",
        primary_key=True,
    )
    public = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @classmethod
    def update(cls, **kwargs):
        from outpost.django.base.models import MaterializedView
        from outpost.django.base.tasks import MaterializedViewTasks

        try:
            mv = MaterializedView.objects.get(name=cls.id.field.related_model._meta.db_table)
        except MaterializedView.DoesNotExist:
            logger.warn(f"No materialized view object found for {cls.id.field.related_model._meta.db_table}")
            return
        MaterializedViewTasks.refresh.apply_async((mv.pk,), queue="maintainance")


post_save.connect(DjangoProjectStatus.update, sender=DjangoProjectStatus)


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
    funder = models.ForeignKey(
        "Funder", models.DO_NOTHING, db_constraint=False, null=True, blank=True
    )

    class Meta:
        managed = False
        db_table = "research_program"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project function, defined by language.
    """

    organization = models.ForeignKey(
        "campusonline.Organization",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        "ProjectCategory", models.SET_NULL, db_constraint=False, null=True, blank=True
    )
    short = models.CharField(max_length=256, blank=True, null=True)
    title = HStoreField()
    partner_function = models.ForeignKey(
        "ProjectPartnerFunction",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    manager = models.ForeignKey(
        "campusonline.Person",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    contact = models.ForeignKey(
        "campusonline.Person",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="+",
    )
    status = models.ForeignKey(
        "ProjectStatus", models.SET_NULL, db_constraint=False, null=True, blank=True
    )
    url = models.URLField(blank=True, null=True)
    abstract = HStoreField()
    begin_planned = models.DateTimeField(blank=True, null=True)
    begin_effective = models.DateTimeField(blank=True, null=True)
    end_planned = models.DateTimeField(blank=True, null=True)
    end_effective = models.DateTimeField(blank=True, null=True)
    grant = models.ForeignKey(
        "ProjectGrant", models.SET_NULL, db_constraint=False, null=True, blank=True
    )
    research = models.ForeignKey(
        "ProjectResearch", models.SET_NULL, db_constraint=False, null=True, blank=True
    )
    event = models.ForeignKey(
        "ProjectEvent", models.SET_NULL, db_constraint=False, null=True, blank=True
    )
    study = models.ForeignKey(
        "ProjectStudy", models.SET_NULL, db_constraint=False, null=True, blank=True
    )
    language = models.ForeignKey(
        "Language", models.SET_NULL, db_constraint=False, null=True, blank=True
    )
    funders = models.ManyToManyField(
        "Funder",
        db_table="research_project_funder",
        db_constraint=False,
        related_name="projects",
    )
    assignment = models.DateTimeField(blank=True, null=True)
    program = models.ForeignKey(
        "Program", models.SET_NULL, db_constraint=False, null=True, blank=True
    )
    subprogram = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "research_project"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.title.get("de")


class PublicationCategory(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of category, defined by language.
    """

    name = HStoreField()

    class Meta:
        managed = False
        db_table = "research_publicationcategory"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get("de")


class PublicationDocument(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of publication document, defined by language.
    """

    name = HStoreField()

    class Meta:
        managed = False
        db_table = "research_publicationdocument"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get("de")


class PublicationAuthorship(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of publication authorship, defined by language.
    """

    name = HStoreField()

    class Meta:
        managed = False
        db_table = "research_publicationauthorship"

    class Refresh:
        interval = 86400

    def __str__(self):
        return self.name.get("de")


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
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="organization_authorship",
    )
    organization = models.ForeignKey(
        "campusonline.Organization",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        related_name="publication_authorship",
    )
    authorship = models.ForeignKey(
        "PublicationAuthorship",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    assigned = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "research_publicationorganization"

    class Refresh:
        interval = 86400

    def __str__(self):
        return f"{self.publication} ({self.organization})"


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

    title = models.CharField(max_length=256, blank=True, null=True)
    authors = ArrayField(models.CharField(max_length=256))
    year = models.PositiveSmallIntegerField()
    source = models.TextField()
    category = models.ForeignKey(
        "PublicationCategory",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    document = models.ForeignKey(
        "PublicationDocument",
        models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
    )
    sci = models.CharField(max_length=128, blank=True, null=True)
    pubmed = models.CharField(max_length=128, blank=True, null=True)
    doi = models.CharField(max_length=128, blank=True, null=True)
    pmc = models.CharField(max_length=128, blank=True, null=True)
    abstract_bytes = models.BinaryField(blank=True, null=True)
    persons = models.ManyToManyField(
        "campusonline.Person",
        db_table="research_publication_person",
        db_constraint=False,
        related_name="publications",
    )
    impact = models.FloatField()
    imported = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "research_publication"

    class Refresh:
        interval = 3600

    @property
    @memoize(timeout=3600)
    def abstract(self):
        if not self.abstract_bytes:
            return None
        return self.abstract_bytes.tobytes().decode("utf-8").strip()

    def __repr__(self):
        return str(self.pk)

    def __str__(self):
        if not self.abstract_bytes:
            return str(self.pk)
        short = shorten(self.abstract, 30)
        return f"{self.pk}: {short}"


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
        db_constraint=False,
        related_name="biddings",
    )
    start = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "research_bidding"

    class Refresh:
        interval = 3600

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

    bidding = models.ForeignKey(
        "Bidding", models.DO_NOTHING, db_constraint=False, related_name="deadlines"
    )
    deadline = models.DateTimeField()
    time = models.CharField(max_length=16, blank=True, null=True)
    comment = models.TextField()

    class Meta:
        managed = False
        db_table = "research_biddingdeadline"

    class Refresh:
        interval = 86400

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

    bidding = models.ForeignKey(
        "Bidding", models.DO_NOTHING, db_constraint=False, related_name="endowments"
    )
    information = models.TextField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "research_biddingendowment"

    class Refresh:
        interval = 86400

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
        models.DO_NOTHING,
        db_constraint=False,
    )
    url = models.CharField(max_length=128, blank=True, null=True)
    telephone = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    information = models.TextField()

    class Meta:
        managed = False
        db_table = "research_partner"

    class Refresh:
        interval = 86400

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

    class Meta:
        managed = False
        db_table = "research_partnertypeintellectualcapitalaccounting"

    class Refresh:
        interval = 86400

    def __str__(self):
        return next((n for n in self.name if n is not None), _("Unknown"))


class FunderTypeIntellectualCapitalAccounting(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Name of the funder type according to intellectual capital accounting in multiple languages.
    """

    name = HStoreField()

    class Meta:
        managed = False
        db_table = "research_fundertypeintellectualcapitalaccounting"

    class Refresh:
        interval = 86400

    def __str__(self):
        return next((n for n in self.name if n is not None), _("Unknown"))


class FunderTypeStatisticsAustria(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Name of the funder type according to [Statistics Austria](https://www.statistik.at/web_en/statistics/index.html) in multiple languages.
    """

    name = HStoreField()

    class Meta:
        managed = False
        db_table = "research_fundertypestatisticsaustria"

    class Refresh:
        interval = 86400

    def __str__(self):
        return next((n for n in self.name if n is not None), _("Unknown"))
