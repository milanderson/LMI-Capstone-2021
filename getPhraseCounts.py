'''
* Module  : getPhraseCount
* Purpose : Read a document and get the counts of matching of given phrases (multi-word)
*           Read the document and search for matching phrases (multi-word)
*           Get Phrase Coutns,
'''

import tokenize
import nltk

def test():
    phraseList = ["Apple", "Pear", "Peach", "Banana"]
    countList = [0, 0, 0, 0]

    phraseDictionary = dict(zip(phraseList, countList))

    return(phraseDictionary)

def getPhraseCount():
    #fileObject = open(r'C:\Users\srini\UVA-MSDS\DS-6011-CAP\Files\AI08_2016.txt', 'r')
    fileObject = open(r'C:\Users\srini\UVA-MSDS\DS-6011-CAP\Files\A088P.TXT', 'r')

    data = fileObject.read()
    data.replace(r"\n"," ")
    #print(data)
    nltk_tokens = nltk.word_tokenize(data)
    '''
    print(type(nltk_tokens))
    for i in range(0,len(nltk_tokens),1):
        print("Token # {0} Word : {1}".format(i,nltk_tokens[i]))
    '''
    tempPhrase = "National Capital Region"
    print(len(tempPhrase))

    phrase_Tokens = nltk.word_tokenize(tempPhrase)

    for i in range(0,len(phrase_Tokens),1):
        print("Token # {0} Word : {1}".format(i,phrase_Tokens[i]))

    print(len(phrase_Tokens))

    tPosition = 0
    while tPosition < len(nltk_tokens):
        compPhrase = ""
        pCount = 0
        matched = False
        while pCount < len(phrase_Tokens):
            compPhrase = compPhrase + nltk_tokens[tPosition + pCount]
            if phrase_Tokens[pCount] == nltk_tokens[tPosition+pCount]:
                matched = True
            else:
                matched = False
            pCount = pCount + 1

        if matched == True:
            print("*** MATCHED ***")
            print("compPhrase : " + compPhrase)
        tPosition = tPosition + 1
        '''
        compPhrase = compPhrase + nltk_tokens[tPosition+pCount]
        if (tempPhrase.strip() == compPhrase.strip()):
            print("*** MATCHED *** : " + tempPhrase + " == " + compPhrase)
        print("tempPhrase : " + tempPhrase)
        print("compPhrase : " + compPhrase)
        '''

    #print(nltk_tokens.size())
    # with open(r'C:\Users\srini\UVA-MSDS\DS-6011-CAP\Files\AI08_2016.txt', 'rb') as f:
    #     #tokens = tokenize.tokenize(f.readline)
    #     #for token in tokens:
    #
    #     #    print("token : " + token. + token.string)
    #     #print(f.readline)
    #     #nltk_tokens = nltk.word_tokenize(f.readline)
    #     #print(nltk_tokens.count())
    #     data = f.read() #.replace(r"\\n", "")
    #     nltk_tokens = nltk.word_tokenize(data)
    #     print(nltk_tokens )

if __name__ == '__main__':
    phCount = test()
    print(phCount)

    getPhraseCount()