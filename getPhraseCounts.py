'''
* Module  : getPhraseCount
* Purpose : Read a document and get the counts of matching of given phrases (multi-word)
*           Read the document and search for matching phrases (multi-word)
*           Get Phrase Coutns,
'''

import tokenize
import nltk
from rdfHandler import rdfObject

def test():
    phraseList = ["Apple", "Pear", "Peach", "Banana"]
    countList = [0, 0, 0, 0]

    phraseDictionary = dict(zip(phraseList, countList))

    return(phraseDictionary)

def getPhraseCount(phraseList=[],tokenList=[]):
    countList = [0]*len(phraseList)

    if (len(phraseList) == 0 | len(tokenList) == 0):
        return(dict(zip(phraseList)))

    print("*** BEGIN SOURCE PHRASES ***")
    for tempPhrase in phraseList:
        print("Source Phrase : " + tempPhrase)
    print("*** END SOURCE PHRASES ***")

    phrasePosition = 0
    for tempPhrase in phraseList:
        print("Source Phrase : " + tempPhrase)

        phrase_Tokens = nltk.word_tokenize(tempPhrase)

        print(phrase_Tokens)
        for i in range(0,len(phrase_Tokens),1):
            print("Token # {0} Word : {1}".format(i,phrase_Tokens[i]))


        tPosition = 0
        while tPosition < len(tokenList)-len(phrase_Tokens):
            compPhrase = ""
            pCount = 0
            matched = False
            while pCount < len(phrase_Tokens):
                compPhrase = compPhrase + tokenList[tPosition + pCount]
                if phrase_Tokens[pCount] == tokenList[tPosition+pCount]:
                    matched = True
                else:
                    matched = False
                pCount = pCount + 1
            #print("compPhrase : " + compPhrase)

            #if matched == True:
            if compPhrase == tempPhrase:
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

    retDict = getPhraseCount(synonymsList,nltk_tokens)
    print(retDict)

    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')
    print(rdf.synonymsList())
