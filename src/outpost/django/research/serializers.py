import logging

from drf_haystack.serializers import HaystackSerializer
from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework.serializers import (
    CharField,
    PrimaryKeyRelatedField,
)

from . import (
    models,
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


class CountryGroupSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.CountryGroup
        fields = "__all__"


class CountrySerializer(FlexFieldsModelSerializer):
    """
    ## Expansions

    To activate relation expansion add the desired fields as a comma separated
    list to the `expand` query parameter like this:

        ?expand=<field>,<field>,<field>,...

    The following relational fields can be expanded:

     * `group`

    """

    class Meta:
        model = models.Country
        fields = "__all__"

    @property
    def expandable_fields(self):
        return {
            "group": (f"{self.__class__.__module__}.CountryGroupSerializer",),
        }


class LanguageSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Language
        fields = "__all__"


class ClassificationSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Classification
        fields = ("classification_id", "name", "level", "parent")


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
