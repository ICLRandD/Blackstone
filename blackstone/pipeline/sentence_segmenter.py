from spacy.matcher import Matcher


class SentenceSegmenter(object):
    """Adds custom sentence boundaries to spaCy Doc. 
    @param vocab: the language vocabulary from the spaCy nlp object
    @param boundary_protection_rules: an optional list of labelled matching patterns that will explicitly prevent sentence boundaries
    """

    name = "sentence_segmenter"

    def __init__(self, vocab, boundary_protection_rules=[]):
        self.matcher = Matcher(vocab)
        for rule in boundary_protection_rules:
            self.matcher.add(rule["label"], None, rule["pattern"])

    def __call__(self, doc):
        matches = self.matcher(doc)
        for i, token in enumerate(doc[:-2]):
            if token_in_match_range(token, matches):
                token.is_sent_start = False
            if token.text == "Sch" and doc[i + 1].is_punct:
                doc[i + 2].is_sent_start = False
            if str(doc[i]) == "]" and doc[i + 1].is_digit:
                doc[i + 2].is_sent_start = False
            if str(doc[i + 1]) == ")":
                doc[i + 2].is_sent_start = False
            if str(doc[i + 1]) == "(":
                doc[i + 2].is_sent_start = False
            if str(doc[i + 1]) == "]":
                doc[i + 2].is_sent_start = False
            if str(doc[i + 1]) == "[":
                doc[i + 2].is_sent_start = False
            if doc[i + 1].is_digit:
                doc[i + 2].is_sent_start = False
            if str(doc[i + 1]) == ";":
                doc[i + 2].is_sent_start = False
            if str(doc[i + 1]) == ":":
                doc[i + 2].is_sent_start = True
            if str(doc[i + 1]) == "\n\n":
                doc[i + 2].is_sent_start = True
            if str(doc[i + 1]) == "\n":
                doc[i + 2].is_sent_start = True
            if str(doc[i + 1]) == "-":
                doc[i + 2].is_sent_start = False
            if str(doc[i + 2]) == "[":
                doc[i + 2].is_sent_start = False
            if doc[i].is_digit and str(doc[i + 1]) == "]":
                doc[i + 1].is_sent_start = False
            if doc[i].is_digit:
                doc[i + 1].is_sent_start = False
            if token.text == "?" and doc[i + 1].is_quote:
                doc[i + 1].is_sent_start = False
            if token.text == "ex":
                doc[i].is_sent_start = False
            if token.text == "ex" and str(doc[i + 1]) == "parte":
                doc[i + 2].is_sent_start = False
            if token.text == "\n" and str(doc[i + 1]) == "\n":
                doc[i + 2].is_sent_start = True
            if token.text == "cf" and str(doc[i + 1]) == ".":
                doc[i + 2].is_sent_start = False
            if token.text == "unreported" and str(doc[i + 1]) == ":":
                doc[i + 2].is_sent_start = False
            if token.text == "Hon" and str(doc[i + 1]) == ".":
                doc[i + 2].is_sent_start = False
            if token.text == "." and doc[i + 1].is_quote:
                doc[i + 1].is_sent_start = False
            if token.text == "?" and str(doc[i + 1]) == "!":
                doc[i + 1].is_sent_start = False
            if token.text == "!" and str(doc[i + 1]) == "?":
                doc[i + 1].is_sent_start = False
            if str(doc[i + 2]) == "(":
                doc[i + 2].is_sent_start = False
            if token.text == "reg" and doc[i + 1].is_punct:
                doc[i + 2].is_sent_start = False
            if token.text == "’s":
                doc[i].is_sent_start = False
            if doc[i].is_quote:
                doc[i + 1].is_sent_start = False
            if token.text == ")" and doc[i + 1].is_punct == False:
                doc[i + 2].is_sent_start = False
            if token.text == "Eu" and doc[i + 1].is_punct:
                doc[i + 2].is_sent_start = False
        return doc


def token_in_match_range(token, matches):
    for _, start, end in matches:
        if token.i >= start and token.i <= end:
            return True
    return False
