import pandas as pd
import regex as re
import numpy as np
import os
import webbrowser
from bs4 import BeautifulSoup
import requests
from collections import defaultdict

class DocExtract():
    '''
    Class to read in DoD documents and eliminate line breaks, eliminate footer/headers,
    pick out glossary terms, pick out acronyms, and produce the section splits
    '''
    def __init__(self, text=None):
        if text: #Test clean_text method by initializing the class with text
            self.raw_text = text
            self.cleaned_text = self.clean_text(self.raw_text)
        self.root_path = 'https://mikeanders.org/data/Ontologies/DoD/Corpus/processed/'
        self.doc_types = ['admin%20instructions', 'directives', 'instructions', 'manuals', 'memos']
        self.headers = ['Name', 'Last modified', 'Size', 'Description']
        self.docs_dict = { "doc_type":[],
                            "file_name":[],
                             "raw_text":[],
                             "cleaned_text":[],
                             "url":[],
                             "acronyms": []}

    def clean_text(self, text):
        '''
        function to take in the raw text and clean the text by:
            - remove new line markers
            - remove header/footers
        :return: Cleaned Text in string format
        '''
        #break down text to lines
        line_list = text.split('\r')

        #Separates lines of the document text by the return character (\r), creates pattern for the new line character (\n)
        pattern = re.compile('\s*\n\s*')
        repl = ''
        no_newLine = [re.sub(pattern, repl, i) for i in line_list]
        text_lines = [i for i in no_newLine if i != '']

        # Pulling the date from the first line of the document
        # Assumes the first line follows the format: Some Text, Date
        pattern = re.search("[a-zA-Z][\s][0-9]{1,2},[\s][0-9]{4}", text_lines[0])

        # A list to hold the indices in final_list that contain headers
        match_index = []
        for i in range(len(text_lines)):
            match = re.search(pattern.group(), text_lines[i])
            if match:
                match_index.append(i)
            else:
                continue

        # Create a list of dictionaries with the text as the key and the index as the value
        # Used to create a defaultdict
        headers_duplicates = []
        for i in match_index:
            headers_duplicates.append({'text': text_lines[i], 'index': i})

        # Create a dictionary with non-duplicate keys and a list of indices as the value
        headers = defaultdict(list)
        for item in headers_duplicates:
            headers[item['text']].append(item['index'])

        # Remove only those keys that have one entry
        # Only the repeated keys (more than one value) are headers
        # TODO: Might need to work on the case where there is only one page (one index value)
        remove_key = []
        for item in headers.items():
            k = item[0]
            v = item[1]

            if len(v) > 1:
                #print('This key has more than one index.')
                continue
            else:
                #print('This key has only 1 index. Therefore it is not a header. Adding to removal list.')
                remove_key.append(k)

        # Removes the non-header keys from the dictionary
        for k in remove_key:
            headers.pop(k)

        # Using the headers indices to find the footers
        # Footers follow the headers and should be one index away
        headers_key = list(headers)[0]

        footers = []
        for i in headers.get(headers_key):
            i += 1
            footers.append(i)

        # Turn the headers values back into a list of indices
        headers = headers[headers_key]

        # Combine headers and footers in one list, sort in descending order to remove those items from
        # the end of the document first (in order to keep index numbers from changing)
        remove_list = headers + footers + [0]
        remove_list.sort(reverse=True)

        for i in remove_list:
            text_lines.pop(i)

        return " ".join(text_lines)

    def parse_soup(self, soup, type, test):
        count = 0
        for link in soup.find_all('a', href=True):
            if link.text in self.headers:
                continue
            count += 1
            raw_text = requests.get(self.root_path + type + "/" + link['href']).text
            self.docs_dict['doc_type'].append(type)
            self.docs_dict['file_name'].append(link.text)
            self.docs_dict['raw_text'].append(raw_text)
            self.docs_dict['cleaned_text'].append(self.clean_text(raw_text))
            self.docs_dict['url'].append(self.root_path + type + "/" + link['href'])
            self.docs_dict['acronyms'].append(self.findAcronyms_Norm(self.clean_text(raw_text)))
            if test:
                if count == 1:
                    break

    def get_text(self, doc_type='all', test=False):
        if doc_type == 'all':
            for type in self.doc_types:
                source = requests.get(self.root_path + type).text
                soup = BeautifulSoup(source, 'lxml')
                self.parse_soup(soup, type, test)
        elif doc_type == 'admin':
            source = requests.get(self.root_path + self.doc_types[0]).text
            soup = BeautifulSoup(source, 'lxml')
            self.parse_soup(soup, 'admin%20instructions', test)
        elif doc_type == 'directives':
            source = requests.get(self.root_path + self.doc_types[1]).text
            soup = BeautifulSoup(source, 'lxml')
            self.parse_soup(soup, 'directives', test)
        elif doc_type == 'instructions':
            source = requests.get(self.root_path + self.doc_types[2]).text
            soup = BeautifulSoup(source, 'lxml')
            self.parse_soup(soup, 'instructions', test)
        elif doc_type == 'manuals':
            source = requests.get(self.root_path + self.doc_types[3]).text
            soup = BeautifulSoup(source, 'lxml')
            self.parse_soup(soup, 'manuals', test)
        elif doc_type == 'memos':
            source = requests.get(self.root_path + self.doc_types[4]).text
            soup = BeautifulSoup(source, 'lxml')
            self.parse_soup(soup, 'memos', test)
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
        #TODO (Mike): score based on shortest contiguous
        def getLongest(lst):
            if not lst:
                return []
            length = max(len(x) for x in lst)
            return [x for x in lst if len(x) == length][0]

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
        SEARCH_RANGE = 8
        # Assumes acronyms are defined in the form: (ToS) Terms of Service
        for result in [r for r in re.finditer(r'[(]([a-z]+)?[A-Z]+([a-zA-Z]+)?[)]', text, re.M|re.A)]:
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
        return acronym_table


if __name__ == "__main__":

    #test the class
    testDoc = DocExtract()
    testDoc.get_text(doc_type = 'instructions', test=True)

    #Save the one doc to dataframe
    testDoc.df.to_csv("testing_dataframe.csv")

    #Open up the original and then cleaned text
    testDoc.test_one_doc()
