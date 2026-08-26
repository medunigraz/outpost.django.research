import logging
from textwrap import shorten

from django.contrib.gis.db import models
from django.contrib.postgres.fields import (
    ArrayField,
    HStoreField,
)
from django.db.models.signals import post_save
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

    name = HStoreField()

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
    """

    name = HStoreField()
    active = models.BooleanField()

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

    ### `short` (`string`)
    Short identifier.
    """

    name = HStoreField()
    active = models.BooleanField()

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

    name = HStoreField()

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
    """

    name = HStoreField()
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
    """

    name = HStoreField()
    public = models.BooleanField()

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

    name = HStoreField()
    active = models.BooleanField()

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

    name = HStoreField()
    active = models.BooleanField()

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
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return str(self.name)


class Sponsorship(OrderedModel):
    name = HStoreField(default=MultiLanguage.empty_default)
    active = models.BooleanField(default=False)

    def __str__(self):
        lang = get_language()
        if lang in self.name:
            return self.name.get(lang)
        return self.name.get(settings.LANGUAGE_CODE, next(self.names.values()))
