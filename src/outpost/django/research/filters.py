from functools import reduce
from operator import or_

from django.db.models import Q
from django_filters import CharFilter
from django_filters.rest_framework import filterset

from . import models
from .conf import settings


class ProjectFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `organization`
      - `category`
      - `manager`
      - `contact`
      - `status`
      - `grant`
      - `research`
      - `study`
      - `language`
      - `funders`
      - `program`

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    All fields with advanced lookups can also be used for exact value matches
    as described above.

    Possible advanced lookups:

      - `begin_planned`: `gt`, `gte`, `lt`, `lte`
      - `begin_effective`: `gt`, `gte`, `lt`, `lte`
      - `end_planned`: `gt`, `gte`, `lt`, `lte`
      - `end_effective`: `gt`, `gte`, `lt`, `lte`
    """

    title = CharFilter(method="title_filter", label="Title")

    class Meta:
        model = models.Project
        fields = {
            "organization": ("exact",),
            "category": ("exact",),
            "manager": ("exact",),
            "contact": ("exact",),
            "status": ("exact",),
            "begin_planned": ("exact", "gt", "lt", "gte", "lte", "date"),
            "begin_effective": ("exact", "gt", "lt", "gte", "lte", "date"),
            "end_planned": ("exact", "gt", "lt", "gte", "lte", "date"),
            "end_effective": ("exact", "gt", "lt", "gte", "lte", "date"),
            "grant": ("exact",),
            "research": ("exact",),
            "event": ("exact",),
            "study": ("exact",),
            "language": ("exact",),
            "funders": ("exact",),
            "assignment": ("exact", "gt", "lt", "gte", "lte", "date"),
            "program": ("exact",),
        }

    def title_filter(self, queryset, name, value):
        f = reduce(
            or_,
            [
                Q(**{f"{name}__{lang}__icontains": value})
                for lang, _ in settings.LANGUAGES
            ],
        )
        return queryset.filter(f)


class PublicationFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `year`
      - `category`
      - `document`
      - `persons`

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    All fields with advanced lookups can also be used for exact value matches
    as described above.

    Possible advanced lookups:

      - `year`: `gt`, `gte`, `lt`, `lte`
      - `sci`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`
      - `pubmed`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`
      - `doi`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`
      - `pmc`: `iexact`, `contains`, `icontains`, `startswith`, `istartswith`
      - `organization_authorship`: `in`
      - `impact`: `isnull`, `gt`, `gte`, `lt`, `lte`
      - `imported`: `isnull`, `gt`, `gte`, `lt`, `lte`, `date`
    """

    class Meta:
        model = models.Publication
        fields = {
            "year": ("exact", "gt", "lt", "gte", "lte"),
            "category": ("exact",),
            "document_type": ("exact",),
            "sci": (
                "exact",
                "iexact",
                "contains",
                "icontains",
                "startswith",
                "istartswith",
            ),
            "pubmed": (
                "exact",
                "iexact",
                "contains",
                "icontains",
                "startswith",
                "istartswith",
            ),
            "doi": (
                "exact",
                "iexact",
                "contains",
                "icontains",
                "startswith",
                "istartswith",
            ),
            "pmc": (
                "exact",
                "iexact",
                "contains",
                "icontains",
                "startswith",
                "istartswith",
            ),
            "persons": ("exact",),
            "organizations": ("exact",),
            "impactfactor": (
                "exact",
                "isnull",
                "gt",
                "lt",
                "gte",
                "lte",
            ),
            "impactfactor_norm": (
                "exact",
                "isnull",
                "gt",
                "lt",
                "gte",
                "lte",
            ),
            "impactfactor_norm_super": (
                "exact",
                "isnull",
                "gt",
                "lt",
                "gte",
                "lte",
            ),
            "imported": (
                "exact",
                "isnull",
                "gt",
                "lt",
                "gte",
                "lte",
                "date",
            ),
        }

    @property
    def qs(self):
        qs = super().qs
        return qs


class PublicationPersonFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `publication`
      - `person`
      - `authorship`
      - `last_author`

    """

    class Meta:
        model = models.PublicationPerson
        fields = {
            "publication": ("exact",),
            "person": ("exact",),
            "authorship": ("exact",),
            "last_author": ("exact",),
        }


class BiddingDeadlineFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `bidding`

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    All fields with advanced lookups can also be used for exact value matches
    as described above.

    Possible advanced lookups:

      - `deadline`: `gt`, `gte`, `lt`, `lte`, `date`
    """

    class Meta:
        model = models.BiddingDeadline
        fields = {
            "bidding": ("exact",),
            "deadline": ("exact", "gt", "lt", "gte", "lte", "date"),
        }


class BiddingEndowmentFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `bidding`

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    All fields with advanced lookups can also be used for exact value matches
    as described above.

    Possible advanced lookups:

      - `amount`: `gt`, `gte`, `lt`, `lte`
    """

    class Meta:
        model = models.BiddingEndowment
        fields = {"bidding": ("exact",), "amount": ("exact", "gt", "lt", "gte", "lte")}


class BiddingFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `running`

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    All fields with advanced lookups can also be used for exact value matches
    as described above.

    Possible advanced lookups:

      - `title`: `iexact`, `contains`, `icontains`
      - `mode`: `iexact`, `contains`, `icontains`
      - `funders`: `in`
      - `start`: `gt`, `gte`, `lt`, `lte`, `date`
    """

    class Meta:
        model = models.Bidding
        fields = {
            "title": ("exact", "iexact", "contains", "icontains"),
            "mode": ("exact", "iexact", "contains", "icontains"),
            "running": ("exact",),
            "funders": ("exact",),
            "start": ("exact", "gt", "lt", "gte", "lte", "date"),
        }


class PartnerFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `running`

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    All fields with advanced lookups can also be used for exact value matches
    as described above.

    Possible advanced lookups:

      - `title`: `iexact`, `contains`, `icontains`
      - `mode`: `iexact`, `contains`, `icontains`
      - `funders`: `in`
      - `start`: `gt`, `gte`, `lt`, `lte`, `date`
    """

    class Meta:
        model = models.Partner
        fields = {
            "name": ("exact", "iexact", "contains", "icontains"),
            "short": ("exact", "iexact", "contains", "icontains"),
            "typeintellectualcapitalaccounting": ("exact",),
        }


class ClassificationFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `level`
    """

    class Meta:
        model = models.Classification
        fields = {
            "level": ("exact",),
        }


class ProjectStudyFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `active`
    """

    class Meta:
        model = models.ProjectStudy
        fields = {
            "active": ("exact",),
        }


class ProjectResearchFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `active`
    """

    class Meta:
        model = models.ProjectResearch
        fields = {
            "active": ("exact",),
        }


class ProjectFunctionFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `active`
    """

    class Meta:
        model = models.ProjectFunction
        fields = {
            "active": ("exact",),
        }


class FieldFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `active`
    """

    class Meta:
        model = models.Field
        fields = {
            "active": ("exact",),
        }


class LegalBasisFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `active`
    """

    class Meta:
        model = models.LegalBasis
        fields = {
            "active": ("exact",),
        }


class ProjectPersonFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `project`
      - `person`
      - `function`
    """

    class Meta:
        model = models.ProjectPerson
        fields = {
            "project": ("exact",),
            "person": ("exact",),
            "function": ("exact",),
        }


class ServiceProviderFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `active`
    """

    class Meta:
        model = models.ServiceProvider
        fields = {
            "active": ("exact",),
        }


class ServiceProviderContactFilter(filterset.FilterSet):
    """
    ## Filters

    To filter for exact value matches:

        ?<fieldname>=<value>

    Possible exact filters:

      - `serviceprovider`
    """

    class Meta:
        model = models.ServiceProviderContact
        fields = {
            "serviceprovider": ("exact",),
        }
