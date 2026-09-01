from . import api

v1 = [
    (
        r"research/predominantfunder",
        api.PredominantFunderViewSet,
        "research-predominantfunder",
    ),
    (r"research/legalbasis", api.LegalBasisViewSet, "research-legalbasis"),
    (r"research/field", api.FieldViewSet, "research-field"),
    (r"research/country", api.CountryViewSet, "research-country"),
    (r"research/country:group", api.CountryGroupViewSet, "research-country-group"),
    (r"research/language", api.LanguageViewSet, "research-language"),
    (r"research/program", api.ProgramViewSet, "research-program"),
    (r"research/classification", api.ClassificationViewSet, "research-classification"),
    (
        r"research/bidding:deadline",
        api.BiddingDeadlineViewSet,
        "research-bidding-deadline",
    ),
    (
        r"research/bidding:endowment",
        api.BiddingEndowmentViewSet,
        "research-bidding-endowment",
    ),
    (r"research/bidding", api.BiddingViewSet, "research-bidding"),
    (
        r"research/funder:type:intellectualcapitalaccounting",
        api.FunderTypeIntellectualCapitalAccountingViewSet,
        "research-funder-type-intellectualcapitalaccounting",
    ),
    (
        r"research/funder:type:statisticsaustria",
        api.FunderTypeStatisticsAustriaViewSet,
        "research-funder-type-statisticsaustria",
    ),
    (r"research/funder", api.FunderViewSet, "research-funder"),
    (
        r"research/project:category",
        api.ProjectCategoryViewSet,
        "research-project-category",
    ),
    (
        r"research/project:type",
        api.ProjectTypeViewSet,
        "research-project-type",
    ),
    (
        r"research/project:research",
        api.ProjectResearchViewSet,
        "research-project-research",
    ),
    (
        r"research/project:function",
        api.ProjectFunctionViewSet,
        "research-project-function",
    ),
    (
        r"research/project:partnerfunction",
        api.ProjectPartnerFunctionViewSet,
        "research-project-partner-function",
    ),
    (r"research/project:study", api.ProjectStudyViewSet, "research-project-study"),
    (r"research/project:event", api.ProjectEventViewSet, "research-project-event"),
    (r"research/project:grant", api.ProjectGrantViewSet, "research-project-grant"),
    (
        r"research/serviceprovider",
        api.ServiceProviderViewSet,
        "research-serviceprovider",
    ),
    (
        r"research/serviceprovider:contact",
        api.ServiceProviderContactViewSet,
        "research-serviceprovider-contact",
    ),
    (
        r"research/projectmentorcontribution",
        api.ProjectMentorContributionViewSet,
        "research-projectmentorcontribution",
    ),
    (r"research/sponsorship", api.SponsorshipViewSet, "research-sponsorship"),
]
