from appconf import AppConf
from django.conf import settings


class ResearchAppConf(AppConf):
    DB_MAP = {
        "FODOK12": ("RIO", "RIOTEST", "BERUFUNG", "FIS", "MUG_DEV_BS"),
        "FODOKG": ("RIO", "RIOTEST", "BERUFUNG", "MUG_DEV_BS"),
        "FODOKSP": ("FIS", "FIS_TEST", "FIS_DEV"),
    }
    PUBMED_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    PUBMED_TIMEOUT = 5
    PUBMED_CHUNK_SIZE = 20
    PUBMED_AUTHOR_TOKEN = "[Author]"
    PUBMED_PDAT_TOKEN = "[PDAT]"
    PUBMED_XPATH_PUBMEDARTICLE_MEDLINECITATION = "PubmedArticle/MedlineCitation/"

    class Meta:
        prefix = "research"
