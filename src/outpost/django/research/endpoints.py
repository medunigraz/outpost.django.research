from . import api

v1 = [
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
    (r"research/funder", api.FunderViewSet, "research-funder"),
    (
        r"research/project:category",
        api.ProjectCategoryViewSet,
        "research-project-category",
    ),
    (
        r"research/project:research",
        api.ProjectResearchViewSet,
        "research-project-research",
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
    (r"research/publication", api.PublicationViewSet, "research-publication"),
    (
        r"research/search/publication",
        api.PublicationSearchViewSet,
        "research-publication-search",
    ),
]
