'''
* Module  : getPhraseCount
* Purpose : Read a document and get the counts of matching of given phrases (multi-word)
*           Read the document and search for matching phrases (multi-word)
*           Get Phrase Counts
'''

import tokenize
import nltk
from rdfHandler import rdfObject
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# class to handle the phrase counts and related operations
class phraseCounts:
    phraseCount = {}
    phraseFrequency = []

    def __int__(self):
        self.phraseCount = {}
        self.phraseFrequency=[]

    def getPhraseCount(self,listPhrases=[],listTokens=[]):
        phraseList = listPhrases
        tokenList = listTokens

        self.phraseCount = {}
        self.phraseFrequency=[]

        countList = [0]*len(phraseList) # create and initialize an array with the given length of phraseList

        # Return a blank list if either phrase list or token list is blank
        if (len(phraseList) == 0 | len(tokenList) == 0):
            self.phraseCount = dict(zip(phraseList,countList))
            return([]) #(self.phraseCount)

        phrasePosition = 0
        for tempPhrase in phraseList:
            phrase_Tokens = nltk.word_tokenize(tempPhrase)

            tPosition = 0
            while tPosition < len(tokenList)-len(phrase_Tokens)+1:
                compPhrase = ""
                pCount = 0
                matchCount = 0
                while pCount < len(phrase_Tokens):
                    compPhrase = compPhrase + tokenList[tPosition + pCount]
                    if phrase_Tokens[pCount] == tokenList[tPosition+pCount]:
                        matchCount = matchCount + 1
                    pCount = pCount + 1
                if len(phrase_Tokens) == matchCount:
                    countList[phrasePosition] = countList[phrasePosition] + 1
                    self.phraseFrequency.append(tempPhrase)
                    if len(phrase_Tokens) > 1:
                        print("*** MATCHED ***")
                        print("tempPhrase : " + tempPhrase)
                        print("compPhrase : " + compPhrase)

                tPosition = tPosition + 1
            phrasePosition = phrasePosition + 1

        self.phraseCount = dict(zip(phraseList, countList))
        self.dictionaryHandler(phraseList, countList)
        return (self.phraseFrequency) #(self.phraseCount)

    # Update non-zero values in a dictionary
    def dictionaryHandler(self,lstPhrases, lstCounts):

        self.phraseCount = {}

        tempDict = dict(zip(lstPhrases, lstCounts))

        for keyDict, valDict in tempDict.items():
            if (valDict > 0):
                self.phraseCount[keyDict] = valDict


    def getPhraseFrequencyCount(self,listPhrases=[],listTokens=[]):
        phraseList = listPhrases
        tokenList = listTokens

        self.phraseCount = {}
        self.phraseFrequency=[]

        countList = [0]*len(phraseList) # create and initialize an array with the given length of phraseList

        # Return a blank list if either phrase list or token list is blank
        if (len(phraseList) == 0 | len(tokenList) == 0):
            self.phraseCount = dict(zip(phraseList,countList))
            return([]) #(self.phraseCount)

        phrasePosition = 0
        for tempPhrase in phraseList:
            phrase_Tokens = nltk.word_tokenize(tempPhrase)

            tPosition = 0
            while tPosition < len(tokenList)-len(phrase_Tokens)+1:
                compPhrase = ""
                pCount = 0
                matchCount = 0
                while pCount < len(phrase_Tokens):
                    compPhrase = compPhrase + tokenList[tPosition + pCount]
                    if phrase_Tokens[pCount] == tokenList[tPosition+pCount]:
                        matchCount = matchCount + 1
                    pCount = pCount + 1
                if len(phrase_Tokens) == matchCount:
                    countList[phrasePosition] = countList[phrasePosition] + 1
                    self.phraseFrequency.append(tempPhrase)
                    #if len(phrase_Tokens) > 1:
                    #    print("*** MATCHED ***")
                    #    print("tempPhrase : " + tempPhrase)
                    #    print("compPhrase : " + compPhrase)

                tPosition = tPosition + 1
            phrasePosition = phrasePosition + 1

        self.dictionaryHandler(phraseList, countList)
        return (self.phraseCount)


# Plot a graph
def pltAGraph(dictData):
    plt.bar(retDict.keys(), retDict.values(), width=.5)
    plt.show()


if __name__ == '__main__':

    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')

    synonymsList = rdf.synonymsList()

    filesList = ['a088p.txt','a50p.txt'] #,'AI08_2016.txt','AI120_2017.txt','DTM-19-013.txt','DTM-20-002.txt']
    filePath = r"C:\\Users\\srini\\UVA-MSDS\\DS-6011-CAP\\Files\\"
    for fileName in filesList:
        fileObject = open(filePath + fileName, 'r')

        data = fileObject.read()
        data.replace(r"\n", " ")

        nltk_tokens = nltk.word_tokenize(data)

        phCount = phraseCounts()
        #retDict = phCount.getPhraseCount(synonymsList,nltk_tokens)
        retDict = phCount.getPhraseFrequencyCount(synonymsList,nltk_tokens)

        pltAGraph(retDict)









