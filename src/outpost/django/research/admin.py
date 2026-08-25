from types import MethodType

from django.contrib import admin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView

from . import models


class ResearchAutocompleteJsonView(AutocompleteJsonView):
    def serialize_result(self, obj, to_field_name):
        result = super().serialize_result(obj, to_field_name)

        if isinstance(obj, models.Funder) and self.source_field.name == "parent":
            details = []

            if obj.street:
                details.append(obj.street)
            if obj.city:
                details.append(obj.city)
            if obj.country:
                details.append(str(obj.country))

            result["text"] = obj.name

            if details:
                result["text"] += f" - {' | '.join(details)}"

        return result


def custom_autocomplete_view(self, request):
    return ResearchAutocompleteJsonView.as_view(admin_site=self)(request)


admin.site.autocomplete_view = MethodType(
    custom_autocomplete_view,
    admin.site,
)


@admin.register(models.PredominantFunder)
class PredominantFunderAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.LegalBasis)
class LegalBasisAdmin(admin.ModelAdmin):
    list_filter = ("active",)
    search_fields = ("name",)


@admin.register(models.Field)
class FieldAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.ResearchType)
class ResearchTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Classification)
class ClassificationAdmin(admin.ModelAdmin):
    autocomplete_fields = ("parent",)
    search_fields = ("name",)


@admin.register(models.Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    autocomplete_fields = ("person",)
    list_display = ("__str__", "person")
    search_fields = ("name", "person__first_name", "person__last_name")


@admin.register(models.Knowledge)
class KnowledgeAdmin(admin.ModelAdmin):
    autocomplete_fields = ("person",)
    list_display = ("__str__", "person")
    search_fields = ("name", "person__first_name", "person__last_name")


@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    autocomplete_fields = ("person",)
    list_display = ("__str__", "person")
    search_fields = ("name", "person__first_name", "person__last_name")


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ("name", "iso")


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "iso")
    search_fields = ("name", "iso")


@admin.register(models.FunderCategory)
class FunderCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name", "short")


@admin.register(models.Funder)
class FunderAdmin(admin.ModelAdmin):
    autocomplete_fields = (
        "country",
        "typeintellectualcapitalaccounting",
        "typestatisticsaustria",
        "parent",
    )
    list_display = (
        "__str__",
        "abbreviation",
        "street",
        "zipcode",
        "city",
        "country",
        "url",
        "active",
    )
    list_filter = (
        "active",
        "patron",
        "patron_peer_review",
        "typeintellectualcapitalaccounting",
        "typestatisticsaustria",
    )
    readonly_fields = ("id",)
    search_fields = ("name", "abbreviation")

    def get_fields(self, request, obj=None):
        fields = list(super().get_fields(request, obj))
        return ["id", *[field for field in fields if field != "id"]]


@admin.register(models.ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_filter = ("third_party_funding_policy",)
    search_fields = ("name",)


@admin.register(models.ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    list_filter = ("public",)
    search_fields = ("name",)


@admin.register(models.ProjectResearch)
class ProjectResearchAdmin(admin.ModelAdmin):
    list_filter = ("active",)
    search_fields = ("name",)


@admin.register(models.ProjectFunction)
class ProjectFunctionAdmin(admin.ModelAdmin):
    list_filter = ("active",)
    search_fields = ("name",)


@admin.register(models.ProjectPerson)
class ProjectPersonAdmin(admin.ModelAdmin):
    autocomplete_fields = ("project", "person", "function")
    list_display = ("project", "person", "function")
    list_filter = ("function",)
    search_fields = ("project__name", "person__last_name", "person__first_name")


@admin.register(models.ProjectPartnerFunction)
class ProjectPartnerFunctionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.ProjectStudy)
class ProjectStudyAdmin(admin.ModelAdmin):
    list_filter = ("active",)
    search_fields = ("name",)


@admin.register(models.ProjectEvent)
class ProjectEventAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.ProjectGrant)
class ProjectGrantAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_filter = ("public",)
    search_fields = ("name",)


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
    autocomplete_fields = ("funder",)
    list_display = ("name", "funder")
    list_filter = ("active",)
    search_fields = ("name", "funder__name")


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    autocomplete_fields = (
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
        "program",
        "legalbasis",
        "predominant_funder",
        "project_management_accountable",
        "parent",
        "co_accountable",
    )
    list_display = ("__str__", "short", "organization")
    list_filter = (
        "category",
        "type",
        "status",
        "grant",
        "research",
        "event",
        "language",
        "publish",
        "visible",
    )
    search_fields = ("title", "short")
    date_hierarchy = "assignment"


@admin.register(models.PublicationCategory)
class PublicationCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.PublicationDocument)
class PublicationDocumentAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.PublicationAuthorship)
class PublicationAuthorshipAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.PublicationOrganization)
class PublicationOrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PublicationPerson)
class PublicationPersonAdmin(admin.ModelAdmin):
    autocomplete_fields = ("publication", "person", "authorship")
    list_display = ("person", "publication", "authorship")
    list_display_links = ("person", "publication")
    list_filter = ("authorship", "last_author")
    search_fields = ("person__first_name", "person__last_name", "publication__title")


@admin.register(models.Publication)
class PublicationAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "title",
        "authors",
        "source",
        "sci",
        "pubmed",
        "doi",
        "pmc",
        "issn",
    )
    autocomplete_fields = ("category", "document_type")


@admin.register(models.Bidding)
class BiddingAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "start")
    list_display_links = ("title",)
    list_filter = ("running",)
    search_fields = ("title",)
    date_hierarchy = "start"


@admin.register(models.BiddingDeadline)
class BiddingDeadlineAdmin(admin.ModelAdmin):
    autocomplete_fields = ("bidding",)
    list_display = ("bidding", "deadline")
    list_display_links = ("bidding",)
    search_fields = ("bidding__title", "comment")


@admin.register(models.BiddingEndowment)
class BiddingEndowmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ("bidding",)
    list_display = ("bidding", "amount", "currency")
    list_display_links = ("bidding",)
    search_fields = ("bidding__title", "information")


@admin.register(models.Partner)
class PartnerAdmin(admin.ModelAdmin):
    autocomplete_fields = ("typeintellectualcapitalaccounting",)
    list_display = ("name", "url")
    list_filter = ("typeintellectualcapitalaccounting",)
    search_fields = ("name", "short", "street", "city", "email", "information")


@admin.register(models.PartnerTypeIntellectualCapitalAccounting)
class PartnerTypeIntellectualCapitalAccountingAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.FunderTypeIntellectualCapitalAccounting)
class FunderTypeIntellectualCapitalAccountingAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.FunderTypeStatisticsAustria)
class FunderTypeStatisticsAustriaAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(models.ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active")


@admin.register(models.ServiceProviderContact)
class ServiceProviderContactAdmin(admin.ModelAdmin):
    list_display = ("id", "serviceprovider", "name", "email")


@admin.register(models.ProjectMentorContribution)
class ProjectMentorContributionAdmin(admin.ModelAdmin):
    list_filter = ("active",)
    search_fields = ("name",)


@admin.register(models.Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "active")
