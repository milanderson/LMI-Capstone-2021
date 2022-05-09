import spacy
from spacy.matcher import PhraseMatcher
import pandas as pd
import pickle
from time import process_time

nlp = spacy.load("en_core_web_lg")

def custom_tokenize(text, matcher):
    """
    Function takes the document and matches in order to merge together the
    word patterns found in the documents.
    :param text: the text to tokenize
    :param matcher: a spacy matcher that has been initialized with custom rules
    """
    doc = nlp(text)
    with doc.retokenize() as retokenizer:
        #spacy will cache the merges and execute them when this block concludes.
        #See: https://spacy.io/api/doc#retokenize
        for _, start, end in deconflict(matcher(doc)):
            retokenizer.merge(doc[start:end])

    return doc

###################### Utility Methods ######################

def deconflict(matches):
    # assumes matches are sorted
    deconflicted = matches[:1]
    for match in matches[1:]:
        if overlaps(deconflicted[-1][1:], match[1:]):
            if inside(deconflicted[-1][1:], match[1:]):
                deconflicted[-1] = match
        else:
            deconflicted.append(match)
    return deconflicted

def inside(rangeA, rangeB):
    return rangeA[0] >= rangeB[0] and rangeA[1] <= rangeB[1]

def overlaps(rangeA, rangeB):
    return between(rangeA[0], *rangeB) or between(rangeA[1], *rangeB) or between(rangeB[0], *rangeA)

def between(a, b, c):
    return a >= b and a <= c

###################### Loading Methods ######################

def createMatcher(glossary):
    matcher = PhraseMatcher(nlp.vocab)
    for i, phrase in enumerate(glossary):
        matcher.add(f"pattern_{i}", [nlp(phrase)])
    return matcher
    
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
    matcher = createMatcher(glossary)

    # combined_glossary = create_glossary(glossary_file, acronyms_file)

    start_time = process_time()

    new_docs = [[tok.text for tok in custom_tokenize(text, matcher)] for text in allDocs["cleaned_text"]]
    #new_docs = [list(doc.sents) for doc in new_docs]
    #allDocs["custom_tokenized_text"] = new_docs

    end_time = process_time()

    print("Total elapsed time (in seconds):", end_time-start_time)

    pickle.dump(new_docs, open('./embeddings/new_docs.pkl', 'wb'))
    #allDocs.to_csv("full_custom_tokenized_df.csv")



