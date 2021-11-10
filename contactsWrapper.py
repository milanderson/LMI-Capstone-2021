'''
* Module  : contactsWrapper
* Purpose : A wrapper to create contacts objects with all phrases and matching counts
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

    # Update prefLabel count
    def updatePrefLabels(self,labelText,newCount):
        self.prefLables[labelText] = newCount

    # Update altLable count
    def updateAltLabels(self,labelText,newCount):
        self.altLabels[labelText] = newCount

    # Update acronyms count
    def updateAcronyms(self,labelText,newCount):
        self.acronyms[labelText] = newCount

if __name__ == '__main__':
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

    print(phraseList )
    # Read data files corpus and load matching acronym phrases
    filesList = ['a088p.txt'] #['a50p.txt', 'a088p.txt' ,'AI08_2016.txt','AI120_2017.txt','DTM-19-013.txt','DTM-20-002.txt']
    filePath = r"C:\\Users\\srini\\UVA-MSDS\\DS-6011-CAP\\Files\\"
    for fileName in filesList:
        fileObject = open(filePath + fileName, 'r')

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


    # Loop through the concepts list and update the corresponding matching acronym phrase count in the concept object list
    for count,con in enumerate(conceptList):
        #print("Count : " + str(count))
        #print(con.about)
        #print(con.acronyms)

        for key in con.acronyms:
            #print(key)
            for key1 in retDict:
                if key == key1:
                    con.updateAcronyms(key,retDict[key])
                    conceptList[count] = con
                #print(key1)
                #print(retDict[key1])

    # PrefLables

    phraseList = rdf.customTagList("prefLabel")
    retDict = phCount.getPhraseFrequencyCount(phraseList, nltk_tokens)

    # Loop through the concepts list and update the corresponding matching acronym phrase count
    # in the concept object list
    for count,con in enumerate(conceptList):
        for key in con.prefLables:
            #print(key)
            for key1 in retDict:
                if key == key1:
                    con.updatePrefLabels(key,retDict[key])
                    conceptList[count] = con
                #print(key1)
                #print(retDict[key1])

    # AltLables

    phraseList = rdf.customTagList("altLabel")
    retDict = phCount.getPhraseFrequencyCount(phraseList, nltk_tokens)

    # Loop through the concepts list and update the corresponding matching acronym phrase count
    # in the concept object list
    for count, con in enumerate(conceptList):
        for key in con.altLabels:
            # print(key)
            for key1 in retDict:
                if key == key1:
                    con.updateAltLabels(key, retDict[key])
                    conceptList[count] = con
                # print(key1)
                # print(retDict[key1])

    print("UPDATED CONCEPTS LIST")
    for count, con in enumerate(conceptList):
        print("Concept # " + str(count))
        #print(con.about)
        print("\tprelabel")
        print(con.prefLables)
        print("\taltlabel")
        print(con.altLabels)
        print("\tacronym")
        print(con.acronyms)


    #con.updateAcronyms()
    #print(con.prefLables)

