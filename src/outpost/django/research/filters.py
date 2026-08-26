from functools import reduce
from operator import or_

from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django_filters import CharFilter
from django_filters.rest_framework import filterset

from . import models
from .conf import settings


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


class ProjectMentorContributionFilter(filterset.FilterSet):
    """
    ## Filters

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    All fields with advanced lookups can also be used for exact value matches
    as described above.

    Possible advanced lookups:

      - `name`: `iexact`, `contains`, `icontains`
    """

    name = CharFilter(method="name_filter", label=_("Name"), lookup_expr="icontains")

    class Meta:
        model = models.ProjectMentorContribution
        fields = {}

    def name_filter(self, queryset, name, value):
        lookup = self.filters.get(name).lookup_expr
        f = reduce(
            or_,
            [
                Q(**{f"{name}__{lang}__{lookup}": value})
                for lang, _ in settings.LANGUAGES
            ],
        )
        return queryset.filter(f)


class SponsorshipFilter(filterset.FilterSet):
    """
    ## Filters

    For advanced filtering use lookups:

        ?<fieldname>__<lookup>=<value>

    All fields with advanced lookups can also be used for exact value matches
    as described above.

    Possible advanced lookups:

      - `name`: `iexact`, `contains`, `icontains`
    """

    name = CharFilter(method="name_filter", label=_("Name"), lookup_expr="icontains")

    class Meta:
        model = models.Sponsorship
        fields = {}

    def name_filter(self, queryset, name, value):
        lookup = self.filters.get(name).lookup_expr
        f = reduce(
            or_,
            [
                Q(**{f"{name}__{lang}__{lookup}": value})
                for lang, _ in settings.LANGUAGES
            ],
        )
        return queryset.filter(f)
