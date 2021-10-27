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

    # Update acronyms count
    def updateAcronyms(self,labelText,newCount):
        self.acronyms[labelText] = newCount

if __name__ == '__main__':
    #pltHistogram()
    headers = {'user_agent': 'Srinivas class project;ver 1.0;email = spc6ph@virginia.edu;language = Python 3.8.12; platform = windows 10'}

    reqString = requests.get('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', headers=headers)
    xmlRDFString = bs4.BeautifulSoup(reqString.text, "xml")
    print([f.string for f in xmlRDFString.find_all('acronym')])


    conceptList = []

    for pref in xmlRDFString.find_all('Concept'):

        #print("*** CONCEPT *** : " + pref.attrs['rdf:about'])
        #print("==================")
        #print("prefLable : " + pref.find("prefLabel").text)
        #print("altLable : " + pref.find("altLabel").text)
        #print("acronym : " + pref.find("acronym").text)

        # pref.find_all("synonym")[0].text
        conceptObj = Concept(pref.attrs['rdf:about'])

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

    for con in conceptList:
        print("================ " )
        print("*** CONCEPT *** : " + con.about)
        print("================ " )
        if (len(con.prefLables) > 0):
            print("---> PrefLables : " )
            print(con.prefLables)

        if (len(con.altLabels) > 0):
            print("---> AltLabels : " )
            print(con.altLabels)

        if (len(con.acronyms) > 0):
            print("---> Acronyms : " )
            print(con.acronyms)
        if (len(con.synonyms) > 0):
            print("---> Synonyms : " )
            print(con.synonyms)
        if (len(con.antonyms) > 0):
            print("---> Antonyms : " )
            print(con.antonyms)
        if (len(con.broaders) > 0):
            print("---> Broaders : " )
            print(con.broaders)
        if (len(con.narrowers) > 0):
            print("---> Narrowers : " )
            print(con.narrowers)
        if (len(con.related) > 0):
            print("---> Related : " )
            print(con.related)

    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')
    phraseList = rdf.customTagList("acronym")

    filesList = ['a50p.txt', 'a088p.txt']  # ,'AI08_2016.txt','AI120_2017.txt','DTM-19-013.txt','DTM-20-002.txt']
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

    # conceptObj.updateAcronyms("ZI", 10)
    print(retDict)
    for con in conceptList:
        print(con.about)
        print(con.acronyms)
        for key in con.acronyms:
            print(key)


        #con.updateAcronyms()
    #print(con.prefLables)

