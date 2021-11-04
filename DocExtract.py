import pandas as pd
import re
import os
import webbrowser
from bs4 import BeautifulSoup
import requests
import json
from collections import defaultdict
import string
import spacy
nlp = spacy.load('en_core_web_lg')
table = str.maketrans(dict.fromkeys(string.punctuation))

class DocExtract():
    '''
    Class to read in DoD documents and eliminate line breaks, eliminate footer/headers,
    pick out glossary terms, pick out acronyms, and produce the section splits
    '''
    def __init__(self, text=None):
        if text: #Test clean_text method by initializing the class with text
            self.raw_text = text
            self.cleaned_text = self.clean_text(self.raw_text)
            self.cleaned_text_list = None
        self.root_path = 'https://mikeanders.org/data/Ontologies/DoD/Corpus/processed/'
        self.doc_types = ['admin%20instructions', 'directives', 'instructions', 'manuals', 'memos']
        self.headers = ['Name', 'Last modified', 'Size', 'Description']
        self.docs_dict = { "doc_type":[],
                            "file_name":[],
                             "raw_text":[],
                             "cleaned_text":[],
                             "cleaned_text_list":[],
                             "url":[],
                             "acronyms": [],
                             "glossary": []}

    def clean_text(self, text):
        '''
        function to take in the raw text and clean the text by:
            - remove new line markers
            - remove header/footers
        :return: Cleaned Text in string format
        '''
        #break down text to lines
        line_list = text.split('\r\n')

        # Pulling the date from the first line of the document
        # TODO: Modify header matching to add a couple different cases instead of assuming one header
        #       style for all documents
        # Assumes the first line follows the format: Some Text, Date
        pattern = ".*[0-9]{1,2},[\s][0-9]{4}"

        # Create a dictionary with non-duplicate keys and a list of indices as the value
        headers = defaultdict(list)
        for i, s in enumerate(line_list):
            if re.search(pattern, s):
                headers[s].append(i)

        final_text_lines = [l for l in line_list if len(headers[l]) < 2]

        self.cleaned_text_lines = final_text_lines
        return "\r\n".join(final_text_lines), final_text_lines

# This is returned the original data and also misses the assignment to self.cleaned_text_list
# self.cleaned_text_list = text_lines
# return " ".join(text_lines), text_lines

    def parse_soup(self, soup, type, test, full_count):
        for link in soup.find_all('a', href=True):
            type_count = 0
            if link.text in self.headers:
                continue
            full_count += 1
            type_count += 1
            raw_text = requests.get(self.root_path + type + "/" + link['href']).text
            cleaned_text, cleaned_text_list = self.clean_text(raw_text)
            self.docs_dict['doc_type'].append(type)
            self.docs_dict['file_name'].append(link.text)
            self.docs_dict['raw_text'].append(raw_text)
            self.docs_dict['cleaned_text'].append(cleaned_text)
            self.docs_dict['cleaned_text_list'].append(cleaned_text_list)
            self.docs_dict['url'].append(self.root_path + type + "/" + link['href'])
            self.docs_dict['acronyms'].append(self.findAcronyms_Norm(cleaned_text))
            self.docs_dict['glossary'].append(self.getGlossary(cleaned_text))
            print(f"Number of documents parsed: {full_count}")
            if test:
                if type_count > 0:
                    break

        return full_count

    def get_text(self, doc_type='all', test=False):
        count = 0
        if doc_type == 'all':
            for type in self.doc_types:
                source = requests.get(self.root_path + type).text
                soup = BeautifulSoup(source, 'lxml')
                count = self.parse_soup(soup, type, test, count)
        elif doc_type == 'admin':
            source = requests.get(self.root_path + self.doc_types[0]).text
            soup = BeautifulSoup(source, 'lxml')
            count = self.parse_soup(soup, 'admin%20instructions', test, count)
        elif doc_type == 'directives':
            source = requests.get(self.root_path + self.doc_types[1]).text
            soup = BeautifulSoup(source, 'lxml')
            count = self.parse_soup(soup, 'directives', test, count)
        elif doc_type == 'instructions':
            source = requests.get(self.root_path + self.doc_types[2]).text
            soup = BeautifulSoup(source, 'lxml')
            count = self.parse_soup(soup, 'instructions', test, count)
        elif doc_type == 'manuals':
            source = requests.get(self.root_path + self.doc_types[3]).text
            soup = BeautifulSoup(source, 'lxml')
            count = self.parse_soup(soup, 'manuals', test, count)
        elif doc_type == 'memos':
            source = requests.get(self.root_path + self.doc_types[4]).text
            soup = BeautifulSoup(source, 'lxml')
            count = self.parse_soup(soup, 'memos', test, count)
        else:
            print("Please provide document type (all, admin, directives, instructions, manuals, or memos)")
        self.df = pd.DataFrame(self.docs_dict)

    def test_one_doc(self):
        '''
        Opens up original text and then cleaned text in chrome
        '''
        for type in set(self.docs_dict['doc_type']):
            this_df = self.df[self.df['doc_type'] == type]

            #randomly select one
            sample = this_df.sample(1)

            #open the actual text file
            browser = webbrowser.get('chrome')
            browser.open(sample['url'].iloc[0])

            #open the cleaned version
            path = os.path.abspath('temp' + str(type) + '.txt')
            url2 = 'file://' + path
            with open(path, 'w') as f:
                f.write(sample['cleaned_text'].iloc[0])
            browser.open(url2)

    # parse a block of text for acronyms using exhaustive recursive search across preceding words
    def findAcronyms_Norm(self, text):
        def findMatch(fromStr, toStrList, matchList, isMatch=False):
            if not fromStr or not toStrList:
                rets = " ".join(matchList[::-1])
                return isMatch, rets

            if not toStrList[-1]:
                return findMatch(fromStr, toStrList[:-1], matchList, isMatch)

            if fromStr[-1].lower() not in 'qwertyuiopasdfghjklzxcvbnm':
                return findMatch(fromStr[:-1], toStrList, matchList, isMatch)

            if toStrList and fromStr[-1].lower() == toStrList[-1][0].lower():
                if matchList and toStrList[-1] != matchList[-1]:
                    newMatchList = [x for x in matchList] + toStrList[-1:]
                else:
                    newMatchList = toStrList[-1:]
                isMatch, rets = findMatch(fromStr[:-1], toStrList[:-1], newMatchList, True)
                if isMatch:
                    return isMatch, rets

            if toStrList and toStrList[-1].lower() in ["and", "of", "for", "to"]:
                newMatchList = [x for x in matchList] + toStrList[-1:]
                isMatch, rets = findMatch(fromStr, toStrList[:-1], newMatchList, True)
                if isMatch:
                    return isMatch, rets

            if matchList and fromStr[-1].lower() in matchList[-1][0].lower():
                isMatch, rets = findMatch(fromStr[:-1], toStrList, matchList, False)
                if isMatch:
                    return isMatch, rets

            if toStrList:
                isMatch, rets = findMatch(fromStr, toStrList[:-1], matchList, False)
            return False, ""

        acronym_table = {}
        SEARCH_RANGE = 9
        # Assumes acronyms are defined in the form: (ToS) Terms of Service
        for result in [r for r in re.finditer(r'[(]([a-z]+)?[A-Z]+([a-zA-Z]+)?[)]', text, re.M|re.A)]:
            stIdx, edIdx = result.span()
            index = stIdx - 1
            for _ in range(SEARCH_RANGE):
                index = max(text.rfind(" ", 0, index), 0)
            acronym, phrase = text[stIdx + 1:edIdx -1], text[index:stIdx - 1].replace('-', ' ').split(" ")
            # TODO(Mike): add mutliple acronyms
            if acronym not in acronym_table or type(acronym_table[acronym]) == list:
                found, match = findMatch(acronym, phrase, [])
                if found:
                    acronym_table[acronym] = match
        for result in [r for r in re.finditer(r'^[A-Z][a-zA-Z\(&\)]+', text, re.M|re.A)]:
            stIdx, edIdx = result.span()
            index = stIdx - 1
            for _ in range(SEARCH_RANGE):
                index = max(text.rfind(" ", 0, index), 0)
            acronym, phrase = text[stIdx + 1:edIdx -1], text[index:stIdx - 1].split(" ")
            # TODO(Mike): add mutliple acronyms
            if acronym not in acronym_table or type(acronym_table[acronym]) == list:
                found, match = findMatch(acronym, phrase, [])
                if found:
                    acronym_table[acronym] = match
        return json.dumps(acronym_table)

    def getGlossary(self, raw_text):
        glossary = {}
        if 'glossary' in raw_text.lower():
            #just get the second half of the document because that's where the glossary is, and we're going
            #to split on the first instance of 'glossary' and we don't want the table of contents glossary
            second_half = raw_text[len(raw_text)//2:]
            after_glossary = second_half.split("GLOSSARY", 1)[-1]
            sentences = after_glossary.split(". ")
            for i in range(len(sentences)):
                if sentences[i].isupper() and sentences[i].strip() not in ['ACRONYMS', 'DEFINITIONS'] and re.match('^[^.]*$', sentences[i]) and len(sentences[i-1]) > 5:
                    if len(sentences) > i + 1:
                        glossary[sentences[i].translate(table).strip()] = sentences[i+1]
                if sentences[i].islower() and len(sentences[i].strip(' ')) > 3 and len(sentences[i].split()) < 5:
                    if re.match('(?:[A-Z]\.){1,}(?:[A-Z])', sentences[i-1].split()[-1]):
                        if sentences[i-2].islower() and len(sentences[i-2].strip(' ')) > 3 and len(sentences[i-2].split()) < 5:
                            if len(sentences) > i + 1:
                                glossary[sentences[i].translate(table).strip()] = sentences[i + 1]
                        else:
                            continue
                    if True in [char.isdigit() for char in sentences[i].strip(' ')]:
                        continue
                    glossary[sentences[i].translate(table).strip()] = sentences[i + 1]
                i += 1
        return json.dumps(glossary)


if __name__ == "__main__":

    #test the class
    testDoc = DocExtract()
    testDoc.get_text(doc_type = 'all', test=False)

    print("\n")
    print("-----------------------------------------------------")
    print("All documents parsed")
    print("-----------------------------------------------------")

    #Save the one doc to dataframe
    testDoc.df.to_csv("full_dataframe.csv")

    #Open up the original and then cleaned text
    #testDoc.test_one_doc()
