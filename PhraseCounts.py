'''
* Module  : getPhraseCount
* Purpose : Read a document and get the counts of matching of given phrases (multi-word)
*           Read the document and search for matching phrases (multi-word)
*           Get Phrase Counts
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

# class to handle the phrase counts and related operations
class phraseCounts:

    phraseCount = {}
    def __int__(self):

        self.phraseCount = {}

    def getPhraseCount(self,listPhrases=[],listTokens=[]):
        phraseList = listPhrases
        tokenList = listTokens

        countList = [0]*len(phraseList)

        if (len(phraseList) == 0 | len(tokenList) == 0):
            self.phraseCount = dict(zip(phraseList,countList))
            return(self.phraseCount)

        phrasePosition = 0
        for tempPhrase in phraseList:
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
                if len(phrase_Tokens) == matchCount:
                    countList[phrasePosition] = countList[phrasePosition] + 1
                    #if len(phrase_Tokens) > 1:
                    #    print("*** MATCHED ***")
                    #    print("tempPhrase : " + tempPhrase)
                    #    print("compPhrase : " + compPhrase)

                tPosition = tPosition + 1
            phrasePosition = phrasePosition + 1

        self.phraseCount = dict(zip(phraseList, countList))
        return (self.phraseCount)


if __name__ == '__main__':
    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')

    print(type(rdf.synonymsList()))
    synonymsList = rdf.synonymsList()


    #    fileObject = open(r'C:\Users\srini\UVA-MSDS\DS-6011-CAP\Files\AI08_2016.txt', 'r')
    #   fileObject = open(r'C:\Users\srini\UVA-MSDS\DS-6011-CAP\Files\A088P.TXT', 'r')
    fileObject = open(r'C:\Users\srini\UVA-MSDS\DS-6011-CAP\Files\A50P.TXT', 'r')

    data = fileObject.read()
    data.replace(r"\n", " ")
    # print(data)
    nltk_tokens = nltk.word_tokenize(data)
    #synonymsList = ["National Capital Region","NCR","item entry control"]

    phCount = phraseCounts()
    retDict = phCount.getPhraseCount(synonymsList,nltk_tokens)
    print(retDict)

    #rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')
    #print(rdf.synonymsList())

    #df = pd.DataFrame.from_dict(retDict)
    #print(df)

