'''
* Module  : conceptsWrapper
* Purpose : A wrapper to create concept objects with all phrases and matching counts
*           Reads the RDF file, create contacts and updates counts using the other modules functionality
* Created : Oct-27-2021 : Srinivas -
'''

import requests
import bs4
from rdfHandler import rdfObject
from PhraseCounts import phraseCounts
import nltk
from datetime import datetime
import pandas as pd


# Concept object class to store all phrase counts
class Concept():
    conceptCounter = 0
    def __init__(self,aboutText=None):
        if aboutText == None:
            self.about = ""
        else:
            self.about = aboutText

        # Initialize variables to track various phrase counts
        Concept.conceptCounter += 1
        self.conceptId = Concept.conceptCounter
        self.prefLables = {}
        self.altLabels = {}
        self.acronyms = {}
        self.synonyms = {}

    # add a new preLabel phrase to the prefLabels dictionary
    def addPrefLabel(self,labelText,labelCount):
        if (labelCount == 0):
            self.prefLables[labelText] = 0
        else:
            if (isinstance(labelCount, int) ):
                self.prefLables[labelText] = self.prefLables[labelText]  + labelCount
            else:
                self.prefLables[labelText] = labelCount
        #self.prefLables[labelText] = labelCount

    # add a new altLabel phrase to the altLabels dictionary
    def addAltLabel(self,labelText,labelCount):
        if (labelCount == 0):
            self.altLabels[labelText] = 0
        else:
            if (isinstance(labelCount, int) ):
                self.altLabels[labelText] = self.altLabels[labelText]  + labelCount
            else:
                self.prefLables[labelText] = labelCount
        #self.altLabels[labelText] =  labelCount

    # add a new acronym phrase to the Acronyms dictionary
    def addAcronyms(self,labelText,labelCount):
        if (labelCount == 0):
            self.acronyms[labelText] = 0
        else:
            if (isinstance(labelCount, int) ):
                self.acronyms[labelText] = self.acronyms[labelText]  + labelCount
            else:
                self.prefLables[labelText] = labelCount

        #self.acronyms[labelText] =  labelCount

    # add a new synonym phrase to the Synonyms dictionary
    def addSynonyms(self,labelText,labelCount):
        self.synonyms[labelText] = labelCount

#     Getters and setters are relatively uncommon in Python. It's more common to directly access the fields. If it at some point necessary
#     to run specific code on accessing the field, it's more common to use `@property` (https://docs.python.org/3/library/functions.html#property)

# create and initialize Concept objects
# Open and reads the RDF document for all concept objects available and creates a list with ConceptObjects
# Also initializes the phrases in the Concept Objects (Synonyms, Acronyms, PrefLable and AltLabel)

def CreateConcepts():
    tConceptsList = []
    headers = {'user_agent': 'Srinivas class project;ver 1.0;email = spc6ph@virginia.edu;language = Python 3.8.12; platform = windows 10'}

    reqString = requests.get('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', headers=headers)
    xmlRDFString = bs4.BeautifulSoup(reqString.text, "xml")

    # Search for all "concept" tags to create Concpet objects list
    for pref in xmlRDFString.find_all('Concept'):

        # rdf:about an attribute to identify a concept object
        conceptObj = Concept(pref.attrs['rdf:about'])

        # Loop through the other phrases available and add to the concept object
        for item in pref.find_all('prefLabel'):
            conceptObj.addPrefLabel(item.text, 0)

        for item in pref.find_all('altLabel'):
            conceptObj.addAltLabel(item.text,0)

        for item in pref.find_all('acronym'):
            conceptObj.addAcronyms(item.text,0)

        for item in pref.find_all('synonym'):
            conceptObj.addSynonyms(item.text,0)

        tConceptsList.append(conceptObj)

    return (tConceptsList)

# Update matching phrase in the Concept objects
def UpdateConcepts(phraseType,conceptObjList,textTokens,documentName,docType):

    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')

    data = {'doc_name': 'dummyText.txt',
            'doc_type': 'test_type',
            'cocept_id': 0,
            'phrase_type': 'testLable',
            'phrase_text': 'test Phrase',
            'phrase_count': 0,
            'time_stamp': '01-01-1900 01:01:01'}
    tempDF = pd.DataFrame(data, index=[0])

    phraseList = rdf.customTagList("altLabel")

    phCount = phraseCounts()
    retDictAltLabels = phCount.getPhraseFrequencyCount(phraseList, textTokens)

    phraseList = rdf.customTagList("prefLabel")

    phCount = phraseCounts()
    retDictPrefLabels = phCount.getPhraseFrequencyCount(phraseList, textTokens)


    phraseList = rdf.customTagList("acronym")

    phCount = phraseCounts()
    retDictAcronyms = phCount.getPhraseFrequencyCount(phraseList, textTokens)

    # Loop through the concepts list and update the corresponding matching acronym phrase count
    # in the concept object list

    if (phraseType == "allLabels"):
        for count, con in enumerate(conceptObjList):

            #[writeToDataFrame(sourceDF,documentName,con.conceptId,'altLabel',key) for key in list(con.altLabels.keys()) if key in retDictAltLabels.keys()]
            #[writeToDataFrame(sourceDF,documentName,con.conceptId,'prefLabel',key) for key in list(con.prefLables.keys()) if key in retDictPrefLabels.keys()]
            #[writeToDataFrame(sourceDF,documentName,con.conceptId,'acronym',key) for key in list(con.acronyms.keys()) if key in retDictAcronyms.keys()]

            # Update the ConceptObjects
            #[con.addAltLabel(key, retDictAltLabels[key]) for key in list(con.altLabels.keys()) if key in retDictAltLabels.keys()]
            #[con.addPrefLabel(key, retDictPrefLabels[key]) for key in list(con.prefLables.keys()) if key in retDictPrefLabels.keys()]
            #[con.addAcronyms(key, retDictAcronyms[key]) for key in list(con.acronyms.keys()) if key in retDictAcronyms.keys()]

            #[con.addAltLabel(key, retDictAltLabels[key]) for key in list(con.altLabels.keys()) if key in retDictAltLabels.keys()]
            #[con.addPrefLabel(key, retDictPrefLabels[key]) for key in list(con.prefLables.keys()) if key in retDictPrefLabels.keys()]
            #[con.addAcronyms(key, retDictAcronyms[key]) for key in list(con.acronyms.keys()) if key in retDictAcronyms.keys()]


            for key in con.altLabels:
                for key1 in retDictAltLabels:
                    if key == key1:
                        #con.addAltLabel(key, retDictAltLabels[key])
                        tempDF = tempDF.append(writeToDataFrame(documentName,docType, con.conceptId, 'altLabel', key,retDictAltLabels[key]))
            for key in con.prefLables:
                for key1 in retDictPrefLabels:
                    if key == key1:
                        #con.addPrefLabel(key, retDictPrefLabels[key])
                        tempDF = tempDF.append(writeToDataFrame(documentName,docType, con.conceptId, 'prefLabel', key,retDictPrefLabels[key]))
            for key in con.acronyms:
                for key1 in retDictAcronyms:
                    if key == key1:
                        #con.addAcronyms(key, retDictAcronyms[key])
                        tempDF = tempDF.append(writeToDataFrame(documentName,docType, con.conceptId, 'acronym', key,retDictAcronyms[key]))

    return (tempDF)

    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')

    phraseList = rdf.customTagList(phraseType)

    phCount = phraseCounts()
    retDict = phCount.getPhraseFrequencyCount(phraseList, textTokens)

    if (phraseType == "altLabel"):
        for count, con in enumerate(conceptObjList):
            for key in con.altLabels:
                for key1 in retDict:
                    if key == key1:
                        con.addAltLabel(key, retDict[key])

    if (phraseType == "prefLabel"):
        for count, con in enumerate(conceptObjList):
            for key in con.prefLables:
                for key1 in retDict:
                    if key == key1:
                        con.addPrefLabel(key, retDict[key])

    if (phraseType == "acronym"):
        for count, con in enumerate(conceptObjList):
            for key in con.acronyms:
                for key1 in retDict:
                    if key == key1:
                        con.addAcronyms(key, retDict[key])


# Print the Concept Objects List
def PrintConcepts(conceptObjList):
    print("UPDATED CONCEPTS LIST")
    for count, con in enumerate(conceptObjList):
        print("===================")
        print("CONCEPT # " + str(count))
        print(con.conceptId)
        print(con.about)
        print("===================")
        print("\tprelabel")
        print(con.prefLables)
        print("\taltlabel")
        print(con.altLabels)
        print("\tacronym")
        print(con.acronyms)


def logEvents(logText):
    print(datetime.now().strftime("%H:%M:%S") + " - " + logText)

##########################
# Read the documents text data from the data frame
##########################
def ReadData(retRowNum):
    dataDF = pd.read_csv("full_dataframe.csv")
    return (dataDF['file_name'][retRowNum],dataDF['raw_text'][retRowNum],dataDF['doc_type'][retRowNum])

# Append an entry to a data frame
def writeToDataFrame(docName,docType,conceptId,phraseType,phraseText,phraseCount):
    data = {'doc_name': docName,
            'doc_type': docType,
            'cocept_id': conceptId,
            'phrase_type': phraseType,
            'phrase_text': phraseText,
            'phrase_count': phraseCount,
            'time_stamp': datetime.now()}
    #srcDF = srcDF.append(pd.DataFrame(data, index=[0]))
    df = pd.DataFrame(data, index=[0])
    return (df)
if __name__ == '__main__':

# PG: The main function is very long. I would move blocks of code that do one thing (e.g. read and parse the RDF file, initialize the concept list) into 
#     functions
    #pltHistogram()


    # Create and initialize a list to store Concept objects
    #conceptList = []

    logEvents("1...")
    conceptList = CreateConcepts()

    #logEvents("2...")
    #rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')

    # Get all acronym phrases
    #phraseList = rdf.customTagList("acronym")

    #print(phraseList)

    '''
    # Read data files corpus and load matching acronym phrases
    filesList = ['a088p.txt','a50p.txt','AI08_2016.txt','AI120_2017.txt','DTM-19-013.txt','DTM-20-002.txt']
    #['a088p.txt','a50p.txt','AI08_2016.txt','AI120_2017.txt','DTM-19-013.txt','DTM-20-002.txt']
    filePath = r"C:\\Users\\srini\\UVA-MSDS\\DS-6011-CAP\\Files\\"
    nltk_tokens = []
    for fileName in filesList:
        with open(filePath + fileName, 'r') as fileObject:
            # Read data from the source file
            data = fileObject.read()

        data.replace(r"\n", " ")

        # Create tokens
        nltk_tokens = nltk_tokens + nltk.word_tokenize(data)

        # Get the matching phrase count
        #phCount = phraseCounts()

        # retDict = phCount.getPhraseCount(synonymsList,nltk_tokens)
        #retDict = phCount.getPhraseFrequencyCount(phraseList, nltk_tokens)
    '''
    data = {'doc_name' : 'dummyText.txt',
            'doc_type' : 'test_type',
            'cocept_id' : 0,
            'phrase_type' : 'testLable',
            'phrase_text' : 'test Phrase',
            'phrase_count' : 0,
            'time_stamp' : '01-01-1900 01:01:01'}
    dataDF = pd.DataFrame(data,index=[0])

    for i in range(1,5,1):
        logEvents("Start the iteration..." + str(i))
        docName,data,docType = ReadData(i)
        print('Document Name :')
        print(docName)
        logEvents("Read the data...")
        data.replace(r"\n", " ")

        # Create tokens
        nltk_tokens = nltk.word_tokenize(data)

        logEvents("Tokenized the data...")
        # PG: If you directly access the fields in the concept object, I think this can be simplified even more:

        # allLabels
        df = UpdateConcepts("allLabels",conceptList,nltk_tokens,docName,docType)
        dataDF = dataDF.append(df)

        logEvents("Processed allLabels...")

        """
        # Acronyms
        UpdateConcepts("acronym", conceptList,nltk_tokens)
        logEvents("Processed Acronyms...")
        # prefLabel
        UpdateConcepts("prefLabel",conceptList,nltk_tokens)
        logEvents("Processed preflabels...")
        # AltLables
        UpdateConcepts("altLabel",conceptList,nltk_tokens)
        logEvents("Processed altlabels...")
        """

    dataDF
    # Print the Cocepts List
    PrintConcepts(conceptList)
    logEvents("Printed Concept Objects...")



