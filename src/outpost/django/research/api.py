from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from outpost.django.base.decorators import docstring_format
from outpost.django.base.filters import SimpleDjangoFilterBackend
from outpost.django.base.mixins import CacheResponseMixin
from rest_flex_fields.views import FlexFieldsMixin
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.viewsets import ReadOnlyModelViewSet

from . import (
    filters,
    key_constructors,
    models,
    serializers,
)
from .conf import settings


@docstring_format(
    model=models.PredominantFunder.__doc__,
    serializer=serializers.PredominantFunderSerializer.__doc__,
)
class PredominantFunderViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List predominant funders.

    {model}
    {serializer}
    """

    queryset = models.PredominantFunder.objects.all()
    serializer_class = serializers.PredominantFunderSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.LegalBasis.__doc__,
    serializer=serializers.LegalBasisSerializer.__doc__,
    filter=filters.LegalBasisFilter.__doc__,
)
class LegalBasisViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List legal basis.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.LegalBasis.objects.all()
    serializer_class = serializers.LegalBasisSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = filters.LegalBasisFilter


@docstring_format(
    model=models.Field.__doc__,
    serializer=serializers.FieldSerializer.__doc__,
    filter=filters.FieldFilter.__doc__,
)
class FieldViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List research fields.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.Field.objects.all()
    serializer_class = serializers.FieldSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = filters.FieldFilter


@docstring_format(
    model=models.Country.__doc__, serializer=serializers.CountrySerializer.__doc__
)
class CountryViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List countries.

    {model}
    {serializer}
    """

    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.Language.__doc__, serializer=serializers.LanguageSerializer.__doc__
)
class LanguageViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List languages.

    {model}
    {serializer}
    """

    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.Program.__doc__, serializer=serializers.ProgramSerializer.__doc__
)
class ProgramViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List programs.

    {model}
    {serializer}
    """

    queryset = models.Program.objects.all()
    serializer_class = serializers.ProgramSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.Classification.__doc__,
    serializer=serializers.ClassificationSerializer.__doc__,
    filter=filters.ClassificationFilter.__doc__,
)
class ClassificationViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List OESTAT 2012 classifications.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.Classification.objects.all()
    serializer_class = serializers.ClassificationSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = filters.ClassificationFilter


@docstring_format(
    model=models.FunderTypeIntellectualCapitalAccounting.__doc__,
    serializer=serializers.FunderTypeIntellectualCapitalAccountingSerializer.__doc__,
)
class FunderTypeIntellectualCapitalAccountingViewSet(
    CacheResponseMixin, ReadOnlyModelViewSet
):
    """
    List funder types according to intellectual capital accounting.

    {model}
    {serializer}
    """

    queryset = models.FunderTypeIntellectualCapitalAccounting.objects.all()
    serializer_class = serializers.FunderTypeIntellectualCapitalAccountingSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.FunderTypeStatisticsAustria.__doc__,
    serializer=serializers.FunderTypeStatisticsAustriaSerializer.__doc__,
)
class FunderTypeStatisticsAustriaViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List funder types according to Statistics Austria.

    {model}
    {serializer}
    """

    queryset = models.FunderTypeStatisticsAustria.objects.all()
    serializer_class = serializers.FunderTypeStatisticsAustriaSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.Funder.__doc__, serializer=serializers.FunderSerializer.__doc__
)
class FunderViewSet(CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List funders.

    {model}
    {serializer}
    """

    queryset = models.Funder.objects.all()
    serializer_class = serializers.FunderSerializer
    permission_classes = (AllowAny,)
    permit_list_expands = (
        "country",
        "typeintellectualcapitalaccounting",
        "typestatisticsaustria",
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.has_perm("research.view_funder_non_patron"):
            return queryset
        else:
            return queryset.filter(patron=True)


@docstring_format(
    model=models.ProjectCategory.__doc__,
    serializer=serializers.ProjectCategorySerializer.__doc__,
)
class ProjectCategoryViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List project categories.

    {model}
    {serializer}
    """

    queryset = models.ProjectCategory.objects.all()
    serializer_class = serializers.ProjectCategorySerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.ProjectType.__doc__,
    serializer=serializers.ProjectTypeSerializer.__doc__,
)
class ProjectTypeViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List project types.

    {model}
    {serializer}
    """

    queryset = models.ProjectType.objects.all()
    serializer_class = serializers.ProjectTypeSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.ProjectResearch.__doc__,
    serializer=serializers.ProjectResearchSerializer.__doc__,
    filter=filters.ProjectResearchFilter.__doc__,
)
class ProjectResearchViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List project research.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.ProjectResearch.objects.all()
    serializer_class = serializers.ProjectResearchSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = filters.ProjectResearchFilter


@docstring_format(
    model=models.ProjectFunction.__doc__,
    serializer=serializers.ProjectFunctionSerializer.__doc__,
    filter=filters.ProjectFunctionFilter.__doc__,
)
class ProjectFunctionViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List project functions.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.ProjectFunction.objects.all()
    serializer_class = serializers.ProjectFunctionSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = filters.ProjectFunctionFilter


@docstring_format(
    model=models.ProjectPartnerFunction.__doc__,
    serializer=serializers.ProjectPartnerFunctionSerializer.__doc__,
)
class ProjectPartnerFunctionViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List project partner functions.

    {model}
    {serializer}
    """

    queryset = models.ProjectPartnerFunction.objects.all()
    serializer_class = serializers.ProjectPartnerFunctionSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.ProjectStudy.__doc__,
    serializer=serializers.ProjectStudySerializer.__doc__,
    filter=filters.ProjectStudyFilter.__doc__,
)
class ProjectStudyViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List project studies.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.ProjectStudy.objects.all()
    serializer_class = serializers.ProjectStudySerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = filters.ProjectStudyFilter


@docstring_format(
    model=models.ProjectEvent.__doc__,
    serializer=serializers.ProjectEventSerializer.__doc__,
)
class ProjectEventViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List project events.

    {model}
    {serializer}
    """

    queryset = models.ProjectEvent.objects.all()
    serializer_class = serializers.ProjectEventSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.ProjectGrant.__doc__,
    serializer=serializers.ProjectGrantSerializer.__doc__,
)
class ProjectGrantViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List project grants.

    {model}
    {serializer}
    """

    queryset = models.ProjectGrant.objects.all()
    serializer_class = serializers.ProjectGrantSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.BiddingDeadline.__doc__,
    serializer=serializers.BiddingDeadlineSerializer.__doc__,
    filter=filters.BiddingDeadlineFilter.__doc__,
)
class BiddingDeadlineViewSet(CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List bidding deadlines.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.BiddingDeadline.objects.all()
    serializer_class = serializers.BiddingDeadlineSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = filters.BiddingDeadlineFilter
    ordering_fields = ("deadline",)
    permission_classes = (AllowAny,)
    permit_list_expands = ("deadline",)


@docstring_format(
    model=models.BiddingEndowment.__doc__,
    serializer=serializers.BiddingEndowmentSerializer.__doc__,
    filter=filters.BiddingEndowmentFilter.__doc__,
)
class BiddingEndowmentViewSet(
    CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet
):
    """
    List bidding endowments.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.BiddingEndowment.objects.all()
    serializer_class = serializers.BiddingEndowmentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.BiddingEndowmentFilter
    permission_classes = (AllowAny,)
    permit_list_expands = ("bidding",)


@docstring_format(
    model=models.Bidding.__doc__,
    serializer=serializers.BiddingSerializer.__doc__,
    filter=filters.BiddingFilter.__doc__,
)
class BiddingViewSet(CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List biddings.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.Bidding.objects.all()
    serializer_class = serializers.BiddingSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = filters.BiddingFilter
    ordering_fields = ("start",)
    permission_classes = (AllowAny,)
    permit_list_expands = ("funders", "deadlines", "endowments")

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("funders", "deadlines", "endowments")
        return queryset


@docstring_format(
    model=models.ServiceProvider.__doc__,
    filter=filters.ServiceProviderFilter.__doc__,
    serializer=serializers.ServiceProviderSerializer.__doc__,
)
class ServiceProviderViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List service providers.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.ServiceProvider.objects.all()
    serializer_class = serializers.ServiceProviderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.ServiceProviderFilter
    permission_classes = (AllowAny,)
    permit_list_expands = ("contacts", "campusonline")


@docstring_format(
    model=models.ServiceProviderContact.__doc__,
    filter=filters.ServiceProviderContactFilter.__doc__,
    serializer=serializers.ServiceProviderContactSerializer.__doc__,
)
class ServiceProviderContactViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List service provider contacts.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.ServiceProviderContact.objects.all()
    serializer_class = serializers.ServiceProviderContactSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.ServiceProviderContactFilter
    permission_classes = (AllowAny,)
    permit_list_expands = ("serviceprovider", "campusonline")


@docstring_format(
    model=models.ProjectMentorContribution.__doc__,
    filter=filters.ProjectMentorContributionFilter.__doc__,
    serializer=serializers.ProjectMentorContributionSerializer.__doc__,
)
class ProjectMentorContributionViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List project mentor contributions.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.ProjectMentorContribution.objects.all()
    serializer_class = serializers.ProjectMentorContributionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.ProjectMentorContributionFilter
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.Sponsorship.__doc__,
    filter=filters.SponsorshipFilter.__doc__,
    serializer=serializers.SponsorshipSerializer.__doc__,
)
class SponsorshipViewSet(FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List sponsorships.

    {model}
    {filter}
    {serializer}
    """

    queryset = models.Sponsorship.objects.all()
    serializer_class = serializers.SponsorshipSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.SponsorshipFilter
    permission_classes = (AllowAny,)
