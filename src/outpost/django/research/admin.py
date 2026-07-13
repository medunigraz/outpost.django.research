from django.contrib import admin

from . import models


@admin.register(models.PredominantFunder)
class PredominantFunderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.LegalBasis)
class LegalBasisAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Field)
class FieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ResearchType)
class ResearchTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Classification)
class ClassificationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Knowledge)
class KnowledgeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Education)
class EducationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FunderCategory)
class FunderCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Funder)
class FunderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectType)
class ProjectTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectResearch)
class ProjectResearchAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectFunction)
class ProjectFunctionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectPerson)
class ProjectPersonAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectPartnerFunction)
class ProjectPartnerFunctionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectStudy)
class ProjectStudyAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectEvent)
class ProjectEventAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectGrant)
class ProjectGrantAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


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
    search_fields = ("id", "title", "authors", "source", "sci", "pubmed", "doi", "pmc", "issn")
    autocomplete_fields = ("category", "document_type")


@admin.register(models.Bidding)
class BiddingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BiddingDeadline)
class BiddingDeadlineAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BiddingEndowment)
class BiddingEndowmentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Partner)
class PartnerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PartnerTypeIntellectualCapitalAccounting)
class PartnerTypeIntellectualCapitalAccountingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FunderTypeIntellectualCapitalAccounting)
class FunderTypeIntellectualCapitalAccountingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FunderTypeStatisticsAustria)
class FunderTypeStatisticsAustriaAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active")


@admin.register(models.ServiceProviderContact)
class ServiceProviderContactAdmin(admin.ModelAdmin):
    list_display = ("id", "serviceprovider", "name", "email")


@admin.register(models.ProjectMentorContribution)
class ProjectMentorContributionAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "active")


@admin.register(models.Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "active")
