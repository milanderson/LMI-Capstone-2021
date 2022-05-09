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

# csv output from the DocExtract.py to a .txt file composed of a list of the document's contents
# getting prepared to be tokenized

# =============================================================================
# fileObject = pd.read_csv('/Users/abigailbernhardt/Desktop/UVA/Fall 2021/DS 6011 - Capstone/full_dataframeV3.csv', encoding = "utf8", engine="python", names=["doc_type", "file_name", "raw_text", "cleaned_text", "cleaned_text_list", "url", "acronyms", "glossary"])
# 
# #fileObject['cleaned_text_tokenized'] = fileObject.apply(lambda row: nltk.word_tokenize(row['cleaned_text']), axis=1)
# fileObject.loc[fileObject.doc_type == "admin%20instructions", "doc_type"] = "admin instructions"
# data_list = fileObject['cleaned_text'].tolist()
# 
# output_file = open('data_list.txt', 'w')
# 
# for datalist in data_list:
#     output_file.write(datalist)
# 
# output_file.close() 
# =============================================================================


# class to handle the phrase counts and related operations
# PG: The convention in Python is to capitalize class names - here PhraseCount
class phraseCounts:
# PG: If you don't use class fields, initialize your variables in the __init__ method (as you already do). These two lines are not required
    phraseCount = {}
    phraseFrequency = []

    def __int__(self):
        self.phraseCount = {}
        self.phraseFrequency=[]

# PG: Move the description of the method into the method like this. This will then work as documentation
    def getPhraseCount(self,listPhrases=[],listTokens=[]):
        """ Returns a list of matching phrases. 
        Keeping for a backward compatibility. It was replaced with getPhraseFrequencyCount """
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
# PG: You can rewrite this function into a single statement using a dictionary comprehension
# 
# self.phraseCount = {key: value for key, value in zip(lstPhrases, lstCounts) if value > 0}
# 
# This avoids the temporary generation of the dictionary tempDict and because the code is more 
# compact, it will also be easier to understand (once you get used to list, set, or dictionary comprehensions)
#
# The name of the function is not descriptive. You could call it for example updatePhraseCount 

    # Returns a dictionary with matching phrases as keys and frequency as values
    def getPhraseFrequencyCount(self,listPhrases=[],listTokens=[]):
        phraseList = listPhrases
        tokenList = listTokens
# PG: there was some dicussion on slack about the use of initialization of keyword arguments with mutables. This should only 
# be done in very rare cases as it can lead to unwanted side effects. Use the following instead:
# def getPhraseFrequencyCount(self, listPhrases=None, listTokens=None):
#     phraseList = listPhrases or []
#     tokenList = listTokens or []

        self.phraseCount = {}
        self.phraseFrequency=[]
# PG: try to be consistent with the use of whitespace - I prefer spaces around operators in statements 
# like in the assingment to phraseCount

        countList = [0]*len(phraseList) # create and initialize an array with the given length of phraseList

        # Return a blank list if either phrase list or token list is blank
        if (len(phraseList) == 0 | len(tokenList) == 0):
            self.phraseCount = dict(zip(phraseList,countList))
            return([]) #(self.phraseCount)
# PG: you don't need the brackets around the if condition in Python. You can also make use of the fact that 
# empty lists are interpreted as False. The if statement can be written as:
#  if not phraseList or not tokenList:
# or 
#  if not (phraseList and tokenList):
# the second version is probably easier to read. Note also that I used the logical operators "and" and "or"
#
# the brackets in the return statement are not required. There is however a difference in the returned type 
# here (list) from the end of the function (dictionary self.phraseCount) - be consistent

        phrasePosition = 0
        for tempPhrase in phraseList:
# PG: The variable phrasePosition is used as a counter of for loop index. The pythonic way of 
# doing this is:
#   for phrasePosition, tempPhrase in enumerate(phraseList):

            phrase_Tokens = nltk.word_tokenize(tempPhrase)

            tPosition = 0
            while tPosition < len(tokenList)-len(phrase_Tokens)+1:
# PG: isn't this identical to 
# for tPosition in range(len(tokenList) - len(phrase_Tokens) + 1): 
# 
                compPhrase = ""
                pCount = 0
                matchCount = 0
                while pCount < len(phrase_Tokens):
                    compPhrase = compPhrase + tokenList[tPosition + pCount]
                    if phrase_Tokens[pCount] == tokenList[tPosition+pCount]:
                        matchCount = matchCount + 1
                    pCount = pCount + 1
# PG: You an rewrite this also using the enumerate function
#   for pCount, phrase_Token in enumerate(phrase_Tokens):
# and remove the update to pCount
                if len(phrase_Tokens) == matchCount:
                    countList[phrasePosition] = countList[phrasePosition] + 1
                    self.phraseFrequency.append(tempPhrase)
                    #if len(phrase_Tokens) > 1:
                    #    print("*** MATCHED ***")
                    #    print("tempPhrase : " + tempPhrase)
                    #    print("compPhrase : " + compPhrase)
# PG: I'm not sure if I understand the idea of this code block. If you
# want to see if the list of tokens starting at tokenList[tPosition] is identical to the content of phrase_tokens, 
# then you could replace this maybe with the following statement:
# 
# if tokenList[tPosition: tPosition + len(phrase_Tokens] == phrase_Tokens:
#     countList[phrasePosition] += 1
#     self.phraseFrequency.append(tempPhrase)
# 
# This might not be the most efficient way of comparing the two lists. This might also work and could be faster
#
# if all(tok1 == tok2 for tok1, tok2 in zip(tokenList[tPosition:], phrase_Tokens)): 

                tPosition = tPosition + 1
            phrasePosition = phrasePosition + 1
# PG: Both updates to tPosition and phrasePosition are not required with the suggested changes.


        self.dictionaryHandler(phraseList, countList)
        return (self.phraseCount)
# brackets are not required in Python


# Plot a graph
def pltAGraph(dictData):
    plt.bar(retDict.keys(), retDict.values(), width=.5)
    plt.show()


if __name__ == '__main__':

    # Create an RDF object and read data from an RDF file available in the repository
    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')

    # Generate a Synonyms list from the RDF object
    synonymsList = rdf.synonymsList()

    # Read text from the source files for testing.
    filesList = ['tempdirectives.txt','tempinstructions.txt'] 
    filePath = r"/Users/abigailbernhardt/Desktop/UVA/Fall 2021/DS 6011 - Capstone/Data/"
#    filesList = ['data_list.txt'] 
#    filePath = r"/Users/abigailbernhardt/Desktop/UVA/Fall 2021/DS 6011 - Capstone/"
 
    
    for fileName in filesList:
        fileObject = open(filePath + fileName, 'r')

        # Read data from the source file
        data = fileObject.read()
        data.replace(r"\n", " ")

        # Create tokens
        nltk_tokens = nltk.word_tokenize(data)

        # Get the matchig phrase count
        phCount = phraseCounts()
        #retDict = phCount.getPhraseCount(synonymsList,nltk_tokens)
        retDict = phCount.getPhraseFrequencyCount(synonymsList,nltk_tokens)
        print(retDict)
        # Display a graph with matching phrase frequency
        pltAGraph(retDict)
        
        
        
        
        
        
        
        
        
