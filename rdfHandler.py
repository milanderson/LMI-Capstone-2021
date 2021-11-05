'''
* Module  : rdfHandler
* Purpose : To handle functionality related to rdfFile processing.
*           Reading an RDF File from the internet source, replace HTML characters with ASCII,
*           Get Synonyms list etc.,
*           Added a method to get any custom phrase count along with other predefined methods to get
*           standard phrases like Synonyms list, Acronyms list etc.,
'''
#from bs4 import beautifulsoup
#import beautifulsoup4

import lxml as lxml
import numpy
import pandas as pd
import requests
import bs4


# RDF Class
class rdfObject:
# PG: in Python, classes usually start with a capital letter
    # Default constructor
    def __init__(self, rdfSource, type="web"):
        if (type == "web"):
            headers = {'user_agent': 'Srinivas class project;ver 1.0;email = spc6ph@virginia.edu;language = Python 3.8.12; platform = windows 10'}
            reqString = requests.get(rdfSource, headers=headers)
            self.originalRDFString = reqString.text
            self.findHTMLChars()
            self.replaceHTMLStrings()
            self.parseXMLStrings()
            self.charList = []
# PG: I usually avoid processing in the constructor. Here, the constructor downloads the data, handles special characters and parses the XML.
#     This is a lot of work being done. 
#
# The round brackets around the `if` condition is not required: `if type == "web":`

    # Look for all special character codes found in the document and make list for further processing
    def findHTMLChars(self):
        self.charList = []
        rdfLength = len(self.originalRDFString)

        stPos = 0
        while stPos < rdfLength:
            if (self.originalRDFString[stPos:stPos + 2] == "&#"):
                if (self.originalRDFString[stPos:stPos + 5] not in self.charList):
                    self.charList.append(self.originalRDFString[stPos:stPos + 5])
                stPos = stPos + 6
            stPos = stPos + 2
# PG: Because you increment stPos twice if &# matches, you will miss cases like: &#40;&#40;
#     I also think that you wouldn't identify abc&#40; 
#     In the first iteration, you look at ab, then stPos increments by 2, so we look next at c& 
#     which doesn't match. Next we look at #4...
# So it should be 
#         stPos = 0
#         while stPos < rdfLength:
#             if (self.originalRDFString[stPos:stPos + 2] == "&#"):
#                 if (self.originalRDFString[stPos:stPos + 5] not in self.charList):
#                     self.charList.append(self.originalRDFString[stPos:stPos + 5])
#                 stPos = stPos + 5
#             else:
#                 stPos = stPos + 1

# PG: You could use a set instead of a list for `self.charList`:
#
# self.charList = set()
# stPos = 0
# while stPos < rdfLength:
#     if (self.originalRDFString[stPos:stPos + 2] == "&#"):
#         self.charList.add(self.originalRDFString[stPos:stPos + 5]
#         stPos = stPos + 5
#     else:
#         stPos = stPos + 1 
#
# PG: a even shorter approach would be to use a regular expression:
# import re
# self.charList = set(re.findall('&#\d\d;', self.originalRDFString))
#
# example:
# >>> s = 'you will miss cases\n like: &#40;&#40;def &#32;'
# >>> set(re.findall('&#\d\d;', s))
# {'&#40;', '&#32;'}
# Looking at the following code, looks like we need to identify cases like &#123; as well,
#
# self.charList = set(re.findall('&#\d{2,3};', self.originalRDFString))
# >>> s = 'you will miss cases\n like: &#40;&#40;def &#321;'
# >>> set(re.findall('&#\d{2,3};', s))
# {'&#321;', '&#40;'}

    # replace special character codes with the actual ASCII chracters
    # example : &#40; with "(" , &#40; with ")"
    def replaceHTMLStrings(self):
        self.modifiedRDFString = self.originalRDFString

        # Loop through the list of strings found and replace in the RDFString
        for s in self.charList:
            # if the last character is ";", take only two digits for ASCII character (&#40;)
            # otherwise, take three digits and add an extra (;) to match in the string
            if (s[4:5] == ";"):
                self.modifiedRDFString = self.modifiedRDFString.replace(s.strip(), chr(int(s[2:4])))
            else:
                self.modifiedRDFString = self.modifiedRDFString.replace(s[2:5] + ';', chr(int(s[2:5])))
# PG: with the complete list above, we don't need the the if statement
#
# for s in charList:
#     s = s.strip()  # I cannot see why you need this
#     c = chr(int(s.lstrip('&#').rstrip(';'))
#     self.modifiedRDFString = self.modifiedRDFString.replace(s, c)

        # replacing ampersand code with & (special case. It is not following the ASCII codes pattern)
        self.modifiedRDFString = self.modifiedRDFString.replace("&amp;", "&")

    # Parse the modified RDF string as an XML parser and store in a separate string for further processing
    def parseXMLStrings(self):
        self.xmlRDFString = bs4.BeautifulSoup(self.modifiedRDFString, "xml")

    # Return all the matching words with synonym tag in the xml string
    def synonymsList(self):
        return ([f.string for f in self.xmlRDFString.find_all('synonym')])

    # Return all the matching words with acronym tag in the xml string
    def acronymsList(self):
        return ([f.string for f in self.xmlRDFString.find_all('acronym')])

    # Return all matching words with a given tag in the xml string
    def customTagList(self, tagToMatch):
        return ([f.string for f in self.xmlRDFString.find_all(tagToMatch)])
# PG: no need to have the round brackets for the return statement. 

    # Save the modifiled rdf file to another destination file
    def saveRDFFile(self, destFilename):
        f = open(destFilename, "w", encoding="UTF-8")
        f.write(self.modifiedRDFString)
        f.close()
# PG: I recommend using the following syntax for reading/writing files:
#
# with open(destFilename, "w", encoding="UTF-8") as f:
#     f.write(self.modifiedRDFString)
# 
# using the with-statement makes sure that the file is closed irrespective of what happens during the writing. 

if __name__ == '__main__':
    print('RDF file handling functionality...')
    rdf = rdfObject('https://mikeanders.org/data/Ontologies/DoD/DASD SKOS_Ontology.rdf', 'web')

    print("\n*** SYNONYMS LIST ***\n")
    print(rdf.synonymsList())
    print("\n*** SYNONYMS LIST WITH CUSTOM-TAG-LIST METHOD ***\n")
    print(rdf.customTagList("synonym"))
    print("\n*** ACRONYMS LIST ***\n")
    print(rdf.acronymsList())


    print("\n*** PREF-LABELS LIST ***\n")
    print(rdf.customTagList("prefLabel"))

    print("\n*** ALT-LABELS LIST ***\n")
    print(rdf.customTagList("altLabel"))

    print("\n*** BROADER LIST ***\n")
    print(rdf.customTagList("broader"))

    print("\n*** NARROWER LIST ***\n")
    print(rdf.customTagList("narrower"))

    print("\n*** RELATED LIST ***\n")
    print(rdf.customTagList("related"))
    # This code is to save the modified RDF file to a new file with changes. We are not using this functionality for now.
    #rdf.saveRDFFile("c:\\testing\\DASD_SKOS_Ontology_mod.rdf")

    print('Completed Successfully')
