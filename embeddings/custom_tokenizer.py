import spacy
from spacy.matcher import Matcher

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


if __name__ == "__main__":
    test = "This sentence contains department of defense. It also contains under secretary of defense " \
           "and military installation words."

    test_glossary = ["department of defense", "under secretary of defense", "military installation"]

    doc = custom_tokenizer(test, test_glossary)

    print([t.text for t in doc])


