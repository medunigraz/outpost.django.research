from types import MethodType
from django.contrib import admin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView

from . import models


class FunderAutocompleteJsonView(AutocompleteJsonView):
    def serialize_result(self, obj, to_field_name):
        result = super().serialize_result(obj, to_field_name)
        if isinstance(obj, models.Funder) and self.source_field.name == "parent":
            details = [
                v for v in (obj.street, obj.city, obj.country and str(obj.country)) if v
            ]
            result["text"] = obj.name + (f" - {' | '.join(details)}" if details else "")
        return result


def _custom_autocomplete_view(self, request):
    return FunderAutocompleteJsonView.as_view(admin_site=self)(request)


admin.site.autocomplete_view = MethodType(_custom_autocomplete_view, admin.site)


class ResearchModelAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    search_fields = ("name",)

    def _ensure_id_first(self, fields):
        fields = list(fields)
        if "id" in fields:
            fields.remove("id")
        return ["id"] + fields

    def get_readonly_fields(self, request, obj=None):
        return self._ensure_id_first(super().get_readonly_fields(request, obj))

    def get_fields(self, request, obj=None):
        return self._ensure_id_first(super().get_fields(request, obj))


@admin.register(models.Bidding)
class BiddingAdmin(ResearchModelAdmin):
    list_display = ("id", "title", "url", "start")
    list_filter = ("running",)
    search_fields = ("title",)
    date_hierarchy = "start"


@admin.register(models.BiddingDeadline)
class BiddingDeadlineAdmin(ResearchModelAdmin):
    autocomplete_fields = ("bidding",)
    list_display = ("id", "bidding", "deadline")
    search_fields = ("bidding__title", "comment")


@admin.register(models.BiddingEndowment)
class BiddingEndowmentAdmin(ResearchModelAdmin):
    autocomplete_fields = ("bidding",)
    list_display = ("id", "bidding", "amount", "currency")
    search_fields = ("bidding__title", "information")


@admin.register(models.Classification)
class ClassificationAdmin(ResearchModelAdmin):
    autocomplete_fields = ("parent",)
    list_display = ("classification_id", "__str__", "level")


@admin.register(models.Country)
class CountryAdmin(ResearchModelAdmin):
    list_display = ("id", "__str__", "group")
    list_filter = ("group",)
    search_fields = ("name", "iso")


@admin.register(models.CountryGroup)
class CountryGroupAdmin(ResearchModelAdmin):
    pass


@admin.register(models.Field)
class FieldAdmin(ResearchModelAdmin):
    list_filter = ("active",)


@admin.register(models.Funder)
class FunderAdmin(ResearchModelAdmin):
    autocomplete_fields = (
        "country",
        "typeintellectualcapitalaccounting",
        "typestatisticsaustria",
        "parent",
    )
    list_display = (
        "id",
        "name",
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
        "country",
    )
    search_fields = ("name", "abbreviation")


@admin.register(models.FunderTypeIntellectualCapitalAccounting)
class FunderTypeIntellectualCapitalAccountingAdmin(ResearchModelAdmin):
    pass


@admin.register(models.FunderTypeStatisticsAustria)
class FunderTypeStatisticsAustriaAdmin(ResearchModelAdmin):
    pass


@admin.register(models.Language)
class LanguageAdmin(ResearchModelAdmin):
    list_display = ("id", "__str__", "iso")
    search_fields = ("name", "iso")


@admin.register(models.LegalBasis)
class LegalBasisAdmin(ResearchModelAdmin):
    list_filter = ("active",)


@admin.register(models.PredominantFunder)
class PredominantFunderAdmin(ResearchModelAdmin):
    pass


@admin.register(models.Program)
class ProgramAdmin(ResearchModelAdmin):
    autocomplete_fields = ("funder",)
    list_display = ("id", "name", "funder")
    list_filter = ("active", "funder")
    search_fields = ("name", "funder__name")


@admin.register(models.ProjectCategory)
class ProjectCategoryAdmin(ResearchModelAdmin):
    list_filter = ("third_party_funding_policy",)


@admin.register(models.ProjectEvent)
class ProjectEventAdmin(ResearchModelAdmin):
    pass


@admin.register(models.ProjectFunction)
class ProjectFunctionAdmin(ResearchModelAdmin):
    list_filter = ("active",)


@admin.register(models.ProjectGrant)
class ProjectGrantAdmin(ResearchModelAdmin):
    pass


@admin.register(models.ProjectMentorContribution)
class ProjectMentorContributionAdmin(ResearchModelAdmin):
    list_filter = ("active",)


@admin.register(models.ProjectPartnerFunction)
class ProjectPartnerFunctionAdmin(ResearchModelAdmin):
    pass


@admin.register(models.ProjectResearch)
class ProjectResearchAdmin(ResearchModelAdmin):
    list_filter = ("active",)


@admin.register(models.ProjectStudy)
class ProjectStudyAdmin(ResearchModelAdmin):
    list_filter = ("active",)


@admin.register(models.ProjectType)
class ProjectTypeAdmin(ResearchModelAdmin):
    list_filter = ("public",)


@admin.register(models.ResearchType)
class ResearchTypeAdmin(ResearchModelAdmin):
    pass


@admin.register(models.ServiceProvider)
class ServiceProviderAdmin(ResearchModelAdmin):
    list_display = ("id", "__str__", "active")
    search_fields = ("campusonline",)


@admin.register(models.ServiceProviderContact)
class ServiceProviderContactAdmin(ResearchModelAdmin):
    autocomplete_fields = ("serviceprovider", "campusonline")
    list_display = ("id", "serviceprovider", "name", "email")
    list_filter = ("serviceprovider",)


@admin.register(models.Sponsorship)
class SponsorshipAdmin(ResearchModelAdmin):
    list_display = ("id", "__str__", "active")
