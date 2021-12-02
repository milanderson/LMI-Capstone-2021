import re

class NGRAM():
    def __init__(self, phrase, lemma, pos, size):
        self.text = phrase
        self.lemma = lemma
        self.pos = pos
        self.size = size
        self.successors = set()
        self.predecessors = set()
        self.count = 0
        self._score = None

'''
    Description:
        Processes a sequence of formatted tokens and returns a list of significant ngrams
    Arguments:
        REQUIRED
            @max_n          the max size of an ngram
        OPTIONAL
            @stop_chars     a string of characters that act as delimiters for ngrams
            @stop_words     a list of strings that act as delimiters for ngrams
            @score_func     scoring function of format: score(ngram, num_tokens)
            @ignore_rare    number of occurances an ngram must have to be considered (default 1)
'''
class NGramGenerator():
    REM_CHARS = ',:;.?!-'
    ENCL_CHARS = '"()[]}{'
    STOP_WORDS = ['but', 'because']
    CHAR_MAP = {'"': '"', '{': '}', '}': '{', '(': ')', ')': '(', ']': '[', '[': ']'}
    OPEN_CHARS = '"{[('

    def __init__(self, max_n, stop_chars='', stop_words=[], score_func=None, ignore_rare=1):
        # map of strings: {occurance counts
        self.ngram_map = {}
        self.token_que = []
        self._n = 0
        self.max_n = max_n

        self.REM_CHARS = stop_chars + NGramGenerator.REM_CHARS
        self.STOP_CHARS = [char for char in self.REM_CHARS + self.ENCL_CHARS]
        self.STOP_WORDS = stop_words + NGramGenerator.STOP_WORDS
        self.ENCL_CHARS = NGramGenerator.ENCL_CHARS
        self._enclosing = [None]

        self.score_func = score_func
        self.ignore_rare = ignore_rare

    def glueScore(self, token):
        if token._score:
            return token._score
        if token.count <= self.ignore_rare:
            token._score = 0
            return 0

        pTok = token.count / self._n
        if token.size == 1:
            token._score = pTok
            return pTok
        
        subProb = 0
        '''
        def getSubProbs(tok):
            nParts = tok.text.split(" ")
            subProb = tok.count / self._n
            for i in range(1, tok.size):
                subProb += getSubProbs(self.ngram_map[" ".join(nParts[:i])])*getSubProbs(self.ngram_map[" ".join(nParts[i:])])
            return subProb
        subProb = getSubProbs(token)
        subProb = (1 / (token.size + 1))*subProb
        '''
        # non-exhaustive sub-probability from "N-Gram_Feature_Selection_for_Authorship_Identification" http://www.icsd.aegean.gr/lecturers/stamatatos/papers/AIMSA2006.pdf
        nParts = token.lemma.split(" ")
        for i in range(1, token.size):
            prefTok = self.ngram_map[" ".join(nParts[:i])]
            suffTok = self.ngram_map[" ".join(nParts[i:])]
            subProb += (prefTok.count / self._n)*(suffTok.count / self._n)

        score = pTok**2 / subProb
        if self.score_func:
            score += self.score_func(token, self._n)
        token._score = score
        return score

    def processNextN(self, token):
        def enclFound(tok):
            for char in tok:
                if char in self.ENCL_CHARS:
                    return char
            return None

        def stopFound(tok):
            return any(char in tok[0] + tok[-1] for char in self.STOP_CHARS) or tok in self.STOP_WORDS

        def isMalformed(tok):
            return any(char in tok.text[1:-1] for char in '.*$%^~@#!?|()[]<>}{\=+') or len([x for x in re.finditer(r'[^a-zA-Z]', tok.text)]) / len(tok.text) >= 1/3

        def queFull():
            return len(self.token_que) > self.max_n

        def processQue(que, curTok=None, inc=1):
            if not que:
                return

            raw_text = " ".join(t.text for t in que)
            ngram_key = " ".join(t.lemma_ for t in que)
            pos_pattern = " ".join(t.tag_ for t in que)
            if ngram_key not in self.ngram_map:
                self.ngram_map[ngram_key] = NGRAM(raw_text, ngram_key, pos_pattern, len(que))
            nextTok = self.ngram_map[ngram_key]
            nextTok.count += inc
            
            if curTok:
                nextTok.successors.add(curTok)
                curTok.predecessors.add(nextTok)
            
            processQue(que[:-1], nextTok, inc)
            processQue(que[1:], nextTok, max(0, inc - 1))

        # format next token and add to que
        formatted_text = token.text.translate(str.maketrans("", "", self.REM_CHARS)).strip().lower()
        encl_char = enclFound(formatted_text)
        if not formatted_text or isMalformed(token):
            return

        if formatted_text not in self.STOP_WORDS and (not encl_char or encl_char not in NGramGenerator.OPEN_CHARS):
            self.token_que.append(token)
            self._n += 1

        # clean up token que
        if stopFound(token.text):
            while self.token_que:
                processQue(self.token_que)
                self.token_que.pop(0)

        if queFull():
            processQue(self.token_que)
            self.token_que.pop(0)

        # handle statefulness (will have undefined behavior on inputs like: "I. put? punctuation. in. my. quotes!")
        if encl_char:
            if NGramGenerator.CHAR_MAP[encl_char] in self._enclosing:
                self._enclosing.remove(NGramGenerator.CHAR_MAP[encl_char])
            elif encl_char in NGramGenerator.OPEN_CHARS:
                self.token_que.append(token)
                self._n += 1
                self._enclosing.append(encl_char)
        if not self.token_que:
            self._enclosing = [None]

    def getNGrams(self):
        def isGTXGood(ngram):
            baseScore = self.glueScore(ngram)
            return all(baseScore >= self.glueScore(pred) for pred in ngram.predecessors) and (
                all(baseScore > self.glueScore(succ) for succ in ngram.successors))
               
        def isLTXGood(ngram):
            baseScore = self.glueScore(ngram)
            return all(baseScore > self.glueScore(succ) for succ in ngram.successors)

        # select most commonly co-occuring grams
        goodgrams = []
        useablegrams = [ngram for _, ngram in self.ngram_map.items() if ngram.size <= self.max_n]

        # track work completed
        steps = 20
        workToDo = len(useablegrams) / steps
        workDone = 0
        ticks = 0
        print("Scoring NGrams: >" + " "*steps + "|", end="\r")

        for ngram in useablegrams:

            # print work completed
            workDone += 1
            if workDone > workToDo:
                workDone = 0
                ticks += 1
                print("Scoring NGrams: " + "="*ticks + ">" + " "*(steps - ticks), end="\r")

            if (ngram.size > 1 and isGTXGood(ngram)) or (ngram.size < 2 and isLTXGood(ngram)):
                goodgrams.append(ngram)

        print("Scoring NGrams Complete" + " "*steps)
        return goodgrams

    def processText(self, text):

        def get_pos(txt):
            import spacy
            nlp = spacy.load("en_core_web_lg")

            CHUNK_SIZE = 1000000
            prevCut, curCut = 0, 0
            doc = []

            while curCut < len(txt):
                if curCut + CHUNK_SIZE > len(txt):
                    nextChunk = txt[curCut:]
                    curCut += CHUNK_SIZE
                else:
                    prevCut = curCut
                    curCut = max(txt.rfind(" ", 0, prevCut + CHUNK_SIZE), prevCut + CHUNK_SIZE/2)
                    nextChunk = txt[prevCut:curCut]
                doc += [t for t in nlp(nextChunk.lower())]
            return doc

        processedDoc = get_pos(text)

        # track work done
        steps = 50
        workToDo = len(processedDoc) / steps
        workDone = 0
        ticks = 0
        print("Generating NGrams: >" + " "*steps + "|", end="\r")

        for tok in processedDoc:
            self.processNextN(tok)
            workDone += 1

            # print work completed
            if workDone > workToDo:
                ticks += 1
                workDone = 0
                print("Generating NGrams: " + "="*ticks + ">" + " "*(steps - ticks) + "|", end="\r")

        print("Generating NGrams Complete" + " "*steps)

    def __call__(self, text):
        self.processText(text)
        return sorted(self.getNGrams(), key=lambda x : x._score, reverse=True)

def makePatternScorer(patterns="patterns.txt"):
    if type(patterns) == str:
        patterns = open(patterns, "r").readlines()
    def scorePattern(token, *args):
        score = 0
        print(token.text)
        print(token.pos)
        # penalize dangling prepositions
        if token.pos[-3:] == "ADP" or token.pos[:3] == "ADP":
            score -= 0.1
        # noun bonus
        if "NN" in token.text[-3:] or "NN" in token.text[:3]:
            score += 0.1
        if token.pos in patterns:
            score += 0.2
        return score

    return scorePattern

def printNGrams(text):
    ngen = NGramGenerator(5, score_func=makePatternScorer())
    for ngram in ngen(text):
        print(ngram.text)

if __name__ == "__main__":
    printNGrams("This is a test")
