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
import re

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
class phraseCounts:
    phraseCount = {}
    phraseFrequency = []

    def __int__(self):
        self.phraseCount = {}
        self.phraseFrequency=[]
    def getPhraseCount(self,listPhrases=[],listTokens=[]):
        phraseList = listPhrases
        tokenList = listTokens

        countList = [0]*len(phraseList)

        if (len(phraseList) == 0 | len(tokenList) == 0):
            self.phraseCount = dict(zip(phraseList,countList))
            return([]) #(self.phraseCount)

        phrasePosition = 0
        for tempPhrase in phraseList:
            phrase_Tokens = nltk.word_tokenize(tempPhrase)

            tPosition = 0
            while tPosition < len(tokenList)-len(phrase_Tokens):
                compPhrase = ""
                pCount = 0
                matchCount = 0
                while pCount < len(phrase_Tokens):
                    compPhrase = compPhrase, tokenList[tPosition + pCount]
                    if phrase_Tokens[pCount].strip() == tokenList[tPosition+pCount].strip():
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

        self.phraseCount = dict(zip(phraseList, countList))
        return (self.phraseFrequency) #(self.phraseCount)

def pltHistogram():
    x = ["one", "two", "three", "four", "five","one"]
    y = [3, 5, 9, 10, 10]

    dict1 = dict(zip(x, y))
    plt.hist(x) #, y)
    plt.show()
if __name__ == '__main__':
    #pltHistogram()

    
    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')

    synonymsList = rdf.synonymsList()
    fileObject = open(r'/Users/abigailbernhardt/Desktop/UVA/Fall 2021/DS 6011 - Capstone/data_list.txt', 'r') #AI08_2016.txt, A088P.TXT
    
    data = fileObject.read()
    data.replace(r"\n", " ")

    nltk_tokens =  nltk.word_tokenize(data)

    phCount = phraseCounts()
    retDict = phCount.getPhraseCount(synonymsList,nltk_tokens)
    #print(retDict)

    plt.hist(retDict)  # , y)
    plt.show()
    
    
    
    







