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

# Concept object class to store all phrase counts
class Concept():

    def __init__(self,aboutText=None):
        if aboutText == None:
            self.about = ""
        else:
            self.about = aboutText

        self.prefLables = {}
        self.altLabels = {}
        self.acronyms = {}
        self.synonyms = {}
        self.antonyms = {}
        self.broaders = {}
        self.narrowers = {}
        self.related = {}

    def addPrefLabel(self,labelText,labelCount):
        self.prefLables[labelText] = labelCount

    def addAltLabel(self,labelText,labelCount):
        self.altLabels[labelText] = labelCount

    def addAcronyms(self,labelText,labelCount):
        self.acronyms[labelText] = labelCount

    def addSynonyms(self,labelText,labelCount):
        self.synonyms[labelText] = labelCount

    def addAntonyms(self,labelText,labelCount):
        self.antonyms[labelText] = labelCount

    def addBroaders(self,labelText,labelCount):
        self.broaders[labelText] = labelCount

    def addNarrowers(self,labelText,labelCount):
        self.narrowers[labelText] = labelCount

    def addRalted(self,labelText,labelCount):
        self.related[labelText] = labelCount

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


        #print(con.prefLables)
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
