'''
###########################################################################################################################
* Module  : RDFGenerator.py
* Purpose : A Set of methods to generate a final RDF file
*           It accepts Concept objects as input, tracks the concepts added and creates a final RDF file with all concepts
*           added.
* Created : Apr-06-2022
* Changes :
###########################################################################################################################
'''

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element, SubElement, QName, tostring
from io import BytesIO
from Concept import Concept  # Import Concetp Classes

###########################################################################################################################
# Class : RDFConcept
# Purpose : Basic RDF Concept class for generating a final RDF Document
###########################################################################################################################

class RDFConcept():
    # Default Constructor
    def __init__(self):
        # Initialize concept variables
        self.about = {}
        self.prefLabels = {}
        self.altLabels = {}
        self.acronyms = {}
        self.synonyms = {}
        self.related = {}
        self.narrower = {}
        self.broader = {}
        self._allItems = {}

    def addAbout(self, key):
        if key not in self.about:
            self.about[key] = 0
            self._allItems[key] = self.about

    # add a new preLabel phrase to the prefLabels dictionary
    def addPrefLabel(self, key):
        if key not in self.prefLabels:
            self.prefLabels[key] = 0
            self._allItems[key] = self.prefLabels

    # add a new AltLabel phrase to the altLebels dictionary
    def addAltLabel(self, key):
        if key not in self.altLabels:
            self.altLabels[key] = 0
            self._allItems[key] = self.altLabels

    # add a new acronym phrase to the acronyms dictionary
    def addAcronym(self, key):
        if key not in self.acronyms:
            self.acronyms[key] = 0
            self._allItems[key] = self.acronyms

    # add a new Synonym phrase to the synonyms dictionary
    def addSynonym(self, key):
        if key not in self.synonyms:
            self.synonyms[key] = 0
            self._allItems[key] = self.synonyms

    # add a new Related phrase to the related dictionary
    def addRelated(self, key):
        if key not in self.related:
            self.related[key] = 0
            self._allItems[key] = self.related

    # add a new Narrower phrase to the narrower dictionary
    def addNarrower(self, key):
        if key not in self.narrower:
            self.narrower[key] = 0
            self._allItems[key] = self.narrower

    # add a new Broader phrase to the broader dictionary
    def addBroader(self, key):
        if key not in self.broader:
            self.broader[key] = 0
            self._allItems[key] = self.broader

    def __str__(self):
        return """==> CONCEPT :
<skos:Concept rdf>{about}>
===================
<skos:prefLabel>{pref}>
<skos:altLabel>{alt}>
<skos:acronym>{acr}>
<skos:synonym>{syn}>
<skos:related>{rel}>
<skos:broader>{brd}>
<skos:narrower>{nar}>

""".format(about=self.about, pref=self.prefLabels,
           alt=self.altLabels, acr=self.acronyms,
           syn=self.synonyms, rel=self.related,
           brd=self.broader, nar=self.narrower)


###########################################################################################################################
# Class : RDFDocGenerator
# Purpose : Collects and track the Concept objects. Later, the objects will be used to create an RDF document
###########################################################################################################################

class RDFDocGenerator():
    def __init__(self):
        self.rdfCollection = []

    def addRDFConcept(self, pRDFConcept):
        self.rdfCollection.append(pRDFConcept)

    def size(self):
        return (len(self.rdfCollection))

    def __str__(self):
        for con in self.rdfCollection:
            print(con)
    # Generate RDF Document
    def generateRDF(self,
                    rdfFileName):
        with open("tempRDF.xml", 'wb') as f:
            tree = concepts2RDF(self.rdfCollection, "rdf:RDF")
            tree.write(f)

        with open("tempRDF.xml", "r") as infile, open(rdfFileName, "w") as outfile:
            data = infile.read()
            data = data.replace("<rdf:RDF>",
                                "<rdf:RDF xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:skos='http://www.w3.org/2004/02/skos/core#'>")
            data = data.replace("<skos:Concept>", "<skos:Concept rdf:about='http://my.site.com/#%28I%26S%29'>")

            outfile.write(data)



###########################################################################################################################
# Method : concepts2RDF
# Purpose : Reads the Concept class objects stored and create an XML document using the concepts collection data
# Parameters : RDF Generator Object and root elements to start the XML document tag
###########################################################################################################################

def concepts2RDF(obj, root_ele):
    root = Element(root_ele)
    tree = ElementTree(root)
    for itm in obj:
        sub1 = SubElement(root, "skos:Concept")
        # sub1.text = itm.about
        # sub = SubElement(sub1, "skos:prefLabel")
        # sub.text = str(key)
        itmCount = 0
        for key, value in itm.about.items():
            sub = SubElement(sub1, "skos:about")
            sub.text = str(key)

        for key, value in itm.prefLabels.items():
            sub = SubElement(sub1, "skos:prefLabel")
            sub.text = str(key)

        for key, value in itm.altLabels.items():
            sub = SubElement(sub1, "skos:altLabel")
            sub.text = str(key)
        for key, value in itm.acronyms.items():
            sub = SubElement(sub1, "skos:acronym")
            sub.text = str(key)
        for key, value in itm.synonyms.items():
            sub = SubElement(sub1, "skos:synonym")
            sub.text = str(key)
        for key, value in itm.related.items():
            sub = SubElement(sub1, "skos:related")
            sub.text = str(key)
        for key, value in itm.narrower.items():
            sub = SubElement(sub1, "skos:narrower")
            sub.text = str(key)
        for key, value in itm.broader.items():
            sub = SubElement(sub1, "skos:broader")
            sub.text = str(key)
    return tree


###########################################################################################################################
# Method : createRDFClassObj
# Purpose : Creates a Concept class by taking all labels as lists. Accepts the first parameter (About) as a string and all
#           other label parameters as lists
# Parameters : About,Preferred Labels, Alternate Labels, Synonyms, Acronyms, Narrow List, Broad List and Related list
###########################################################################################################################

def createRDFClassObj(tAbout,
                      tprefLabelList,
                      taltLabelList,
                      tsynonymList,
                      tacronymList,
                      tnarrowList,
                      tbroadList,
                      trelatedList):
    retRDFConcept = RDFConcept()
    retRDFConcept.addAbout(tAbout)

    for item in tprefLabelList:
        retRDFConcept.addPrefLabel(item)

    for item in taltLabelList:
        retRDFConcept.addAltLabel(item)

    for item in tsynonymList:
        retRDFConcept.addSynonym(item)

    for item in tacronymList:
        retRDFConcept.addAcronym(item)

    for item in tnarrowList:
        retRDFConcept.addNarrower(item)

    for item in tbroadList:
        retRDFConcept.addBroader(item)

    for item in trelatedList:
        retRDFConcept.addRelated(item)

    return (retRDFConcept)

