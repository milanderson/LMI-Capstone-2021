import spacy
from spacy.matcher import Matcher
import pandas as pd
from time import process_time

nlp = spacy.load("en_core_web_sm")


def merge_matches(doc, matches):
    """
    Function takes the document and matches in order to merge together the
    word patterns found in the documents.
    :param doc: spacy Doc object
    :param matches: matches found by the Matcher, tuples
    """
    # For-loop goes in reverse order to avoid incorrect indexing
    # That occurs if you start from the beginning
    for i in reversed(matches):
        # Each item in the matches list is a tuple with match_id, start index, and end index
        match_id, start, end = i
        with doc.retokenize() as retokenizer:
            retokenizer.merge(doc[start:end])


def create_patterns(word):
    """
    Creates a spacy recognized pattern to be passed to the Matcher function
    :param word: word/phrase that needs to be recombined after spacy tokenization
    :return: pattern
    """
    # split the word/phrase into its individual pieces
    word_list = word.split()
    # create a list of dictionaries containing each word
    pattern = [{"LOWER": i} for i in word_list]

    return pattern


def custom_tokenizer(text, glossary):
    matcher = Matcher(nlp.vocab)
    for i, word in enumerate(glossary):
        matcher.add(f"pattern_{i}", [create_patterns(word=word)])
    doc = nlp(text)
    matches = matcher(doc)
    merge_matches(doc, matches)

    return doc


def get_glossary_terms(file_name):
    raw_glossary = pd.read_csv(file_name, index_col=0)
    filtered_glossary = list(raw_glossary[raw_glossary["doc_present"] == True].loc[:, "Term"])

    return filtered_glossary


def get_acronym_terms(file_name):
    raw_acronyms = pd.read_csv(file_name, index_col=0)
    filtered_acronyms = list(raw_acronyms[raw_acronyms["doc_present"] == True].loc[:, "Phrase"])

    return filtered_acronyms

def get_isa_terms(file_name):
    raw_terms = pd.read_csv(file_name, index_col=0)
    hyponyms = list(raw_terms["hyponym"])
    hypernyms = list(raw_terms["hypernym"])

    all_terms = hyponyms + hypernyms

    return all_terms



if __name__ == "__main__":
    # test = "This sentence contains department of defense. It also contains under secretary of defense " \
    #        "and military installation words."
    #
    # test_glossary = ["department of defense", "under secretary of defense", "military installation"]
    #
    # doc = custom_tokenizer(test, test_glossary)
    #
    # print([t.text for t in doc])
    # print(list(doc.sents))
    # print(len(list(doc.sents)))

    allDocs = pd.read_csv("full_dataframe.csv")

    acronyms = get_acronym_terms("./embeddings/matching_acronym.csv")
    glossary = get_glossary_terms("./embeddings/matching_glossary.csv")
    isa_terms = get_isa_terms("hyponyms_less.csv")
    all_terms = acronyms + glossary + isa_terms

    # combined_glossary = create_glossary(glossary_file, acronyms_file)

    start_time = process_time()

    new_docs = [custom_tokenizer(doc.lower(), glossary=glossary) for doc in allDocs["cleaned_text"]]
    new_docs = [list(doc.sents) for doc in new_docs]
    allDocs["custom_tokenized_text"] = new_docs

    end_time = process_time()

    print("Total elapsed time (in seconds):", end_time-start_time)

    allDocs.to_csv("full_custom_tokenized_df.csv")



