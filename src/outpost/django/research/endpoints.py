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
    (r"research/language", api.LanguageViewSet, "research-language"),
    (r"research/program", api.ProgramViewSet, "research-program"),
    (r"research/classification", api.ClassificationViewSet, "research-classification"),
    (r"research/expertise", api.ExpertiseViewSet, "research-expertise"),
    (r"research/knowledge", api.KnowledgeViewSet, "research-knowledge"),
    (r"research/education", api.EducationViewSet, "research-education"),
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
        r"research/funder:category",
        api.FunderCategoryViewSet,
        "research-funder-category",
    ),
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
    (r"research/partner", api.PartnerViewSet, "research-partner"),
    (
        r"research/partner:type:intellectualcapitalaccounting",
        api.PartnerTypeIntellectualCapitalAccountingViewSet,
        "research-partner-type-intellectualcapitalaccounting",
    ),
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
        r"research/project:person",
        api.ProjectPersonViewSet,
        "research-project-person",
    ),
    (
        r"research/project:partnerfunction",
        api.ProjectPartnerFunctionViewSet,
        "research-project-partner-function",
    ),
    (r"research/project:study", api.ProjectStudyViewSet, "research-project-study"),
    (r"research/project:event", api.ProjectEventViewSet, "research-project-event"),
    (r"research/project:grant", api.ProjectGrantViewSet, "research-project-grant"),
    (r"research/project:status", api.ProjectStatusViewSet, "research-project-status"),
    (r"research/project", api.ProjectViewSet, "research-project"),
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
    (r"research/search/project", api.ProjectSearchViewSet, "research-project-search"),
    (
        r"research/publication:authorship",
        api.PublicationAuthorshipViewSet,
        "research-publication-authorship",
    ),
    (
        r"research/publication:category",
        api.PublicationCategoryViewSet,
        "research-publication-category",
    ),
    (
        r"research/publication:document",
        api.PublicationDocumentViewSet,
        "research-publication-document",
    ),
    (
        r"research/publication:person",
        api.PublicationPersonViewSet,
        "research-publication-person",
    ),
    (r"research/publication", api.PublicationViewSet, "research-publication"),
    (
        r"research/search/publication",
        api.PublicationSearchViewSet,
        "research-publication-search",
    ),
]
