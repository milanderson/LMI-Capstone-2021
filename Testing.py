import matplotlib.pyplot as plt
import requests
import bs4

def pltHistogram():
    x = ["one", "two", "three", "four", "five", "one"]
    y = [3, 5, 9, 10, 10]

    dict1 = dict(zip(x, y))
    #plt.hist(dict1) # x)  # , y)
    plt.bar(dict1.keys(), dict1.values(), width=.5, color='g')
    plt.show()

class Concept():
    prefLables = {}
    altLabels = {}
    acronyms = {}
    synonyms = {}
    antonyms = {}
    broaders = {}
    narrowers = {}
    related = {}
    about = ""
    def __init__(self,aboutText=None):
        if aboutText == None:
            about = ""
        else:
            about = aboutText
        prefLables = {}
        altLabels = {}
        acronyms = {}
        synonyms = {}
        antonyms = {}
        broaders = {}
        narrowers = {}
        related = {}

    def addPrefLabel(self,labelText,labelText):
        self.prefLables[labelText] = labelText

    def addAltLabel(self,labelText,labelText):
        self.altLabels[labelText] = labelText

    def addAcronyms(self,labelText,labelText):
        self.acronyms[labelText] = labelText

    def addSynonyms(self,labelText,labelText):
        self.synonyms[labelText] = labelText

    def addAntonyms(self,labelText,labelText):
        self.antonyms[labelText] = labelText

    def addBroaders(self,labelText,labelText):
        self.broaders[labelText] = labelText

    def addNarrowers(self,labelText,labelText):
        self.narrowers[labelText] = labelText

    def addRalted(self,labelText,labelText):
        self.related[labelText] = labelText




if __name__ == '__main__':
    #pltHistogram()
    headers = {
        'user_agent': 'Srinivas class project;ver 1.0;email = spc6ph@virginia.edu;language = Python 3.8.12; platform = windows 10'}

    reqString = requests.get('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', headers=headers)
    #print(reqString.text)
    xmlRDFString = bs4.BeautifulSoup(reqString.text, "xml")
    #print(xmlRDFString)
    print([f.string for f in xmlRDFString.find_all('prefLabel')])


    conceptList = []

    for pref in xmlRDFString.find_all('Concept'):

        print("*** CONCEPT *** : " + pref.attrs['rdf:about'])
        print("==================")
        print("prefLable : " + pref.find("prefLabel").text)
        #print("altLable : " + pref.find("altLabel").text)
        #print("acronym : " + pref.find("acronym").text)

        # pref.find_all("synonym")[0].text
        conceptObj = Concept()

        print("altLable->")
        for item in pref.find_all('altLable'):
            print(item.text)
        print("acronym->")
        for item in pref.find_all('acronym'):
            print(item.text)

        print("Synonyms->")
        for item in pref.find_all('synonym'):
            print(item.text)
        print("Broader->")
        for item in pref.find_all('broader'):
            print(item.text)
        print("Narrower->")
        for item in pref.find_all('narrower'):
            print(item.text)
        print("Antonyms->")
        for item in pref.find_all('antonyms'):
            print(item.text)
        print("Related->")
        for item in pref.find_all('related'):
            print(item.text)


'''
    synonymsList = xmlRDFString.find_all('synonym')
    narrowList = xmlRDFString.find_all('narrower')
    broaderList = xmlRDFString.find_all('borader')
    relatedList = xmlRDFString.find_all('related')
    conceptCount = 0
    for pref in xmlRDFString.find_all('prefLabel'):
        print("Concept")
        print(pref.text)
        print(pref.att)
        children = pref.findChildren("synonym", recursive=False)
        for child in children:
            print("Child")
            print(child)
        conceptCount = conceptCount + 1
'''
