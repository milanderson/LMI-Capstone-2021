'''
class to store a word embeddings model and save the parameters to track versions
'''

from gensim.models import Word2Vec
from ast import literal_eval
import pandas as pd
from datetime import datetime
import dill
import csv
from nltk.tokenize import word_tokenize, sent_tokenize
import wikipedia
import time

class EmbeddingsObject():
    def __init__(self, version, description):
        self.date = datetime.now().strftime("%m/%d/%Y")
        self.version = version
        self.description = description
        self.corpus_description = []

    def build_corpus(self):
        # read in corpus
        df = pd.read_csv('../full_dataframe.csv', index_col=0)
        df['cleaned_text_list'] = df['cleaned_text_list'].apply(literal_eval)
        '''
        sentences must look like this for gensim Word2Vec training:
        sentences = [['Testing', 'if', 'this', 'works'],
                     ['Another', 'sentence', 'about', 'that', 'test'],
                     ['Here', 'is', 'yet', 'another', 'sentence', 'for', 'you']]
        '''
        # get all text as lists of tokenized sentences like example above
        all_sentences = []
        for doc in df['cleaned_text_list']:
            for sent in doc:
                all_sentences.append(word_tokenize(sent))

        #drop blank sentences
        clean_sentences = []
        for sent in all_sentences:
            if len(sent) == 0:
                pass
            else:
                clean_sentences.append(sent)

        with open("clean_sentences.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(clean_sentences)
        print("Corpus outputed to directory as clean_sentences.csv")

    def set_corpus(self):
        try:
            corpus = open("clean_sentences.csv", "r")
            csv_reader = csv.reader(corpus)
        except:
            print("Must have clean_sentences.csv in directory.")
            print("Use build_corpus method to produce this file")

        self.training_data = []
        for row in csv_reader:
            self.training_data.append(row)
        self.corpus_description.append('Main DoD Corpus')
        print("Set main corpus as training data for embeddings")

    def scrape_wiki(self, search_term, search_results_num=50):
        wiki_pages = wikipedia.search(search_term, search_results_num)
        all_content = []
        count = 0
        for page in wiki_pages:
            try:
                this_page = wikipedia.page(page)
                count += 1
            except:
                pass
            all_content.append(this_page.content)
        print("Scraped {} pages containing {} and added them to training set".format(count, search_term))
        for doc in all_content:
            sentences = sent_tokenize(doc)
            for sent in sentences:
                word_tokens = word_tokenize(sent)
                self.training_data.append(word_tokens)
        self.corpus_description.append('wiki_{}_{}'.format(search_term, str(search_results_num)))

    def train_embeddings(self, size = 100, window = 5, min_count = 1, workers = 3, training_type = 0):
        '''
            embeddings method takes
            -embedding dimensions (100 default)
            -window (5 default)
            -min_count (1 default)
            -workers (3 default)
            -training type (0 for CBOW, 1 for Skip-Gram)
        '''
        start_time = time.time()
        self.model = Word2Vec(self.training_data, min_count=min_count, size=size, workers=workers, window=window, sg=training_type)
        self.size = 100
        self.window = 5
        self.min_count = 1
        self.workers = 3
        if training_type == 0:
            self.training_type = 'CBOW'
        else:
            self.training_type = 'Skip-Gram'
        print("Finished Training Custom Embeddings in {} Minutes".format(round((time.time() - start_time)/60), 2))

    def has_numbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def find_synonyms(self, synonym_threshold,save_synonyms=False):
        start_time = time.time()
        self.synonym_threshold = synonym_threshold

        # get words from our corpus
        try:
            file = open("clean_sentences.csv", "r")
        except:
            print("Run build_corpus to produce clean_sentences.csv")
        csv_reader = csv.reader(file)
        sentences = []
        for row in csv_reader:
            sentences.append(row)
        all_words = []
        for doc in sentences:
            for word in doc:
                all_words.append(word)
        words = set(all_words)
        print("num of words: {}".format(len(words)))

        # run through all the words and find the synonyms given a particular threshold
        synonyms = []
        count = 0
        for word in words:
            try:
                similar_words = self.model.wv.most_similar(positive=[word], topn = 10, restrict_vocab=None)
                for w in similar_words:
                    if w[1] > self.synonym_threshold: # and w[0] in all_words
                        synonyms.append([word, w[0]])
            except:
                pass
            count += 1
            if count % 500 == 0:
                print("Through {} out of {} words".format(count, str(len(words))))
        # take out numbers
        clean_synonyms = []
        for pair in synonyms:
            if self.has_numbers(pair[0]) or self.has_numbers(pair[1]):
                pass
            elif len(pair[0]) == 1 or len(pair[1]) == 1:
                pass
            else:
                clean_synonyms.append(pair)
        sorted_syns = []
        for pair in clean_synonyms:
            new_list = sorted(pair, reverse=False)
            sorted_syns.append(new_list)
        final_synonyms = set(tuple(row) for row in sorted_syns)
        self.synonyms_df = pd.DataFrame(final_synonyms, columns = {"First Term", "Second Term"})
        self.num_of_synonyms = len(self.synonyms_df)
        print("Identified and stored {} unique synonym pairs.".format(len(self.synonyms_df)))

        if save_synonyms:
            self.save_synonyms()
        print("Finished Synonym Scraping in {} Minutes".format(round((time.time() - start_time)/60), 2))


    def save_synonyms(self):
        self.synonyms_df.to_csv("synonyms_{}.csv".format(self.date.replace("/", "_")))
        print("Saved synonyms as synonyms_{}.csv".format(self.date.replace("/", "_")))
