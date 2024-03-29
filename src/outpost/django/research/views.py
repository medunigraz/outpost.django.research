import logging
from datetime import datetime
from xml.etree import ElementTree

import pyodbc
import requests
from braces.views import CsrfExemptMixin
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from more_itertools import chunked
from purl import URL

from .conf import settings

# TODO: Find a way to fix https://github.com/mkleehammer/pyodbc/issues/489
#       This makes Oracle SQL error messages useless.

logger = logging.getLogger(__name__)


class DatabaseException(Exception):
    pass


class DatabaseMixin(object):
    def connection(self, database, schema):
        schemas = settings.RESEARCH_DB_MAP.get(database)

        if not schemas:
            raise DatabaseException(_("Unknown database requested"))

        if schema not in schemas:
            raise DatabaseException(_("Schema not allowed"))

        try:
            return pyodbc.connect("DSN={}".format(database), autocommit=False)
        except pyodbc.InterfaceError as e:
            logger.error(f"Unable to connect to database: {e}")
            raise DatabaseException(_("Unable to connect to database"))


class SearchView(CsrfExemptMixin, DatabaseMixin, View):
    url = (
        URL(settings.RESEARCH_PUBMED_URL)
        .add_path_segment("esearch.fcgi")
        .query_param("db", "pubmed")
    )

    def post(self, request, database, schema):
        try:
            con = self.connection(database, schema)
        except DatabaseException as e:
            return HttpResponseBadRequest(e)

        term = []

        author1 = request.POST.get("autor1_in")
        if author1:
            term.append(f'"{author1}"{settings.RESEARCH_PUBMED_AUTHOR_TOKEN}')

        author2 = request.POST.get("autor2_in")
        if author2:
            term.append(f'"{author2}"{settings.RESEARCH_PUBMED_AUTHOR_TOKEN}')

        year = request.POST.get("jahr_in")
        if year:
            try:
                year = int(year)
                term.append(f'"{year}"{settings.RESEARCH_PUBMED_PDAT_TOKEN}')
            except ValueError:
                return HttpResponse(_("Invalid Year specified"), status=400)

        combination = request.POST.get("kombination_in")
        if combination:
            term.append(combination)

        if (len(term)) == 0:
            logger.warn("No search parameters specified")
            return HttpResponse(_("No search parameters specified"), status=400)

        url = self.url.query_param("term", " ".join(term))

        # 2020-04-22: Nach Absprache mit Hrn. Schaffer wird in die Tabelle PUBMED_SUCHE_IDS
        # nur geschrieben, wenn der POST Parameter retmax_in mitübergeben wird. Es werden dann
        # alle PubMed Ids, die anhand der Suche gefunden werden können, gespeichert
        if request.POST.get("retmax_in"):
            try:
                logger.debug("PubMed IDs paketieren")
                url = url.query_param("RetMax", int(request.POST.get("retmax_in")))
            except ValueError:
                logger.warn("Invalid RetMax specified")
                return HttpResponse(_("Invalid RetMax specified"), status=400)

        logger.debug(f"Constructed search URL: {url.as_string()}")

        if not request.POST.get("suche_id_in"):
            logger.warn("No search ID specified")
            return HttpResponse(_("No search ID specified"), status=400)

        try:
            search = int(request.POST.get("suche_id_in"))
        except ValueError:
            logger.warn("Invalid search ID specified")
            return HttpResponse(_("Invalid search ID specified"), status=400)

        person_id = request.POST.get("person_id_in")
        if person_id:
            try:
                person_id = int(person_id)
            except ValueError:
                logger.warn("Invalid person ID specified")
                return HttpResponse(_("Invalid person ID specified"), status=400)

        try:
            with requests.get(
                url.as_string(), timeout=settings.RESEARCH_PUBMED_TIMEOUT
            ) as response:
                xml = ElementTree.fromstring(response.content)
        except requests.exceptions.RequestException:
            return HttpResponse(_("Remote service not available"), status=503)

        length = int(xml.find("Count").text)
        ids = (int(item.text) for item in xml.findall("IdList/Id"))

        try:
            with con.cursor() as cursor:
                if not request.POST.get("retmax_in"):
                    cursor.execute(
                        f"""
                        INSERT INTO
                            {schema}.pubmed_suche_treffer
                        (
                            suche_id,
                            suchbegriff1,
                            suchbegriff2,
                            suchbegriff3,
                            suchfeld_jahr,
                            person_id,
                            suchdatum,
                            anzahl_treffer
                        )
                        VALUES
                        (
                            ?, ?, ?, ?, ?, ?, SYSDATE, ?
                        )
                        """,
                        search,
                        author1,
                        author2,
                        combination,
                        year,
                        person_id,
                        length,
                    )
                else:
                    for cid, chunk in enumerate(
                        chunked(ids, settings.RESEARCH_PUBMED_CHUNK_SIZE)
                    ):
                        for i in chunk:
                            with con.cursor() as cursor:
                                cursor.execute(
                                    f"""
                                    INSERT INTO
                                        {schema}.pubmed_suche_ids
                                    (
                                        suche_id,
                                        pubmed_id,
                                        datenpaket_nr
                                    )
                                    VALUES
                                    (?, ?, ?)
                                    """,
                                    search,
                                    i,
                                    cid + 1,
                                )
        except pyodbc.Error as e:
            con.rollback()
            logger.error(f"Failed to write to {database}/{schema}: {e}")
            return HttpResponse(_("ODBC connection failed"), status=503)
        else:
            con.commit()

        return HttpResponse(response, content_type="text/xml; charset=utf-8")


class DetailView(CsrfExemptMixin, DatabaseMixin, View):
    url = (
        URL(settings.RESEARCH_PUBMED_URL)
        .add_path_segment("efetch.fcgi")
        .query_params({"db": "pubmed", "rettype": "medline", "retmode": "xml"})
    )
    base = settings.RESEARCH_PUBMED_XPATH_PUBMEDARTICLE_MEDLINECITATION

    # Seperatoren für die Umwandlung von Array auf String
    seperatorColon = " : "
    seperatorSemicolon = "; "
    seperatorBlank = " "
    seperatorComma = ", "

    def post(self, request, database, schema):

        try:
            con = self.connection(database, schema)
        except DatabaseException as e:
            return HttpResponseBadRequest(e)

        logger.debug(f"Start detail")
        search = request.POST.get("suche_id_in")
        if not search:
            logger.warn("No search ID specified")
            return HttpResponse(_("No search ID specified"), status=400)

        try:
            search = int(search)
        except ValueError:
            logger.warn("Invalid search ID specified")
            return HttpResponse(_("Invalid search ID specified"), status=400)

        if not request.POST.get("ids_in"):
            logger.warn("No PubMed IDs specified")
            return HttpResponse(_("No PubMed IDs specified"), status=400)

        ids = map(
            lambda i: int(i.strip()),
            request.POST.get("ids_in", "").strip("[]").split(","),
        )

        # print(pubmedIDS)
        for pubmed in ids:
            url = self.url.query_param("id", pubmed)
            logger.debug(f"Constructed search URL: {url.as_string()}")

            try:
                with requests.get(
                    url.as_string(), timeout=settings.RESEARCH_PUBMED_TIMEOUT
                ) as resp:
                    xml = ElementTree.fromstring(resp.content)
            except requests.exceptions.RequestException:
                return HttpResponse(_("Remote service not available"), status=503)

            try:
                self.save_detail(search, pubmed, xml, con, schema)
                self.save_authors(search, pubmed, xml, con, schema)
                self.save_sponsorships(search, pubmed, xml, con, schema)
                self.save_mesh(search, pubmed, xml, con, schema)
            except pyodbc.Error as e:
                con.rollback()
                logger.error(f"Failed to write to {database}/{schema}: {e}")
                return HttpResponse(_("ODBC connection failed"), status=503)
            else:
                con.commit()
        return HttpResponse("true")

    @staticmethod
    def find(node, default, *paths):
        try:
            node = next(
                filter(lambda n: n is not None, map(lambda p: node.find(p), paths))
            )
            return (node.text or "") + "".join(
                ElementTree.tostring(e, "unicode") for e in node
            )
        except StopIteration:
            return default

    def save_detail(self, search, pubmed, xml, con, schema):
        intPubDate = self.find(
            xml, 0, f"{self.base}Article/Journal/JournalIssue/PubDate/Year"
        )
        intPubDateAlternative = self.find(
            xml,
            0,
            "PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus='pubmed']/Year",
        )
        strArticleTitle = self.find(xml, "", f"{self.base}Article/ArticleTitle")

        strDoi = self.find(
            xml,
            "",
            "PubmedArticle/PubmedData/ArticleIdList/ArticleId[@IdType='doi']",
            f"{self.base}Article/ELocationID[@EIdType='doi']",
        )

        strLanguage = self.find(xml, "", f"{self.base}Article/Language")

        strAbstractText = ""
        aAbstract = []
        for item in xml.findall(f"{self.base}Article/Abstract/AbstractText"):
            text = (item.text or "") + "".join(
                ElementTree.tostring(e, "unicode") for e in item
            )
            label = item.get("Label")
            if label is not None:
                aAbstract.append(f"{label}: {text}")
            else:
                aAbstract.append(text)
        strAbstractText = self.seperatorBlank.join(aAbstract)

        strVolume = self.find(
            xml, "", f"{self.base}Article/Journal/JournalIssue/Volume"
        )

        strIssue = self.find(xml, "", f"{self.base}Article/Journal/JournalIssue/Issue")

        strPagination = self.find(xml, "", f"{self.base}Article/Pagination/MedlinePgn")

        strISSNPrint = self.find(
            xml, "", f"{self.base}Article/Journal/ISSN[@IssnType='Print']"
        )

        strISSNElectronic = self.find(
            xml, "", f"{self.base}Article/Journal/ISSN[@IssnType='Electronic']"
        )

        strJournaltitle = self.find(xml, "", f"{self.base}Article/Journal/Title")

        strISOAbbreviation = self.find(
            xml, "", f"{self.base}Article/Journal/ISOAbbreviation"
        )

        intNLM_ID = self.find(xml, 0, f"{self.base}MedlineJournalInfo/NlmUniqueID")

        aPublicationType = []
        for item in xml.findall(
            f"{self.base}Article/PublicationTypeList/PublicationType"
        ):
            aPublicationType.append(item.text)

        strPublicationstypelist = self.seperatorColon.join(aPublicationType)

        strMeshheadingList = ""
        aMeshHeading = []
        for item in xml.findall(f"{self.base}MeshHeadingList/MeshHeading"):
            aQualifierName = []
            strQualifierName = ""
            tempMeshHeading = ""
            for itemQualifierName in item.findall("QualifierName"):
                aQualifierName.append(itemQualifierName.text)
            strQualifierName = self.seperatorComma.join(aQualifierName)
            descriptorName = item.find("DescriptorName").text
            if strQualifierName == "":
                tempMeshHeading = f"{descriptorName} - administration & dosage"
            else:
                tempMeshHeading = f"{descriptorName} - {strQualifierName}"
            aMeshHeading.append(tempMeshHeading)
        strMeshheadingList = self.seperatorColon.join(aMeshHeading)

        strPMC = self.find(
            xml, "", "PubmedArticle/PubmedData/ArticleIdList/ArticleId[@IdType='pmc']"
        )

        strPUBMedStatus = self.find(
            xml, "", "PubmedArticle/PubmedData/PublicationStatus"
        )

        strPubMedReceived = None
        if (
            xml.find(
                'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="received"]'
            )
            is not None
        ):
            # Date Object fürs Insert erstellen
            datePubmedReceived = datetime(
                int(
                    xml.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="received"]/Year'
                    ).text
                ),
                int(
                    xml.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="received"]/Month'
                    ).text
                ),
                int(
                    xml.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="received"]/Day'
                    ).text
                ),
            )
            strPubMedReceived = datePubmedReceived.strftime("%Y-%m-%d")

        strPubMedAccepted = None
        if (
            xml.find(
                'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="accepted"]'
            )
            is not None
        ):
            # Date Object fürs Insert erstellen
            datePubmedAccepted = datetime(
                int(
                    xml.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="accepted"]/Year'
                    ).text
                ),
                int(
                    xml.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="accepted"]/Month'
                    ).text
                ),
                int(
                    xml.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="accepted"]/Day'
                    ).text
                ),
            )
            strPubMedAccepted = datePubmedAccepted.strftime("%Y-%m-%d")

        aAutor = []
        for item in xml.findall(f"{self.base}Article/AuthorList/Author"):
            lastName = item.find("LastName")
            if lastName is not None:
                initials = item.find("Initials")
                if initials is not None:
                    aAutor.append(f"{lastName.text}, {initials.text}")
                else:
                    aAutor.append(lastName.text)
            if item.find("CollectiveName"):
                aAutor.append(item.find("CollectiveName").text)
        strAuthorList = self.seperatorSemicolon.join(aAutor)

        with con.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT COUNT(1) AS count FROM {schema}.pubmed_suche_id_detail WHERE SUCHE_ID=? AND PUBMED_ID=?
                """,
                search,
                pubmed,
            )
            row = cursor.fetchone()
            logger.debug(f"Found {row.COUNT} rows for search {search} pubmed {pubmed}")
            if row.COUNT == 0:
                logger.debug(f"Inserting details for search {search} pubmed {pubmed}")
                cursor.execute(
                    f"""
                    INSERT INTO
                        {schema}.pubmed_suche_id_detail
                    (
                        SUCHE_ID,
                        PUBMED_ID,
                        PUBDATE,
                        ARTICLETITLE,
                        DOI,
                        LANGUAGE,
                        ABSTRACTTEXT,
                        VOLUME,
                        ISSUE,
                        PAGINATION,
                        ISSN_PRINT,
                        ISSN_ELECTRONIC,
                        JOURNALTITLE,
                        ISOABBREVIATION,
                        NLM_ID,
                        PUBLICATIONTYPELIST,
                        MESHHEADINGLIST,
                        PMC,
                        PUBMEDSTATUS,
                        PUBDATE_ALTERNATIV,
                        PUBDATE_RECEIVED,
                        PUBDATE_ACCEPTED,
                        AUTHOR_LIST
                    )
                    VALUES
                    (
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        ?,
                        to_date(?, 'YYYY-MM-DD'),
                        to_date(?, 'YYYY-MM-DD'),
                        ?
                    )
                    """,
                    search,
                    pubmed,
                    int(intPubDate),
                    strArticleTitle,
                    strDoi,
                    strLanguage,
                    strAbstractText,
                    strVolume,
                    strIssue,
                    strPagination,
                    strISSNPrint,
                    strISSNElectronic,
                    strJournaltitle,
                    strISOAbbreviation,
                    intNLM_ID,
                    strPublicationstypelist,
                    strMeshheadingList,
                    strPMC,
                    strPUBMedStatus,
                    intPubDateAlternative,
                    strPubMedReceived,
                    strPubMedAccepted,
                    strAuthorList,
                )
            else:
                logger.debug(f"Skipping details for search {search} pubmed {pubmed}")
                # logger.debug(f"Updating details for search {search} pubmed {pubmed}")
                # cursor.execute(
                #    """
                #    UPDATE
                #        pubmed_suche_id_detail
                #    SET
                #        PUBDATE = ?,
                #        ARTICLETITLE = ?,
                #        DOI = ?,
                #        LANGUAGE = ?,
                #        ABSTRACTTEXT = ?,
                #        VOLUME = ?,
                #        ISSUE = ?,
                #        PAGINATION = ?,
                #        ISSN_PRINT = ?,
                #        ISSN_ELECTRONIC = ?,
                #        JOURNALTITLE = ?,
                #        ISOABBREVIATION = ?,
                #        NLM_ID = ?,
                #        PUBLICATIONTYPELIST = ?,
                #        MESHHEADINGLIST = ?,
                #        PMC = ?,
                #        PUBMEDSTATUS = ?,
                #        PUBDATE_ALTERNATIV = ?,
                #        PUBDATE_RECEIVED = ?,
                #        PUBDATE_ACCEPTED = ?,
                #        AUTHOR_LIST = ?
                #    WHERE
                #        SUCHE_ID = ? AND
                #        PUBMED_ID = ?
                #    """,
                #    int(intPubDate),
                #    strArticleTitle,
                #    strDoi,
                #    strLanguage,
                #    strAbstractText,
                #    strVolume,
                #    strIssue,
                #    strPagination,
                #    strISSNPrint,
                #    strISSNElectronic,
                #    strJournaltitle,
                #    strISOAbbreviation,
                #    intNLM_ID,
                #    strPublicationstypelist,
                #    strMeshheadingList,
                #    strPMC,
                #    strPUBMedStatus,
                #    intPubDateAlternative,
                #    strPubMedReceived,
                #    strPubMedAccepted,
                #    strAuthorList,
                #    search,
                #    pubmed,
                # )

    def save_authors(self, search, pubmed, xml, con, schema):

        for item in xml.findall(f"{self.base}Article/AuthorList/Author"):

            strLastname = self.find(item, "", "LastName")
            strForename = self.find(item, "", "ForeName")
            strInitials = self.find(item, "", "Initials")

            strAffiliation = " ".join(
                map(lambda a: a.text, item.findall("AffiliationInfo/Affiliation"))
            )

            strIdentifierPerson = self.find(item, "", "Identifier[@Source='ORCID']")
            strIdentifierORGE = self.find(
                item, "", "AffiliationInfo/Identifier[@Source='RINGGOLD']"
            )
            strCollectiveName = self.find(item, "", "CollectiveName")

            with con.cursor() as cursor:
                cursor.execute(
                    f"""
                    INSERT INTO
                        {schema}.pubmed_suche_autoren
                    (
                        SUCHE_ID,
                        PUBMED_ID,
                        LASTNAME,
                        FORENAME,
                        INITIALS,
                        AFFILIATION,
                        IDENTIFIER_PERSON,
                        IDENTIFIER_ORGE,
                        COLLECTIVE_NAME
                    )
                    VALUES
                    (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    search,
                    pubmed,
                    strLastname,
                    strForename,
                    strInitials,
                    strAffiliation,
                    strIdentifierPerson,
                    strIdentifierORGE,
                    strCollectiveName,
                )

    def save_sponsorships(self, search, pubmed, xml, con, schema):

        for item in xml.findall(f"{self.base}Article/GrantList/Grant"):
            strGrant_ID = self.find(item, None, "GrantID")
            strFoerd_Inst = self.find(item, None, "Agency")
            strFoerd_Land = self.find(item, None, "Country")

            with con.cursor() as cursor:
                cursor.execute(
                    f"""INSERT INTO
                        {schema}.pubmed_suche_foerderungen
                    (
                        SUCHE_ID,
                        PUBMED_ID,
                        GRANT_ID,
                        FOERD_INST,
                        FOERD_LAND
                    )
                    VALUES
                    (
                        ?, ?, ?, ?, ?
                    )""",
                    search,
                    pubmed,
                    strGrant_ID,
                    strFoerd_Inst,
                    strFoerd_Land,
                )

    def save_mesh(self, search, pubmed, xml, con, schema):
        for item in xml.findall(f"{self.base}MeshHeadingList/MeshHeading"):
            if item.find("DescriptorName") is None:
                continue
            strDescriptor_Name = item.find("DescriptorName").text
            strDescriptor_UI = item.find("DescriptorName").get("UI")
            strMajortopic_Desc_JN = item.find("DescriptorName").get("MajorTopicYN")

            if item.find("QualifierName") is None:
                self.save_mesh_insert(
                    search,
                    pubmed,
                    con,
                    schema,
                    strDescriptor_UI,
                    strDescriptor_Name,
                    strMajortopic_Desc_JN,
                    "",
                    "",
                    "",
                )
            else:
                for item2 in item.findall("QualifierName"):
                    strQualifier_Name = item2.text
                    strQualifier_UI = item2.get("UI")
                    strMajortopic_Quali_JN = item2.get("MajorTopicYN")

                    self.save_mesh_insert(
                        search,
                        pubmed,
                        con,
                        schema,
                        strDescriptor_UI,
                        strDescriptor_Name,
                        strMajortopic_Desc_JN,
                        strQualifier_UI,
                        strQualifier_Name,
                        strMajortopic_Quali_JN,
                    )

    def save_mesh_insert(
        self,
        search,
        pubmed,
        con,
        schema,
        strDescriptor_UI,
        strDescriptor_Name,
        strMajortopic_Desc_JN,
        strQualifier_UI,
        strQualifier_Name,
        strMajortopic_Quali_JN,
    ):
        with con.cursor() as cursor:
            cursor.execute(
                f"""
                INSERT INTO
                    {schema}.pubmed_suche_mesh
                (
                    SUCHE_ID,
                    PUBMED_ID,
                    DESCRIPTOR_UI,
                    DESCRIPTOR_NAME,
                    MAJORTOPIC_DESC_JN,
                    QUALIFIER_UI,
                    QUALIFIER_NAME,
                    MAJORTOPIC_QUALI_JN
                )
                VALUES
                (
                    ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                search,
                pubmed,
                strDescriptor_UI,
                strDescriptor_Name,
                strMajortopic_Desc_JN,
                strQualifier_UI,
                strQualifier_Name,
                strMajortopic_Quali_JN,
            )
