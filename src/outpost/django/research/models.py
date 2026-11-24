import logging

from django.contrib.gis.db import models
from django.contrib.postgres.fields import HStoreField
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
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

    name = HStoreField(default=MultiLanguage.empty_default)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class LegalBasis(models.Model):
    """
    Legal basis.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of legal basis, defined by language.

    ### `active` (`boolean`)
    Is legal basis active.
    """

    name = HStoreField(default=MultiLanguage.empty_default)
    active = models.BooleanField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class Field(models.Model):
    """
    Research field.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of research field, defined by language.

    ### `active` (`boolean`)
    Is research field active.
    """

    name = HStoreField(default=MultiLanguage.empty_default)
    active = models.BooleanField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class ResearchType(models.Model):
    """
    Research type.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of research field, defined by language.
    """

    name = HStoreField(default=MultiLanguage.empty_default)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class Classification(AL_Node):
    """
    Classification of a person as per (ÖFOS2012)[https://www.data.gv.at/katalog/dataset/stat_ofos-2012].

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `classification_id` (`integer`)
    ID of classification.

    ### `name` (`object`)
    Names of classification, defined by language.

    ### `parent` (`integer`)
    Foreign key to parent classification.

    ### `level` (`integer`)
    Level of classification.
    """

    classification_id = models.PositiveIntegerField(unique=True)
    name = HStoreField(default=MultiLanguage.empty_default)
    parent = models.ForeignKey(
        "self",
        models.SET_NULL,
        related_name="children_set",
        null=True,
        blank=True,
    )
    level = models.PositiveSmallIntegerField()

    node_order_by = ["classification_id"]

    class Meta:
        ordering = ("classification_id", "level")

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class Country(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of country, defined by language.

    ### `group` (`integer`)
    Foreign key to `research/country:group` this country applies to.

    ### `iso` (`object`)
    ISO codes of country, defined by language.
    """

    name = HStoreField(default=MultiLanguage.empty_default)
    group = models.ForeignKey(
        "CountryGroup",
        models.SET_NULL,
        null=True,
        blank=True,
    )
    iso = HStoreField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class CountryGroup(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `group_id` (`integer`)
    ID of country group.

    ### `name` (`object`)
    Names of country group, defined by language.
    """

    group_id = models.PositiveIntegerField(unique=True)
    name = HStoreField(default=MultiLanguage.empty_default)

    class Meta:
        ordering = ("name",)

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

    name = HStoreField(default=MultiLanguage.empty_default)
    iso = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class Funder(AL_Node):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of funder, defined by language.

    ### `abbreviation` (`string`)
    Abbreviation of funder.

    ### `street` (`string`)
    Street address.

    ### `zipcode` (`string`)
    ZIP code.

    ### `city` (`string`)
    City.

    ### `country` (`integer`)
    Foreign key to [countries](../country).

    ### `url` (`string`)
    URL to website.

    ### `active` (`boolean`)
    Is funder active.

    ### `parent` (`integer`)
    Foreign key to parent funder.

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

    ### `note` (`string`)
    General notes
    """

    name = models.CharField(max_length=256, blank=True, null=True)
    abbreviation = models.CharField(max_length=256, blank=True, null=True)
    street = models.CharField(max_length=256, blank=True, null=True)
    zipcode = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=256, blank=True, null=True)
    country = models.ForeignKey("Country", models.SET_NULL, null=True, blank=True)
    url = models.CharField(max_length=256, blank=True, null=True)
    active = models.BooleanField(verbose_name="active organization")
    parent = models.ForeignKey(
        "self",
        models.SET_NULL,
        related_name="children_set",
        verbose_name="parent organization",
        null=True,
        blank=True,
    )
    patron = models.BooleanField(verbose_name="research funding agency")
    patron_peer_review = models.BooleanField(
        verbose_name="funding agency with peer review"
    )
    typeintellectualcapitalaccounting = models.ForeignKey(
        "FunderTypeIntellectualCapitalAccounting",
        models.SET_NULL,
        verbose_name="wibi classification",
        null=True,
        blank=True,
    )
    typestatisticsaustria = models.ForeignKey(
        "FunderTypeStatisticsAustria",
        models.SET_NULL,
        verbose_name="statistic austria classification",
        null=True,
        blank=True,
    )
    note = models.TextField(blank=True, null=True)

    node_order_by = ("name",)

    class Meta:
        ordering = ("name",)
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

    ### `third_party_funding_policy` (`boolean`)
    Is third party funding policy applicable.
    """

    name = HStoreField(default=MultiLanguage.empty_default)
    third_party_funding_policy = models.BooleanField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class ProjectType(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project Type, defined by language.

    ### `public` (`boolean`)
    Is project type public.
    """

    name = HStoreField(default=MultiLanguage.empty_default)
    public = models.BooleanField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


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

    name = HStoreField(default=MultiLanguage.empty_default)
    active = models.BooleanField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


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

    name = HStoreField(default=MultiLanguage.empty_default)
    active = models.BooleanField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class ProjectPartnerFunction(models.Model):
    """
    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of project partner function, defined by language.
    """

    name = HStoreField(default=MultiLanguage.empty_default)

    class Meta:
        ordering = ("name",)

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

    ### `active` (`boolean`)
    Is project study active.
    """

    name = HStoreField(default=MultiLanguage.empty_default)
    active = models.BooleanField()

    class Meta:
        ordering = ("name",)

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

    name = HStoreField(default=MultiLanguage.empty_default)

    class Meta:
        ordering = ("name",)

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

    name = HStoreField(default=MultiLanguage.empty_default)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


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

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


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

    ### `running` (`boolean`)
    Is bidding currently running.

    ### `funders` (`integer[]`)
    List of foreign keys to funders for this bidding.

    ### `start` (`datetime`)
    Start date of bidding.
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

    class Meta:
        ordering = ("title",)

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

    class Meta:
        ordering = ("bidding__title",)

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

    class Meta:
        ordering = ("bidding__title",)

    def __str__(self):
        return f"{self.bidding} (Endowment)"


class FunderTypeIntellectualCapitalAccounting(models.Model):
    """
    Funder type according to intellectual capital accounting.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `funder_type_id` (`integer`)
    ID of funder type.

    ### `name` (`object`)
    Name of the funder type according to intellectual capital accounting in multiple languages.
    """

    funder_type_id = models.PositiveIntegerField(unique=True)
    name = HStoreField(default=MultiLanguage.empty_default)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class FunderTypeStatisticsAustria(models.Model):
    """
    Funder type according to Statistics Austria.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `funder_type_id` (`integer`)
    ID of funder type.

    ### `name` (`object`)
    Name of the funder type according to [Statistics Austria](https://www.statistik.at/web_en/statistics/index.html) in multiple languages.
    """

    funder_type_id = models.PositiveIntegerField(unique=True)
    name = HStoreField(default=MultiLanguage.empty_default)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))


class ServiceProvider(models.Model):
    """
    Service provider (linked to campusonline organization).

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `campusonline` (`integer`)
    Foreign key to `campusonline/organization`.

    ### `alternate_name` (`object`)
    Alternate names of service provider, defined by language.

    ### `notes` (`object`)
    Notes about service provider, defined by language.

    ### `active` (`boolean`)
    Is service provider active.
    """

    campusonline = models.ForeignKey(
        "campusonline.Organization",
        models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
    )
    alternate_name = HStoreField(default=MultiLanguage.empty_default)
    notes = HStoreField(default=MultiLanguage.empty_default)
    active = models.BooleanField()

    class Meta:
        ordering = ("campusonline",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))

    @property
    def name(self):
        if self.campusonline:
            return self.campusonline.name
        return self.alternate_name


class ServiceProviderContact(models.Model):
    """
    Contact for a service provider.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `serviceprovider` (`integer`)
    Foreign key to [service provider](../serviceprovider).

    ### `campusonline` (`integer`)
    Foreign key to `campusonline/person` (contact person).

    ### `alternate_name` (`string`)
    Alternate name of contact.

    ### `alternate_email` (`string`)
    Alternate email of contact.
    """

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
        verbose_name="contactperson",
    )
    alternate_name = models.CharField(max_length=1024, blank=True, null=True)
    alternate_email = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ("serviceprovider",)

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
    """
    Project mentor contribution.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of mentor contribution, defined by language.

    ### `active` (`boolean`)
    Is mentor contribution active.

    ### `position` (`integer`)
    Order position.
    """

    name = HStoreField(default=MultiLanguage.empty_default)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return str(self.name)


class Sponsorship(OrderedModel):
    """
    Sponsorship.

    ## Fields

    ### `id` (`integer`)
    Primary key.

    ### `name` (`object`)
    Names of sponsorship, defined by language.

    ### `active` (`boolean`)
    Is sponsorship active.

    ### `position` (`integer`)
    Order position.
    """

    name = HStoreField(default=MultiLanguage.empty_default)
    active = models.BooleanField(default=False)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))
