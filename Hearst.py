#################################################################
#
#   Adapted from https://github.com/mmichelsonIF/hearst_patterns_python
#
#################################################################
import re
import spacy

class PatternMatcher(object):
    NOUN_PHRASE = re.compile('NP_\\w+')

    def __init__(self, extended = False):
        self.__adj_stopwords = ['able', 'available', 'brief', 'certain', 'different', 'due', 'enough', 'especially','few', 'fifth', 'former', 'his', 'howbeit', 'immediate', 'important', 'inc', 'its', 'last', 'latter', 'least', 'less', 'likely', 'little', 'many', 'ml', 'more', 'most', 'much', 'my', 'necessary', 'new', 'next', 'old', 'other', 'our', 'ours', 'own', 'particular', 'past', 'possible', 'present', 'proud', 'recent', 'same', 'several', 'significant', 'similar', 'such', 'sup', 'sure']

        # now define the Hearst patterns
        # format is <hearst-pattern>, <general-term>
        # so, what this means is that if you apply the first pattern, the firsr Noun Phrase (NP)
        # is the general one, and the rest are specific NPs
        self.__hearst_patterns = [
            tuple(re.compile(item) if item != pat[-1] else item for item in pat) for pat in [
                ('NP_\\w+\\s*$', ',? such as ','^(NP_\\w+ ?(, )?(and |or )?)+', 'first'),
                ('such NP_\\w+\\s*$', ',? as ', '^(NP_\\w+ ?(, )?(and |or )?)+', 'first'),
                ('(NP_\\w+,? )+\\s*$', ' (and |or )?other ', '^(NP_\\w+)+', 'last'),
                ('NP_\\w+\\s*$', ',? include ', '^(NP_\\w+ ?(, )?(and |or )?)+', 'first'),
                ('NP_\\w+\\s*$', ',? especially ', '^(NP_\\w+ ?(, )?(and |or )?)+', 'first')]
        ]

        if extended:
            #TODO(Mike): make extensions work
            self.__hearst_patterns.extend([
                ('((NP_\\w+ ?(, )?)+(and |or )?any other NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?some other NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?be a NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )?like (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('such (NP_\\w+ (, )?as (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?like other NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?one of the NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?one of these NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?one of those NP_\\w+)', 'last'),
                ('example of (NP_\\w+ (, )?be (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?be example of NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )?for example (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?wich be call NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?which be name NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )?mainly (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?mostly (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?notably (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?particularly (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?principally (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?in particular (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?except (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?other than (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?e.g. (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?i.e. (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?a kind of NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?kind of NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?form of NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?which look like NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?which sound like NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )?which be similar to (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?example of this be (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?type (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )? NP_\\w+ type)', 'last'),
                ('(NP_\\w+ (, )?whether (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(compare (NP_\\w+ ?(, )?)+(and |or )?with NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )?compare to (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?among -PRON- (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?as NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )? (NP_\\w+ ? (, )?(and |or )?)+ for instance)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?sort of NP_\\w+)', 'last')
            ])

        self.__spacy_nlp = spacy.load('en_core_web_lg')
        
    def chunk(self, rawtext):
        doc = self.__spacy_nlp(rawtext)
        chunks = []
        for sentence in doc.sents:
            sentence_text = sentence.lemma_
            for chunk in sentence.noun_chunks:
                chunk_arr = []
                for token in chunk:
                    # Ignore Punctuation and stopword adjectives (generally quantifiers of plurals)
                    if token.is_punct or token.lemma_ in self.__adj_stopwords or token.is_space:
                        continue
                    chunk_arr.append(token.lemma_)
                if chunk_arr:
                    replacement_value = "NP_"+"_".join(chunk_arr)
                    sentence_text = sentence_text.replace(chunk.lemma_, replacement_value)
            chunks.append(sentence_text)
        return chunks

    """
        This is the main entry point for this code.
        It takes as input the rawtext to process and returns a list of tuples (specific-term, general-term)
        where each tuple represents a hypernym pair.

    """
    def find_hyponyms(self, rawtext):

        hyponyms = []
        np_tagged_sentences = self.chunk(rawtext)

        for sentence in np_tagged_sentences:
            # two or more NPs next to each other should be merged into a single NP, it's a chunk error

            for (l_pat, anchor, r_pat, parser) in self.__hearst_patterns:
                for match in anchor.finditer(sentence):
                    left_match = [m[0] for m in l_pat.finditer(sentence[:match.span()[0]])]
                    right_match = r_pat.search(sentence[match.span()[1]:])
                    
                    if left_match and right_match:
                        nps = self._getNP(left_match[-1]) + self._getNP(right_match[0])

                        if parser == "first":
                            general = nps[0]
                            specifics = nps[1:]
                        else:
                            general = nps[-1]
                            specifics = nps[:-1]

                        for i in range(len(specifics)):
                            #print("adding hyponyms\n\t%s\n\t%s" % (specifics[i], general))
                            hyponyms.append((self.clean_hyponym_term(specifics[i]), self.clean_hyponym_term(general)))

        return hyponyms

    def _getNP(self, text):
        return [np for m in PatternMatcher.NOUN_PHRASE.finditer(text) for np in m.group(0).split() if np.startswith("NP_")]

    def clean_hyponym_term(self, term):
        # good point to do the stemming or lemmatization
        return term.replace("NP_","").replace("_", " ")

