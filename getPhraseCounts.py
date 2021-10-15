'''
* Module  : getPhraseCount
* Purpose : Read a document and get the counts of matching of given phrases (multi-word)
*           Read the document and search for matching phrases (multi-word)
*           Get Phrase Coutns,
'''

import tokenize
import nltk
from rdfHandler import rdfObject
import pandas as pd

def test():
    phraseList = ["Apple", "Pear", "Peach", "Banana"]
    countList = [0, 0, 0, 0]

    phraseDictionary = dict(zip(phraseList, countList))

    return(phraseDictionary)

def getPhraseCount(phraseList=[],tokenList=[]):
    countList = [0]*len(phraseList)

    if (len(phraseList) == 0 | len(tokenList) == 0):
        return(dict(zip(phraseList)))

    phrasePosition = 0
    for tempPhrase in phraseList:
        #print("Phrase Position :: " + str(phrasePosition) + " - Phrase :: " + tempPhrase)

        phrase_Tokens = nltk.word_tokenize(tempPhrase)

        tPosition = 0
        while tPosition < len(tokenList)-len(phrase_Tokens):
            compPhrase = ""
            pCount = 0
            matchCount = 0
            while pCount < len(phrase_Tokens):
                compPhrase = compPhrase + tokenList[tPosition + pCount]
                if phrase_Tokens[pCount].strip() == tokenList[tPosition+pCount].strip():
                    matchCount = matchCount + 1
                pCount = pCount + 1
            if len(phrase_Tokens) == matchCount: #matched == True:
                if len(phrase_Tokens) > 1:
                    print("*** MATCHED ***")

                    print("tempPhrase : " + tempPhrase)
                    print("compPhrase : " + compPhrase)
                countList[phrasePosition] = countList[phrasePosition] + 1

            tPosition = tPosition + 1
        phrasePosition = phrasePosition + 1
    return (dict(zip(phraseList, countList)))

if __name__ == '__main__':
    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')

    print(type(rdf.synonymsList()))
    synonymsList = rdf.synonymsList()
    #phCount = test()
    #print(phCount)

#    fileObject = open(r'C:\Users\srini\UVA-MSDS\DS-6011-CAP\Files\AI08_2016.txt', 'r')
    fileObject = open(r'C:\Users\srini\UVA-MSDS\DS-6011-CAP\Files\A088P.TXT', 'r')

    data = fileObject.read()
    data.replace(r"\n", " ")
    # print(data)
    nltk_tokens = nltk.word_tokenize(data)
    #synonymsList = ["National Capital Region","NCR","item entry control"]
    retDict = getPhraseCount(synonymsList,nltk_tokens)
    print(retDict)

    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')
    print(rdf.synonymsList())

    #df = pd.DataFrame.from_dict(retDict)
    #print(df)

