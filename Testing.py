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

if __name__ == '__main__':
    #pltHistogram()
    headers = {
        'user_agent': 'Srinivas class project;ver 1.0;email = spc6ph@virginia.edu;language = Python 3.8.12; platform = windows 10'}

    reqString = requests.get('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', headers=headers)
    #print(reqString.text)
    xmlRDFString = bs4.BeautifulSoup(reqString.text, "xml")
    #print(xmlRDFString)
    print([f.string for f in xmlRDFString.find_all('prefLabel')])

    for pref in xmlRDFString.find_all('Concept'):

        print("*** CONCEPT *** : " + pref.attrs['rdf:about'])
        print("==================")
        print("prefLable : " + pref.find("prefLabel").text)

        # pref.find_all("synonym")[0].text
        print("Synonyms->")
        for item in pref.find_all('synonym'):
            print(item.text)
        print("Synonyms->")
        for item in pref.find_all('synonym'):
            print(item.text)
        print("Synonyms->")
        for item in pref.find_all('synonym'):
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
