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

# Concept object class to store all phrase counts
class Concept():

    def __init__(self,aboutText=None):
        if aboutText == None:
            self.about = ""
        else:
            self.about = aboutText

        # Initialize variables to track various phrase counts
        self.prefLables = {}
        self.altLabels = {}
        self.acronyms = {}
        self.synonyms = {}

    # add a new preLabel phrase to the prefLabels dictionary
    def addPrefLabel(self,labelText,labelCount):
        self.prefLables[labelText] = labelCount

    # add a new altLabel phrase to the altLabels dictionary
    def addAltLabel(self,labelText,labelCount):
        self.altLabels[labelText] = labelCount

    # add a new acronym phrase to the Acronyms dictionary
    def addAcronyms(self,labelText,labelCount):
        self.acronyms[labelText] = labelCount

    # add a new synonym phrase to the Synonyms dictionary
    def addSynonyms(self,labelText,labelCount):
        self.synonyms[labelText] = labelCount

#     Getters and setters are relatively uncommon in Python. It's more common to directly access the fields. If it at some point necessary
#     to run specific code on accessing the field, it's more common to use `@property` (https://docs.python.org/3/library/functions.html#property)

# create and initialize Concept objects
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
def UpdateConcepts(phraseType,conceptObjList):

    phraseList = rdf.customTagList(phraseType)
    retDict = phCount.getPhraseFrequencyCount(phraseList, nltk_tokens)

    # Loop through the concepts list and update the corresponding matching acronym phrase count
    # in the concept object list
    if (phraseType == "altLabel"):
        for count, con in enumerate(conceptList):
            for key in con.altLabels:
                for key1 in retDict:
                    if key == key1:
                        con.addAltLabel(key, retDict[key])
                        #conceptList[count] = con

    if (phraseType == "prefLabel"):
        for count, con in enumerate(conceptList):
            for key in con.prefLables:
                for key1 in retDict:
                    if key == key1:
                        con.addPrefLabel(key, retDict[key])
                        #conceptList[count] = con

    if (phraseType == "acronym"):
        for count, con in enumerate(conceptList):
            for key in con.acronyms:
                for key1 in retDict:
                    if key == key1:
                        con.addAcronyms(key, retDict[key])
                        #conceptList[count] = con




# Print the Concept Objects List
def PrintConcepts(conceptObjList):
    print("UPDATED CONCEPTS LIST")
    for count, con in enumerate(conceptObjList):
        print("===================")
        print("CONCEPT # " + str(count))
        print(con.about)
        print("===================")
        print("\tprelabel")
        print(con.prefLables)
        print("\taltlabel")
        print(con.altLabels)
        print("\tacronym")
        print(con.acronyms)

if __name__ == '__main__':

# PG: The main function is very long. I would move blocks of code that do one thing (e.g. read and parse the RDF file, initialize the concept list) into 
#     functions
    #pltHistogram()


    # Create and initialize a list to store Concept objects
    #conceptList = []
    conceptList = CreateConcepts()


    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')
    # Get all acronym phrases
    phraseList = rdf.customTagList("acronym")

    print(phraseList)
    # Read data files corpus and load matching acronym phrases
    filesList = ['a088p.txt'] #['a50p.txt', 'a088p.txt' ,'AI08_2016.txt','AI120_2017.txt','DTM-19-013.txt','DTM-20-002.txt']
    filePath = r"C:\\Users\\srini\\UVA-MSDS\\DS-6011-CAP\\Files\\"
    for fileName in filesList:
        with open(filePath + fileName, 'r') as fileObject:
            # Read data from the source file
            data = fileObject.read()

        data.replace(r"\n", " ")

        # Create tokens
        nltk_tokens = nltk.word_tokenize(data)

        # Get the matchig phrase count
        phCount = phraseCounts()
        # retDict = phCount.getPhraseCount(synonymsList,nltk_tokens)
        retDict = phCount.getPhraseFrequencyCount(phraseList, nltk_tokens)

    # Get the matching acronym phrases and counts in a dictionary object
    print(retDict)



# PG: If you directly access the fields in the concept object, I think this can be simplified even more:
    # Acronyms
    UpdateConcepts("acronym", conceptList)

    # prefLabel
    UpdateConcepts("prefLabel",conceptList)

    # AltLables
    UpdateConcepts("altLabel",conceptList)

    # Print the Cocepts List
    PrintConcepts(conceptList)




