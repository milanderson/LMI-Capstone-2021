'''
###########################################################################################################################
* Module  : RDFsComparison.py
* Purpose : A Set of methods to compare two RDF Documents. Generally, the original one with a final RDF document generated
*           It accepts to RDF documents and comparison method.
* Created : Apr-06-2022
* Changes :
###########################################################################################################################
'''

from urllib.parse import unquote
from math import*            # Import Match functions
#from Concept import Concept  # Import Concetp Classes
import time
from datetime import datetime
from bs4 import BeautifulSoup

# Concept object class to store all phrase counts
class Concept():

    def __init__(self, xmlConcept=None):
        # Initialize variables to track various phrase counts
        self.about = ""
        self.prefLabels = {}
        self.altLabels = {}
        self.acronyms = {}
        self.synonyms = {}
        self._allItems = {}

        if xmlConcept != None:
            # rdf:about an attribute to identify a concept object
            # self.about = unquote(xmlConcept.attrs['rdf:about'].split("#")[-1])
            self.about = ""  # unquote(xmlConcept.attrs['rdf:about'].split("#")[-1])

            # Loop through the other phrases available and add to the concept object
            for item in xmlConcept.find_all('altLabel'):
                self.addAltLabel(item.text)

            # Loop through the other phrases available and add to the concept object
            for item in xmlConcept.find_all('prefLabel'):
                self.addPrefLabel(item.text)

            for item in xmlConcept.find_all('acronym'):
                self.addAcronym(item.text)

            self.synonyms = [item.text for item in xmlConcept.find_all('synonym')]

    # add a new synonym phrase to the synonyms dictionary
    def addSynonym(self, key):
        if key not in self.synonyms:
            self.synonyms[key] = 0
            self._allItems[key] = self.synonyms

    # add a new preLabel phrase to the prefLabels dictionary
    def addPrefLabel(self, key):
        if key not in self.prefLabels:
            self.prefLabels[key] = 0
            self._allItems[key] = self.prefLabels

    # add a new altLabel phrase to the altLabels dictionary
    def addAltLabel(self, key):
        if key not in self.altLabels:
            self.altLabels[key] = 0
            self._allItems[key] = self.altLabels

    # add a new acronym phrase to the acronym dictionary
    def addAcronym(self, key):
        if key not in self.acronyms:
            self.acronyms[key] = 0
            self._allItems[key] = self.acronyms

    # Comparison method
    def __eq__(self, other):
        if (isinstance(other, Concept)):
            return self.about == other.about
        return False

    def __getitem__(self, key):
        if key in self._allItems:
            return self._allItems[key][key]
        return None

    def __setitem__(self, key, item):
        if key in self._allItems:
            self._allItems[key][key] = item

    def __iter__(self):
        self._n = 0
        self._keys = [k for k in self._allItems.keys()]
        return self

    def __next__(self):
        if self._n + 1 < len(self._keys):
            self._n += 1
            return self._keys[self._n]
        else:
            raise StopIteration

    def __str__(self):
        return """{about}
===================
    prefLabels
{pref}
    altLabels
{alt}
    acronyms
{acr}
    synonyms
{syn}

""".format(about=self.about, pref=self.prefLabels, alt=self.altLabels, acr=self.acronyms, syn=self.synonyms)

########################################################################################################
## Method : Jaccard_Similarity
## Purpose : Compare elements of given lists and returns a Jaccard Similarity Score
## Parameters : First List (x), Second List (y)
## Return Values : Jaccard similarity score of the given concepts parameters
## source :  https://ashukumar27.medium.com/similarity-functions-in-python-aa6dfe721035
########################################################################################################

def jaccard_similarity(x,y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))

    if union_cardinality > 0:
        return intersection_cardinality/float(union_cardinality)
    else:
        return 0


########################################################################################################
## Method : Set Difference
## Purpose : Find the difference of sets based onthe Difference Direction (X-Y or Y-X)
## Parameters : First List (x), Second List (y), Difference Direction (X-Y or Y-X)
## Return Values : Find the difference and calculated the matching percentage based on the source set length
########################################################################################################

def set_difference(x, y, diffDirection="xMinusY"):
    X1 = set(x)
    Y1 = set(y)

    retVal = 0
    if (diffDirection == "xMinusY"):
        if len(X1) > 0:
            retVal = ((len(X1) - len(X1.difference(Y1))) / len(X1))
    else:
        if len(Y1) > 0:
            retVal = ((len(Y1) - len(Y1.difference(X1))) / len(Y1))
    return (retVal)


########################################################################################################
## Method : Set Difference
## Purpose : Find the difference of sets based onthe Difference Direction (X-Y or Y-X)
## Parameters : First List (x), Second List (y), Difference Direction (X-Y or Y-X)
## Return Values : Find the difference and calculated the matching percentage based on the source set length
########################################################################################################

def set_difference(x, y, diffDirection="xMinusY"):
    X1 = set(x)
    Y1 = set(y)

    retVal = 0
    if (diffDirection == "xMinusY"):
        if len(X1) > 0:
            retVal = ((len(X1) - len(X1.difference(Y1))) / len(X1))
    else:
        if len(Y1) > 0:
            retVal = ((len(Y1) - len(Y1.difference(X1))) / len(Y1))
    return (retVal)


########################################################################################################
## Method : CompareRDFS
## Purpose : Compare specified elements of given two RDF Files
## Parameters : originalRDFFile -> RDFIle to compared with (Source)
##              finalRDFFile -> RDFFile to be compared (Destination)
## Return Values : Total Score
##                 Total Count
##                 Average Score
########################################################################################################

def compareRDFS(originalRDFFile, finalRDFFile, compareParameter="synonyms", calcType="jaccard"):
    # Read Source RDF and load concepts
    with open(originalRDFFile, 'r') as f:
        originalRDFString = f.read()

    originalXMLString = BeautifulSoup(originalRDFString, "xml")

    # Read Final RDF and laod concepts
    with open(finalRDFFile, 'r') as f:
        finalRDFString = f.read()

    finalXMLString = BeautifulSoup(finalRDFString, "xml")

    totalScore = 0
    totalCount = 0
    for orgConc in originalXMLString.find_all('Concept'):
        originalConcept = Concept(orgConc)

        if compareParameter == "synonyms":
            if len(originalConcept.synonyms) <= 0:
                continue
        elif compareParameter == "altLabels":
            if len(originalConcept.altLabels) <= 0:
                continue
        elif compareParameter == "prefLabels":
            if len(originalConcept.prefLabels) <= 0:
                continue
        elif compareParameter == "acronyms":
            if len(originalConcept.acronyms) <= 0:
                continue
        else:
            if len(originalConcept.synonyms) <= 0:
                continue

        totalCount += 1
        maxScore = 0

        for finConc in finalXMLString.find_all('Concept'):
            finalConcept = Concept(finConc)

            similarityScore = compareConcepts(originalConcept, finalConcept, compareParameter, calcType)
            # similarityScore = compareConcepts(originalConcept,finalConcept,compareParameter,"jaccard")
            maxScore = max(maxScore, similarityScore)
            if similarityScore > 0:
                print("Original Concept")
                print(originalConcept)
                print("Final Concept")
                print(finalConcept)
                print("Score:")
                print(similarityScore)
            # print(maxScore)

        totalScore += maxScore

        # if maxScore > 0:
        #    print("Maximum Score : {0}".format(maxScore))
        # if maxScore > 0:
        #    print(maxScore)
        #    print(originalConcept)
    return totalScore, totalCount, totalScore / totalCount


########################################################################################################
## Method : CompareConcepts
## Purpose : Compare specified elements of given two concepts classes and returns a Jaccard Similarity Score
## Parameters : originalConcept -> Concept to compared with (Source)
##              finalConcept -> Concept to be compared (Destination)
##              parameterType -> Type of parameter to compare. Default value is "synonyms"
## Return Values : Jaccard similarity score of the given concepts parameters
########################################################################################################

def compareConcepts(originalConcept, finalConcept, parameterType="synonyms", calcType="jaccard"):
    if parameterType == "synonyms":
        finalList = finalConcept.synonyms
        originalList = originalConcept.synonyms
    elif parameterType == "altLabels":
        finalList = finalConcept.altLabels
        originalList = originalConcept.altLabels
    elif parameterType == "prefLabels":
        finalList = finalConcept.prefLabels
        originalList = originalConcept.prefLabels
    elif parameterType == "acronyms":
        finalList = finalConcept.acronyms
        originalList = originalConcept.acronyms
    else:
        finalList = finalConcept.synonyms
        originalList = originalConcept.synonyms

    retVal = 0.0
    if calcType == "jaccard":
        retVal = jaccard_similarity(originalList, finalList)
    else:
        retVal = set_difference(originalList, finalList, calcType)
    return (retVal)
    # return jaccard_similarity(originalList,finalList)


####################################
## RUnning time calculation utility
####################################
# Usage :
# runTime = timeLog("Test")
# runTime.beginProcess()
# runTime.endProcess()

class timeLog():
    def __init__(self, procname=""):
        self.beginTime = time.time()
        self.endTime = time.time()
        self.procName = procname

    def beginProcess(self):
        self.beginTime = time.time()
        print(datetime.now().strftime("%D %H:%M:%S"), " : Begin Process...", self.procName)

    def endProcess(self):
        self.endTime = time.time()
        print(datetime.now().strftime("%D %H:%M:%S"), " : End Process...", self.procName)
        print(f"Total runtime for {self.procName} : {self.endTime - self.beginTime} seconds")

