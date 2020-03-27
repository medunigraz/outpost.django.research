import logging
from datetime import datetime
from xml.etree import ElementTree

import pyodbc
import requests
from braces.views import CsrfExemptMixin
from django.db import connection
from django.http import HttpResponse
from django.views.generic import View

from .conf import settings

# from .tasks import DetailTask


logger = logging.getLogger(__name__)


class SearchView(CsrfExemptMixin, View):
    # PubMed URL
    # Beispiel: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=gollinger[Author]+
    con = pyodbc.connect("DSN={}".format(settings.RESEARCH_DSN))
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    strSearchUrl = "%s/esearch.fcgi?db=pubmed&term=" % (url)
    # URL Platzhalter
    strAuthor = "[Author]"
    strPDAT = "[PDAT]"

    # GET Parameter
    strAutor1 = ""
    strAutor2 = ""
    strJahr = ""
    strKombination = ""
    strPersonID = ""
    strSuchDatum = ""
    intCounter = 1
    intSucheID = 0

    def post(self, request):
        # import pudb;pu.db #Debugger aktivieren
        # print(request.GET.get("autor1_in"))
        if request.POST.get("autor1_in") is not None:
            self.strAutor1 = request.POST.get("autor1_in")
            self.strSearchUrl += self.strAutor1.replace(" ", "+") + self.strAuthor

        if request.POST.get("autor2_in") is not None:
            self.strAutor2 = request.POST.get("autor2_in")
            self.strSearchUrl += "+" + self.strAutor2.replace(" ", "+") + self.strAuthor

        if request.POST.get("jahr_in") is not None:
            self.strJahr = request.POST.get("jahr_in")
            self.strSearchUrl += "+" + self.strJahr + self.strPDAT

        if request.POST.get("kombination_in") is not None:
            self.strKombination = request.POST.get("kombination_in")
            self.strSearchUrl += request.POST.get("kombination_in")

        if request.POST.get("suche_id_in") is not None:
            self.intSucheID = request.POST.get("suche_id_in")

        # TODO PersonID
        self.strPersonID = request.POST.get("person_id")

        x = datetime.now()
        # self.strSuchDatum = x.strftime("%d.%m.%y")
        self.strSuchDatum = x.strftime("%Y-%m-%d %H:%M:%S")

        response = requests.get(self.strSearchUrl, timeout=5)
        xmlData = ElementTree.fromstring(response.content)
        # print(xmlData)
        dData = self.prepareDataForDB(xmlData)
        # print(dData)

        response = self.writeInDB(dData)

        # DetailTask().run(self.url,  self.intSucheID, dData["IDList"]);

        return HttpResponse(response)

    def prepareDataForDB(self, xmlData):
        dictSearchData = {}
        aIDList = []
        for item in xmlData.findall("IdList/Id"):
            # print(item)
            aIDList.append(item.text)
        dictSearchData["IDList"] = aIDList
        dictSearchData["Count"] = xmlData.find("Count").text
        # print(dictSearchData)

        return dictSearchData

    def writeInDB(self, data):
        try:
            with self.con.cursor() as cursor:
                intPaketSize = 20
                intDatenpaket = 1

                cursor.execute(
                    "insert into pubmed_suche_treffer (suche_id, suchbegriff1, suchbegriff2, suchbegriff3, suchfeld_jahr, person_id, suchdatum, anzahl_treffer) values (?, ?, ?, ?, ?, ?, ?, ?) ",
                    self.intSucheID,
                    self.strAutor1,
                    self.strAutor2,
                    self.strKombination,
                    self.strJahr,
                    self.strPersonID,
                    self.strSuchDatum,
                    data["Count"],
                )

                cursor.commit()

            # Pubmed Suche IDs
            for pubmedId in data["IDList"]:
                self.intCounter = self.intCounter + 1

                with self.con.cursor() as cursorIDs:
                    cursorIDs.execute(
                        """insert into pubmed_suche_ids (suche_id, pubmed_id, datenpaket_nr) values (?, ?, ?) """,
                        self.intSucheID,
                        int(pubmedId),
                        int(intDatenpaket),
                    )
                    cursorIDs.commit()

                if self.intCounter > intPaketSize:
                    self.intCounter = 1
                    intDatenpaket = intDatenpaket + 1

            return "true"

        except pyodbc.Error as er:
            # print(pubmedId)
            # print(er)
            return er


class DetailView(CsrfExemptMixin, View):

    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    strDetailUrl = "%s/efetch.fcgi?db=pubmed&rettyp=medline&retmode=xml&id=" % (url)

    con = pyodbc.connect("DSN={}".format(settings.RESEARCH_DSN))

    xmlStructurPubmedArticleMedlineCitation = "PubmedArticle/MedlineCitation/"

    # Seperatoren für die Umwandlung von Array auf String
    seperatorColon = " : "
    seperatorSemicolon = "; "
    seperatorBlank = " "
    seperatorComma = ", "

    intSucheID = 0

    def post(self, request):
        begin = datetime.now()
        # print(self.url)

        id = 0

        if request.POST.get("suche_id_in") is not None:
            self.intSucheID = request.POST.get("suche_id_in")

        if request.POST.get("ids_in") is not None:
            ids = request.POST.get("ids_in").replace("[", "").replace("]", "")
            pubmedIDS = ids.split(",")

        # print(pubmedIDS)
        response = ""
        for pubmedID in pubmedIDS:
            id = pubmedID.strip()

            xmlData = self.getXMLFromID(id)

            response = self.saveDetail(id, xmlData)
            print(response)
            if response == "true":
                response = self.saveAutoren(id, xmlData)
            if response == "true":
                response = self.saveFoerderungen(id, xmlData)
            if response == "true":
                response = self.saveMesh(id, xmlData)
        print(response)
        return HttpResponse(response)

    def getXMLFromID(self, id):
        tmpUrl = self.strDetailUrl + id
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
        # print(self.intSucheID)
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
                return er
        return "true"

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
                    return er
        return "true"

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
                    return er
        return "true"

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
                    # print(pubmedId)
                    # print(er)
                    return er
                except pyodbc.ProgrammingError as er2:
                    # print(pubmedId)
                    # print(er2)
                    return er2
        return "true"
