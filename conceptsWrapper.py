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
        self.antonyms = {}
        self.broaders = {}
        self.narrowers = {}
        self.related = {}

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

    # add a new antonym phrase to the Antonyms dictionary
    def addAntonyms(self,labelText,labelCount):
        self.antonyms[labelText] = labelCount

    # add a new broader phrase to the Broaders dictionary
    def addBroaders(self,labelText,labelCount):
        self.broaders[labelText] = labelCount

    # add a new narrower phrase to the Narrowers dictionary
    def addNarrowers(self,labelText,labelCount):
        self.narrowers[labelText] = labelCount

    # add a new related phrase to the Ralated dictionary
    def addRalted(self,labelText,labelCount):
        self.related[labelText] = labelCount
# PG: typo in name of method

    # Update prefLabel count
    def updatePrefLabels(self,labelText,newCount):
        self.prefLables[labelText] = newCount

    # Update altLable count
    def updateAltLabels(self,labelText,newCount):
        self.altLabels[labelText] = newCount

    # Update acronyms count
    def updateAcronyms(self,labelText,newCount):
        self.acronyms[labelText] = newCount

# PG: the add and update methods are identical. I don't see a reason to have separate methods. 
#     Getters and setters are relatively uncommon in Python. It's more common to directly access the fields. If it at some point necessary
#     to run specific code on accessing the field, it's more common to use `@property` (https://docs.python.org/3/library/functions.html#property)

if __name__ == '__main__':
    
# PG: The main function is very long. I would move blocks of code that do one thing (e.g. read and parse the RDF file, initialize the concept list) into 
#     functions
    #pltHistogram()
    headers = {'user_agent': 'Srinivas class project;ver 1.0;email = spc6ph@virginia.edu;language = Python 3.8.12; platform = windows 10'}

    reqString = requests.get('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', headers=headers)
    xmlRDFString = bs4.BeautifulSoup(reqString.text, "xml")

    # Create and initialize a list to store Concept objects
    conceptList = []

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

        for item in pref.find_all('broader'):
            conceptObj.addBroaders(item.text,0)

        for item in pref.find_all('narrower'):
            conceptObj.addNarrowers(item.text,0)

        for item in pref.find_all('antonyms'):
            conceptObj.addAntonyms(item.text,0)

        for item in pref.find_all('related'):
            conceptObj.addRalted(item.text,0)
        
        conceptList.append(conceptObj)

    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')
    # Get all acronym phrases
    phraseList = rdf.customTagList("acronym")

    print(phraseList)
    # Read data files corpus and load matching acronym phrases
    filesList = ['a088p.txt'] #['a50p.txt', 'a088p.txt' ,'AI08_2016.txt','AI120_2017.txt','DTM-19-013.txt','DTM-20-002.txt']
    filePath = r"C:\\Users\\srini\\UVA-MSDS\\DS-6011-CAP\\Files\\"
    for fileName in filesList:
        fileObject = open(filePath + fileName, 'r')

        # Read data from the source file
        data = fileObject.read()

# PG: read files using context manager syntax (e.g. here you didn't close the fileObject, so in a long running application, this can cause issues)
# with open(filePath + fileName, 'r') as fileObject:
#     data = fileObject.read()

        data.replace(r"\n", " ")

        # Create tokens
        nltk_tokens = nltk.word_tokenize(data)

        # Get the matchig phrase count
        phCount = phraseCounts()
        # retDict = phCount.getPhraseCount(synonymsList,nltk_tokens)
        retDict = phCount.getPhraseFrequencyCount(phraseList, nltk_tokens)

    # Get the matching acronym phrases and counts in a dictionary object
    print(retDict)


    # Loop through the concepts list and update the corresponding matching acronym phrase count in the concept object list
    for count,con in enumerate(conceptList):
         for key in con.acronyms:
            for key1 in retDict:
                if key == key1:
                    con.updateAcronyms(key,retDict[key])
                    conceptList[count] = con
# PG: Is there a reason that you need to iterate over retDict? This should be identical (and faster as you remove a loop):
for count,con in enumerate(conceptList):
     for key in con.acronyms:
        if key in retDict:
            con.updateAcronyms(key,retDict[key])
            conceptList[count] = con
# the concept is an object that is modified, but not replaced. It is not necessary to assign it back to the list; the list 
# still contains the original, now modified object
for concept in conceptList:
    for key in concept.acronyms:
        if key in retDict:
            concept.updateAcronyms(key, retDict[key])

# PG: If you directly access the fields in the concept object, I think this can be simplified even more:

    # prefLabel
    phraseList = rdf.customTagList("prefLabel")
    retDict = phCount.getPhraseFrequencyCount(phraseList, nltk_tokens)

    # Loop through the concepts list and update the corresponding matching acronym phrase count
    # in the concept object list
    for count,con in enumerate(conceptList):
        for key in con.prefLables:
            for key1 in retDict:
                if key == key1:
                    con.updatePrefLabels(key,retDict[key])
                    conceptList[count] = con
# PG: the same applies here. 

    # AltLables
    phraseList = rdf.customTagList("altLabel")
    retDict = phCount.getPhraseFrequencyCount(phraseList, nltk_tokens)

    # Loop through the concepts list and update the corresponding matching acronym phrase count
    # in the concept object list
    for count, con in enumerate(conceptList):
        for key in con.altLabels:
            for key1 in retDict:
                if key == key1:
                    con.updateAltLabels(key, retDict[key])
                    conceptList[count] = con
# PG: and here


    print("UPDATED CONCEPTS LIST")
    for count, con in enumerate(conceptList):
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
