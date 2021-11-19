'''
* Module  : Concepts
* Purpose : A wrapper to create concept objects with all phrases and matching counts
*           Reads the RDF file, create contacts and updates counts using the other modules functionality
* Created : Oct-27-2021 : Srinivas -
'''
from urllib.parse import unquote

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
            self.about = unquote(xmlConcept.attrs['rdf:about'].split("#")[-1])

            # Loop through the other phrases available and add to the concept object
            for item in xmlConcept.find_all('altLabel'):
                self.addAltLabel(item.text)

            # Loop through the other phrases available and add to the concept object
            for item in xmlConcept.find_all('prefLabel'):
                self.addPrefLabel(item.text)

            for item in xmlConcept.find_all('acronym'):
                self.addAcronym(item.text)

            self.synonyms = [item.text for item in xmlConcept.find_all('synonym')]

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
{acr}""".format(about=self.about, pref=self.prefLabels, alt=self.altLabels, acr=self.acronyms)