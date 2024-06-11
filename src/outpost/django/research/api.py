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
    filter_class = filters.LegalBasisFilter


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
    filter_class = filters.FieldFilter


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
    filter_class = filters.ClassificationFilter


@docstring_format(
    model=models.Expertise.__doc__, serializer=serializers.ExpertiseSerializer.__doc__
)
class ExpertiseViewSet(CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List expertise.

    {model}
    {serializer}
    """

    queryset = models.Expertise.objects.all()
    serializer_class = serializers.ExpertiseSerializer
    permission_classes = (AllowAny,)
    permit_list_expands = ("person",)


@docstring_format(
    model=models.Knowledge.__doc__, serializer=serializers.KnowledgeSerializer.__doc__
)
class KnowledgeViewSet(CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List knowledge.

    {model}
    {serializer}
    """

    queryset = models.Knowledge.objects.all()
    serializer_class = serializers.KnowledgeSerializer
    permission_classes = (AllowAny,)
    permit_list_expands = ("person",)


@docstring_format(
    model=models.Education.__doc__, serializer=serializers.EducationSerializer.__doc__
)
class EducationViewSet(CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List educations.

    {model}
    {serializer}
    """

    queryset = models.Education.objects.all()
    serializer_class = serializers.EducationSerializer
    permission_classes = (AllowAny,)
    permit_list_expands = ("person",)


@docstring_format(
    model=models.FunderCategory.__doc__,
    serializer=serializers.FunderCategorySerializer.__doc__,
)
class FunderCategoryViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List funder categories.

    {model}
    {serializer}
    """

    queryset = models.FunderCategory.objects.all()
    serializer_class = serializers.FunderCategorySerializer
    permission_classes = (AllowAny,)


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
        "category",
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
    filter_class = filters.ProjectResearchFilter


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
    filter_class = filters.ProjectFunctionFilter


@docstring_format(
    model=models.ProjectPerson.__doc__,
    serializer=serializers.ProjectPersonSerializer.__doc__,
    filter=filters.ProjectPersonFilter.__doc__,
)
class ProjectPersonViewSet(CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List project persons with assinged functions.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.ProjectPerson.objects.all()
    serializer_class = serializers.ProjectPersonSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = filters.ProjectPersonFilter
    permission_classes = (IsAuthenticated,)
    permit_list_expands = (
        "project",
        "person",
        "function",
    )
    object_cache_key_func = key_constructors.PermissionDetailKeyConstructor(
        params={"permission": settings.RESEARCH_PROJECT_UNRESTRICTED_PERMS}
    )
    list_cache_key_func = key_constructors.PermissionListKeyConstructor(
        params={"permission": settings.RESEARCH_PROJECT_UNRESTRICTED_PERMS}
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user:
            if self.request.user.has_perms(
                settings.RESEARCH_PROJECT_UNRESTRICTED_PERMS
            ):
                return queryset
        return queryset.filter(
            project__status__public=True,
            project__type__public=True,
            project__publish=True,
            project__visible=True,
        )


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
    filter_class = filters.ProjectStudyFilter


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
    model=models.ProjectStatus.__doc__,
    serializer=serializers.ProjectStatusSerializer.__doc__,
)
class ProjectStatusViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List project status.

    {model}
    {serializer}
    """

    queryset = models.ProjectStatus.objects.all()
    serializer_class = serializers.ProjectStatusSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.Project.__doc__,
    serializer=serializers.ProjectSerializer.__doc__,
    filter=filters.ProjectFilter.__doc__,
)
class ProjectViewSet(CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List projects.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = filters.ProjectFilter
    ordering_fields = (
        "begin_planned",
        "begin_effective",
        "end_planned",
        "end_effective",
    )
    permission_classes = (AllowAny,)
    permit_list_expands = (
        "organization",
        "category",
        "type",
        "partner_function",
        "manager",
        "contact",
        "status",
        "grant",
        "research",
        "event",
        "study",
        "language",
        "funders",
        "program",
        "persons",
    )
    object_cache_key_func = key_constructors.PermissionDetailKeyConstructor(
        params={"permission": settings.RESEARCH_PROJECT_UNRESTRICTED_PERMS}
    )
    list_cache_key_func = key_constructors.PermissionListKeyConstructor(
        params={"permission": settings.RESEARCH_PROJECT_UNRESTRICTED_PERMS}
    )

    def get_serializer_class(self):
        if self.request.user:
            if self.request.user.has_perms(
                settings.RESEARCH_PROJECT_UNRESTRICTED_PERMS
            ):
                return serializers.UnrestrictedProjectSerializer
            return serializers.AuthenticatedProjectSerializer
        return self.serializer_class

    def get_serializer_context(self):
        return {"request": self.request}

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user:
            if self.request.user.has_perms(
                settings.RESEARCH_PROJECT_UNRESTRICTED_PERMS
            ):
                return queryset
        return queryset.filter(
            status__public=True, type__public=True, publish=True, visible=True
        )


class ProjectSearchViewSet(HaystackViewSet):
    index_models = [models.Project]
    serializer_class = serializers.ProjectSearchSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.PublicationAuthorship.__doc__,
    serializer=serializers.PublicationAuthorshipSerializer.__doc__,
)
class PublicationAuthorshipViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List publication authorships.

    {model}
    {serializer}
    """

    queryset = models.PublicationAuthorship.objects.all()
    serializer_class = serializers.PublicationAuthorshipSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.PublicationCategory.__doc__,
    serializer=serializers.PublicationCategorySerializer.__doc__,
)
class PublicationCategoryViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List publication categories.

    {model}
    {serializer}
    """

    queryset = models.PublicationCategory.objects.all()
    serializer_class = serializers.PublicationCategorySerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.PublicationDocument.__doc__,
    serializer=serializers.PublicationDocumentSerializer.__doc__,
)
class PublicationDocumentViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List publication documents.

    {model}
    {serializer}
    """

    queryset = models.PublicationDocument.objects.all()
    serializer_class = serializers.PublicationDocumentSerializer
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.PublicationPerson.__doc__,
    serializer=serializers.PublicationPersonSerializer.__doc__,
    filter=filters.PublicationPersonFilter.__doc__,
)
class PublicationPersonViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    """
    List persons and their authorship type for publications.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.PublicationPerson.objects.all()
    serializer_class = serializers.PublicationPersonSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = filters.PublicationPersonFilter


@docstring_format(
    model=models.Publication.__doc__,
    serializer=serializers.PublicationSerializer.__doc__,
    filter=filters.PublicationFilter.__doc__,
)
class PublicationViewSet(CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List publications.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.Publication.objects.all()
    serializer_class = serializers.PublicationSerializer
    filter_backends = (SimpleDjangoFilterBackend, OrderingFilter)
    filter_class = filters.PublicationFilter
    ordering_fields = (
        "year",
        "impactfactor",
        "impactfactor_norm",
        "impactfactor_nrm_super",
        "imported",
    )
    permission_classes = (AllowAny,)
    permit_list_expands = (
        "persons",
        "category",
        "document_type",
        "status",
        "program",
        "organizations",
    )

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("category", "document_type")
        queryset = queryset.prefetch_related(
            "persons",
            "persons__person__room",
            "persons__person__room__building",
            "persons__person__room__floor",
            "persons__person__room__geo",
            "persons__person__room__category",
            "persons__person__classifications",
            "persons__person__expertise",
            "persons__person__knowledge",
            "persons__person__education",
            "organizations",
        )
        return queryset


class PublicationSearchViewSet(HaystackViewSet):
    index_models = [models.Publication]
    serializer_class = serializers.PublicationSearchSerializer
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
    filter_class = filters.BiddingDeadlineFilter
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
    filter_class = filters.BiddingEndowmentFilter
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
    filter_class = filters.BiddingFilter
    ordering_fields = ("start",)
    permission_classes = (AllowAny,)
    permit_list_expands = ("funders", "deadlines", "endowments")

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("funders", "deadlines", "endowments")
        return queryset


@docstring_format(
    model=models.PartnerTypeIntellectualCapitalAccounting.__doc__,
    serializer=serializers.PartnerTypeIntellectualCapitalAccountingSerializer.__doc__,
)
class PartnerTypeIntellectualCapitalAccountingViewSet(
    CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet
):
    """
    List partner types according to intellectual capital accounting.

    {model}
    {serializer}
    """

    queryset = models.PartnerTypeIntellectualCapitalAccounting.objects.all()
    serializer_class = serializers.PartnerTypeIntellectualCapitalAccountingSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    permission_classes = (AllowAny,)


@docstring_format(
    model=models.Partner.__doc__,
    serializer=serializers.PartnerSerializer.__doc__,
    filter=filters.PartnerFilter.__doc__,
)
class PartnerViewSet(CacheResponseMixin, FlexFieldsMixin, ReadOnlyModelViewSet):
    """
    List partners.

    {model}
    {serializer}
    {filter}
    """

    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnerSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = filters.PartnerFilter
    ordering_fields = ("start",)
    permission_classes = (AllowAny,)
    permit_list_expands = ("typeintellectualcapitalaccounting",)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related("typeintellectualcapitalaccounting")
        return queryset
