import logging

from drf_haystack.serializers import HaystackSerializer
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import (
    CharField,
    PrimaryKeyRelatedField,
)

from . import (
    models,
    search_indexes,
)

logger = logging.getLogger(__name__)


class PredominantFunderSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.PredominantFunder
        fields = "__all__"


class LegalBasisSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.LegalBasis
        fields = "__all__"


class FieldSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Field
        fields = "__all__"


class CountrySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Country
        fields = "__all__"


class LanguageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Language
        fields = "__all__"


class ClassificationSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `persons`

    """

    class Meta:
        model = models.Classification
        fields = "__all__"

    @property
    def expandable_fields(self):
        person = "PersonSerializer"
        request = self.context.get("request", None)
        if request:
            if request.user:
                if request.user.is_authenticated:
                    person = "AuthenticatedPersonSerializer"
        return {
            "persons": (
                f"outpost.django.campusonline.serializers.{person}",
                {"many": True},
            )
        }


class FunderTypeIntellectualCapitalAccountingSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.FunderTypeIntellectualCapitalAccounting
        fields = "__all__"


class FunderTypeStatisticsAustriaSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.FunderTypeStatisticsAustria
        fields = "__all__"


class FunderSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `category`
     * `country`
     * `typeintellectualcapitalaccounting`
     * `typestatisticsaustria`

    """

    class Meta:
        model = models.Funder
        fields = "__all__"

    @property
    def expandable_fields(self):
        return {
            "country": (f"{self.__class__.__module__}.CountrySerializer",),
            "typeintellectualcapitalaccounting": (
                f"{self.__class__.__module__}.FunderTypeIntellectualCapitalAccountingSerializer",
            ),
            "typestatisticsaustria": (
                f"{self.__class__.__module__}.FunderTypeStatisticsAustriaSerializer",
            ),
        }


class ProgramSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `funder`

    """

    class Meta:
        model = models.Program
        fields = "__all__"

    @property
    def expandable_fields(self):
        return {
            "funder": (f"{self.__class__.__module__}.FunderSerializer",),
        }


class ProjectCategorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectCategory
        fields = "__all__"


class ProjectTypeSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectType
        exclude = ("public",)


class ProjectResearchSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectResearch
        fields = "__all__"


class ProjectFunctionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectFunction
        fields = "__all__"


class ProjectPersonSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `project`
     * `person`
     * `function`

    """

    @property
    def expandable_fields(self):
        person = "PersonSerializer"
        request = self.context.get("request", None)
        if request:
            if request.user:
                if request.user.is_authenticated:
                    person = "AuthenticatedPersonSerializer"
        return {
            "project": (f"{self.__class__.__module__}.ProjectSerializer",),
            "person": (f"outpost.django.campusonline.serializers.{person}",),
            "function": (f"{self.__class__.__module__}.ProjectFunctionSerializer",),
        }

    class Meta:
        model = models.ProjectPerson
        fields = "__all__"


class ProjectPartnerFunctionSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectPartnerFunction
        fields = "__all__"


class ProjectStudySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectStudy
        fields = "__all__"


class ProjectEventSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectEvent
        fields = "__all__"


class ProjectGrantSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectGrant
        fields = "__all__"


class ProjectStatusSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.ProjectStatus
        exclude = ("public",)


class ProjectSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `organization`
     * `category`
     * `type`
     * `partner_function`
     * `manager`
     * `contact`
     * `status`
     * `grant`
     * `research`
     * `event`
     * `study`
     * `language`
     * `program`
     * `funders`

    """

    @property
    def expandable_fields(self):
        person = "PersonSerializer"
        request = self.context.get("request", None)
        if request:
            if request.user:
                if request.user.is_authenticated:
                    person = "AuthenticatedPersonSerializer"
        return {
            "organization": (
                "outpost.django.campusonline.serializers.OrganizationSerializer",
            ),
            "category": (ProjectCategorySerializer,),
            "type": (ProjectTypeSerializer,),
            "partner_function": (ProjectPartnerFunctionSerializer,),
            "manager": (f"outpost.django.campusonline.serializers.{person}",),
            "contact": (f"outpost.django.campusonline.serializers.{person}",),
            "status": (ProjectStatusSerializer,),
            "grant": (ProjectGrantSerializer,),
            "research": (ProjectResearchSerializer,),
            "event": (ProjectEventSerializer,),
            "study": (ProjectStudySerializer,),
            "language": (LanguageSerializer,),
            "program": (ProgramSerializer,),
            "funders": (FunderSerializer, {"many": True}),
            "parent": (ProjectSerializer,),
        }

    class Meta:
        model = models.Project
        fields = (
            "id",
            "title",
            "short",
            "url",
            "abstract",
            "begin_planned",
            "begin_effective",
            "end_planned",
            "end_effective",
            "assignment",
            "program",
            "subprogram",
            "organization",
            "category",
            "type",
            "partner_function",
            "manager",
            "contact",
            "status",
            "research",
            "grant",
            "event",
            "study",
            "language",
            "funders",
            "funder_projectcode",
            "ethics_committee",
            "edudract_number",
        )


class AuthenticatedProjectSerializer(ProjectSerializer):
    @property
    def expandable_fields(self):
        return {
            **super().expandable_fields,
            **{
                "persons": (f"{self.__class__.__module__}.ProjectPersonSerializer",),
            },
        }

    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ("persons",)


class UnrestrictedProjectSerializer(AuthenticatedProjectSerializer):
    @property
    def expandable_fields(self):
        base = "outpost.django.campusonline.serializers"
        return {
            **super().expandable_fields,
            **{
                "parent": (f"{self.__class__.__module__}.{self.__class__.__name__}",),
                "legalbasis": (f"{self.__class__.__module__}.LegalBasisSerializer",),
                "predominant_funder": (
                    f"{self.__class__.__module__}.PredominantFunderSerializer",
                ),
                "project_management_accountable": (
                    f"{base}.AuthenticatedPersonSerializer",
                ),
                "co_accountable": (f"{base}.AuthenticatedPersonSerializer",),
            },
        }

    class Meta(AuthenticatedProjectSerializer.Meta):
        fields = AuthenticatedProjectSerializer.Meta.fields + (
            "gender_studies",
            "clinical_trial",
            "invesitgator_init",
            "legalbasis",
            "project_total_requested",
            "project_total_approved",
            "predominant_funder",
            "project_management_accountable",
            "internal_order",
            "parent",
            "co_accountable",
            "zmf_usage",
            "biobank_usage",
            "biomed_research",
            "commercial",
        )


class ProjectSearchSerializer(HaystackSerializer):
    class Meta:
        index_classes = [search_indexes.ProjectIndex]
        fields = ("text",)


class BiddingSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `funders`
     * `deadlines`
     * `endowments`

    """

    @property
    def expandable_fields(self):
        return {
            "funders": (
                f"{self.__class__.__module__}.FunderSerializer",
                {"many": True},
            ),
            "deadlines": (
                f"{self.__class__.__module__}.BiddingDeadlineSerializer",
                {"many": True},
            ),
            "endowments": (
                f"{self.__class__.__module__}.BiddingEndowmentSerializer",
                {"many": True},
            ),
        }

    class Meta:
        model = models.Bidding
        fields = (
            "id",
            "title",
            "short",
            "description",
            "mode",
            "url",
            "running",
            "start",
            "funders",
            "deadlines",
            "endowments",
        )


class BiddingDeadlineSerializer(FlexFieldsModelSerializer):
    """"""

    @property
    def expandable_fields(self):
        return {"bidding": (f"{self.__class__.__module__}.BiddingSerializer",)}

    class Meta:
        model = models.BiddingDeadline
        fields = ("id", "bidding", "deadline", "time", "comment")


class BiddingEndowmentSerializer(FlexFieldsModelSerializer):
    """"""

    @property
    def expandable_fields(self):
        return {"bidding": (f"{self.__class__.__module__}.BiddingSerializer",)}

    class Meta:
        model = models.BiddingEndowment
        fields = ("id", "bidding", "information", "amount", "currency")


class ServiceProviderSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `contacts`
     * `campusonline`

    """

    @property
    def expandable_fields(self):
        return {
            "campusonline": (
                "outpost.django.campusonline.serializers.OrganizationSerializer",
                {"many": False},
            ),
            "contacts": (
                f"{self.__class__.__module__}.ServiceProviderContactSerializer",
                {"many": True},
            ),
        }

    class Meta:
        model = models.ServiceProvider
        fields = (
            "id",
            "campusonline",
            "name",
            "notes",
            "active",
            "contacts",
        )


class ServiceProviderContactSerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `serviceprovider`

    """

    @property
    def expandable_fields(self):
        # import pudb; pu.db
        person = "PersonSerializer"
        if request := self.context.get("request"):
            if request.user.is_authenticated:
                person = "AuthenticatedPersonSerializer"

        return {
            "campusonline": (
                f"outpost.django.campusonline.serializers.{person}",
                {"many": False},
            ),
            "serviceprovider": (
                f"{self.__class__.__module__}.ServiceProviderSerializer",
                {"many": False},
            ),
        }

    class Meta:
        model = models.ServiceProviderContact
        fields = (
            "id",
            "serviceprovider",
            "campusonline",
            "name",
            "email",
        )


class ProjectMentorContributionSerializer(FlexFieldsModelSerializer):
    """"""

    class Meta:
        model = models.ProjectMentorContribution
        fields = (
            "id",
            "name",
        )


class SponsorshipSerializer(FlexFieldsModelSerializer):
    """"""

    class Meta:
        model = models.Sponsorship
        fields = (
            "id",
            "name",
        )
