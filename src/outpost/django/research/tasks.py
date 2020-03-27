import datetime
import logging
from datetime import datetime
from xml.etree import ElementTree

import pyodbc
import requests
from celery.task import Task
from django.db import connection, transaction
from django.utils import timezone
from purl import URL

from .conf import settings

logger = logging.getLogger(__name__)


class DetailTask(Task):
    url = URL(settings.RESEARCH_API_BASE)

    def __init__(self):
        self.session = requests.Session()
        self.session.auth = (
            settings.RESEARCH_API_USERNAME,
            settings.RESEARCH_API_PASSWORD,
        )
        self.session.headers.update({"accept": "application/json"})

        # self.con = pyodbc.connect('DSN={}'.format(settings.RESEARCH_DSN))
        # Beispiel: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=24169358&rettyp=medline&retmode=xml

    #        self.url = ""
    # self.xmlStructurPubmedArticleMedlineCitation = "PubmedArticle/MedlineCitation/"

    # Seperatoren für die Umwandlung von Array auf String
    # self.seperatorColon = ' : '
    # self.seperatorSemicolon = '; '
    # self.seperatorBlank = ' '
    # self.seperatorComma = ', '

    # @transaction.atomic
    # def run(self, url, sucheID, pubmedIDS, **kwargs):
    def run(self, **kwargs):
        # self.intSucheID = sucheID
        # self.url = '%s/efetch.fcgi?db=pubmed&rettyp=medline&retmode=xml&id=' % (url)
        # self.pubmedIDS = pubmedIDS

        # begin = datetime.now()
        # print(self.url)

        # for id in self.pubmedIDS:
        # xmlData = self.getXMLFromID(id)
        # print(id)
        # self.saveDetail(id, xmlData)
        # self.saveAutoren(id, xmlData)
        # self.saveFoerderungen(id, xmlData)
        # self.saveMesh(id, xmlData)

        #        end = datetime.now()
        # time = end - begin
        # print(time)
        pass

    def getXMLFromID(self, id):
        tmpUrl = self.url + id
        response = requests.get(tmpUrl, timeout=5)
        xmlData = ElementTree.fromstring(response.content)

        return xmlData

    def saveDetail(self, pubmedId, xmldoc):
        intPubDate = 0
        intPubDateAlternative = 0
        if (
            xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "Article/Journal/JournalIssue/PubDate/Year"
            )
        ) is not None:
            intPubDate = xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "Article/Journal/JournalIssue/PubDate/Year"
            ).text
        else:
            if (
                xmldoc.find(
                    'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="pubmed"]'
                )
            ) is not None:
                intPubDateAlternative = xmldoc.find(
                    'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="pubmed"]/Year'
                ).text

        strArticleTitle = ""
        if (
            xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation + "Article/ArticleTitle"
            )
        ) is not None:
            strArticleTitle = xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation + "Article/ArticleTitle"
            ).text

        strDoi = ""
        if (
            xmldoc.find(
                'PubmedArticle/PubmedData/ArticleIdList/ArticleId[@IdType="doi"]'
            )
        ) is not None:
            strDoi = xmldoc.find(
                'PubmedArticle/PubmedData/ArticleIdList/ArticleId[@IdType="doi"]'
            ).text
        else:
            if (
                xmldoc.find(
                    self.xmlStructurPubmedArticleMedlineCitation
                    + 'Article/ELocationID[@EIdType="doi"]'
                )
            ) is not None:
                strDoi = xmldoc.find(
                    self.xmlStructurPubmedArticleMedlineCitation
                    + 'Article/ELocationID[@EIdType="doi"]'
                ).text

        strLanguage = ""
        if (
            xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation + "Article/Language"
            )
        ) is not None:
            strLanguage = xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation + "Article/Language"
            ).text

        strAbstractText = ""
        aAbstract = []
        for item in xmldoc.findall(
            self.xmlStructurPubmedArticleMedlineCitation
            + "Article/Abstract/AbstractText"
        ):
            strTemp = ""
            if (item.get("Label")) is not None:
                strTemp = item.get("Label") + ": "

            aAbstract.append(strTemp + item.text)
        strAbstractText = self.seperatorBlank.join(aAbstract)

        strVolume = ""
        if (
            xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "Article/Journal/JournalIssue/Volume"
            )
        ) is not None:
            strVolume = xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "Article/Journal/JournalIssue/Volume"
            ).text

        strIssue = ""
        if (
            xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "Article/Journal/JournalIssue/Issue"
            )
        ) is not None:
            strIssue = xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "Article/Journal/JournalIssue/Issue"
            ).text

        strPagination = ""
        if (
            xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "Article/Pagination/MedlinePgn"
            )
        ) is not None:
            strPagination = xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "Article/Pagination/MedlinePgn"
            ).text

        strISSNPrint = ""
        if (
            xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + 'Article/Journal/ISSN[@IssnType="Print"]'
            )
        ) is not None:
            strISSNPrint = xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + 'Article/Journal/ISSN[@IssnType="Print"]'
            ).text

        strISSNElectronic = ""
        if (
            xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + 'Article/Journal/ISSN[@IssnType="Electronic"]'
            )
        ) is not None:
            strISSNElectronic = xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + 'Article/Journal/ISSN[@IssnType="Electronic"]'
            ).text

        strJournaltitle = ""
        if (
            xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation + "Article/Journal/Title"
            )
        ) is not None:
            strJournaltitle = xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation + "Article/Journal/Title"
            ).text

        strISOAbbreviation = ""
        if (
            xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "Article/Journal/ISOAbbreviation"
            )
        ) is not None:
            strISOAbbreviation = xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "Article/Journal/ISOAbbreviation"
            ).text

        intNLM_ID = 0
        if (
            xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "MedlineJournalInfo/NlmUniqueID"
            )
        ) is not None:
            intNLM_ID = xmldoc.find(
                self.xmlStructurPubmedArticleMedlineCitation
                + "MedlineJournalInfo/NlmUniqueID"
            ).text

        aPublicationType = []
        for item in xmldoc.findall(
            self.xmlStructurPubmedArticleMedlineCitation
            + "Article/PublicationTypeList/PublicationType"
        ):
            aPublicationType.append(item.text)

        strPublicationstypelist = self.seperatorColon.join(aPublicationType)

        strMeshheadingList = ""
        aMeshHeading = []
        for item in xmldoc.findall(
            self.xmlStructurPubmedArticleMedlineCitation + "MeshHeadingList/MeshHeading"
        ):
            aQualifierName = []
            strQualifierName = ""
            tempMeshHeading = ""
            for itemQualifierName in item.findall("QualifierName"):
                aQualifierName.append(itemQualifierName.text)
            strQualifierName = self.seperatorComma.join(aQualifierName)
            if strQualifierName == "":
                tempMeshHeading = (
                    item.find("DescriptorName").text + " - administration & dosage"
                )
            else:
                tempMeshHeading = (
                    item.find("DescriptorName").text + " - " + strQualifierName
                )
            aMeshHeading.append(tempMeshHeading)
        strMeshheadingList = self.seperatorColon.join(aMeshHeading)

        strPMC = ""
        if (
            xmldoc.find(
                'PubmedArticle/PubmedData/ArticleIdList/ArticleId[@IdType="pmc"]'
            )
        ) is not None:
            strPMC = xmldoc.find(
                'PubmedArticle/PubmedData/ArticleIdList/ArticleId[@IdType="pmc"]'
            ).text

        strPUBMedStatus = xmldoc.find("PubmedArticle/PubmedData/PublicationStatus").text

        strPubMedReceived = None
        if (
            xmldoc.find(
                'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="received"]'
            )
        ) is not None:
            # Date Object fürs Insert erstellen
            datePubmedReceived = datetime(
                int(
                    xmldoc.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="received"]/Year'
                    ).text
                ),
                int(
                    xmldoc.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="received"]/Month'
                    ).text
                ),
                int(
                    xmldoc.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="received"]/Day'
                    ).text
                ),
            )
            strPubMedReceived = datePubmedReceived.strftime("%Y-%m-%d %H:%M:%S")

        strPubMedAccepted = None
        if (
            xmldoc.find(
                'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="accepted"]'
            )
        ) is not None:
            # Date Object fürs Insert erstellen
            datePubmedAccepted = datetime(
                int(
                    xmldoc.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="accepted"]/Year'
                    ).text
                ),
                int(
                    xmldoc.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="accepted"]/Month'
                    ).text
                ),
                int(
                    xmldoc.find(
                        'PubmedArticle/PubmedData/History/PubMedPubDate[@PubStatus="accepted"]/Day'
                    ).text
                ),
            )
            strPubMedAccepted = datePubmedReceived.strftime("%Y-%m-%d %H:%M:%S")

        aAutor = []
        for item in xmldoc.findall(
            self.xmlStructurPubmedArticleMedlineCitation + "Article/AuthorList/Author"
        ):
            if (item.find("LastName")) is not None:
                aAutor.append(
                    item.find("LastName").text + " " + item.find("Initials").text
                )
            if (item.find("CollectiveName")) is not None:
                aAutor.append(item.find("CollectiveName").text)
        strAuthorList = self.seperatorSemicolon.join(aAutor)

        with self.con.cursor() as cursor:
            try:
                cursor.execute(
                    """insert into pubmed_suche_id_detail (SUCHE_ID, PUBMED_ID, PUBDATE, ARTICLETITLE, DOI, LANGUAGE, ABSTRACTTEXT, VOLUME, ISSUE, PAGINATION, ISSN_PRINT, ISSN_ELECTRONIC, JOURNALTITLE,
                                    ISOABBREVIATION, NLM_ID, PUBLICATIONTYPELIST, MESHHEADINGLIST, PMC, PUBMEDSTATUS, PUBDATE_ALTERNATIV, PUBDATE_RECEIVED, PUBDATE_ACCEPTED, AUTHOR_LIST)
                                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    self.intSucheID,
                    int(pubmedId),
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
                    int(intNLM_ID),
                    strPublicationstypelist,
                    strMeshheadingList,
                    strPMC,
                    strPUBMedStatus,
                    intPubDateAlternative,
                    strPubMedReceived,
                    strPubMedAccepted,
                    strAuthorList,
                )
                cursor.commit()
            except pyodbc.Error as er:
                print(pubmedId)
                print(er)
        return xmldoc

    def saveAutoren(self, pubmedId, xmldoc):

        for item in xmldoc.findall(
            self.xmlStructurPubmedArticleMedlineCitation + "Article/AuthorList/Author"
        ):

            strLastname = ""
            strForename = ""
            strInitials = ""

            if (item.find("LastName")) is not None:
                strLastname = item.find("LastName").text
            if (item.find("ForeName")) is not None:
                strForename = item.find("ForeName").text
            if (item.find("Initials")) is not None:
                strInitials = item.find("Initials").text

            strAffiliation = ""
            for item2 in item.findall("AffiliationInfo/Affiliation"):
                strAffiliation += item2.text + " "

            strIdentifierPerson = ""
            strIdentifierORGE = ""
            strCollectiveName = ""

            if (item.find('Identifier[@Source="ORCID"]')) is not None:
                strIdentifierPerson = item.find('Identifier[@Source="ORCID"]').text
            if (
                item.find('AffiliationInfo/Identifier[@Source="RINGGOLD"]')
            ) is not None:
                strIdentifierORGE = item.find(
                    'AffiliationInfo/Identifier[@Source="RINGGOLD"]'
                ).text

            if (item.find("CollectiveName")) is not None:
                strCollectiveName = item.find("CollectiveName").text

            with self.con.cursor() as cursor:
                try:
                    cursor.execute(
                        """insert into pubmed_suche_autoren (SUCHE_ID, PUBMED_ID, LASTNAME, FORENAME, INITIALS, AFFILIATION, IDENTIFIER_PERSON, IDENTIFIER_ORGE, COLLECTIVE_NAME)
                                    values (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        self.intSucheID,
                        int(pubmedId),
                        strLastname,
                        strForename,
                        strInitials,
                        strAffiliation,
                        strIdentifierPerson,
                        strIdentifierORGE,
                        strCollectiveName,
                    )
                    cursor.commit()
                except pyodbc.Error as er:
                    print(pubmedId)
                    print(er)

        return xmldoc

    def saveFoerderungen(self, pubmedId, xmldoc):

        for item in xmldoc.findall(
            self.xmlStructurPubmedArticleMedlineCitation + "Article/GrantList/Grant"
        ):
            strGrant_ID = item.find("GrantID").text
            strFoerd_Inst = item.find("Agency").text
            strFoerd_Land = item.find("Country").text

            with self.con.cursor() as cursor:
                try:
                    cursor.execute(
                        """insert into pubmed_suche_foerderungen (SUCHE_ID, PUBMED_ID, GRANT_ID, FOERD_INST, FOERD_LAND)
                                    values (?, ?, ?, ?, ?)""",
                        self.intSucheID,
                        int(pubmedId),
                        strGrant_ID,
                        strFoerd_Inst,
                        strFoerd_Land,
                    )
                    cursor.commit()
                except pyodbc.Error as er:
                    print(pubmedId)
                    print(er)
        return xmldoc

    def saveMesh(self, pubmedId, xmldoc):
        for item in xmldoc.findall(
            self.xmlStructurPubmedArticleMedlineCitation + "MeshHeadingList/MeshHeading"
        ):
            strDescriptor_UI = ""
            strDescriptor_Name = ""
            strMajortopic_Desc_JN = ""
            if (item.find("DescriptorName")) is not None:
                strDescriptor_Name = item.find("DescriptorName").text
                strDescriptor_UI = item.find("DescriptorName").get("UI")
                strMajortopic_Desc_JN = item.find("DescriptorName").get("MajorTopicYN")

            strQualifier_UI = ""
            strQualifier_Name = ""
            strMajortopic_Quali_JN = ""
            if (item.find("QualifierName")) is not None:
                strQualifier_Name = item.find("QualifierName").text
                strQualifier_UI = item.find("QualifierName").get("UI")
                strMajortopic_Quali_JN = item.find("QualifierName").get("MajorTopicYN")

            with self.con.cursor() as cursor:
                try:
                    cursor.execute(
                        """insert into pubmed_suche_mesh (SUCHE_ID, PUBMED_ID, DESCRIPTOR_UI, DESCRIPTOR_NAME, MAJORTOPIC_DESC_JN, QUALIFIER_UI, QUALIFIER_NAME, MAJORTOPIC_QUALI_JN)
                                    values (?, ?, ?, ?, ?, ?, ?, ?)""",
                        self.intSucheID,
                        int(pubmedId),
                        strDescriptor_UI,
                        strDescriptor_Name,
                        strMajortopic_Desc_JN,
                        strQualifier_UI,
                        strQualifier_Name,
                        strMajortopic_Quali_JN,
                    )
                    cursor.commit()
                except pyodbc.Error as er:
                    print(pubmedId)
                    print(er)
                except pyodbc.ProgrammingError as er2:
                    print(pubmedId)
                    print(er2)
        return xmldoc
