from Concept import Concept
import requests
import bs4
import re
from datetime import datetime
import pandas as pd

# create Concept objects
# Open and reads the RDF document for all concept objects available and creates a list with ConceptObjects
# Also initializes the phrases in the Concept Objects (Synonyms, Acronyms, PrefLable and AltLabel)

# def CreateConcepts():
#     reqString = requests.get('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf')
#     xmlRDFString = bs4.BeautifulSoup(reqString.text, "xml")
#
#     # Search for all "concept" tags to create Concept objects list
#     return [Concept(xmlConcept) for xmlConcept in xmlRDFString.find_all('Concept')]

def CreateConcepts(rdfFile):
    reqString = requests.get(rdfFile)
    xmlRDFString = bs4.BeautifulSoup(reqString.text, "xml")

    # Search for all "concept" tags to create Concept objects list
    return [Concept(xmlConcept) for xmlConcept in xmlRDFString.find_all('Concept')]

# Update matching phrase in the Concept objects
def UpdateConcepts(concepts, text):
    for concept in concepts:
        for item in concept:
            concept[item] = len(re.findall(item, text))

# Print the Concept Objects List
def PrintConcepts(conceptObjList):
    print("UPDATED CONCEPTS LIST")
    for count, con in enumerate(conceptObjList):
        print("===================")
        print("CONCEPT # " + str(count))
        print(con)


def logEvents(logText):
    print(datetime.now().strftime("%H:%M:%S") + " - " + logText)

##########################
# Read the documents text data from the data frame
##########################
def ReadData():
    dataDF = pd.read_csv("full_dataframe.csv")
    return " ".join([text for text in dataDF['raw_text']])

if __name__ == '__main__':

    logEvents("1...")
    concepts = CreateConcepts('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf')
    #concepts = CreateConcepts(r'C:\\SourceRDF.rdf')

    for i in range(1,2,1):
        logEvents("Start the iteration..." + str(i))
        data = ReadData()

        logEvents("Reading the corpus")
        data.replace(r"\n", " ")

        logEvents("Tagging the corpus")
        # PG: If you directly access the fields in the concept object, I think this can be simplified even more:
        # Acronyms
        UpdateConcepts(concepts, data)

    # Print the Cocepts List
    PrintConcepts(concepts)
    logEvents("Printed Concept Objects...")

    i = 1
    for cnc in concepts:
        print("===> Concept " + str(i))
        for syn in cnc.synonyms:
            print("---> Synonyms")
            print(syn)
        print(cnc.about)
        i = i + 1


