from typing import List, Any
from spacy.tokens import Doc, Token


def sentence_segmenter(doc):
    """Adds custom sentence boundaries to spaCy Doc. 
    @param doc: the spaCy document to be annotated with sentence boundaries
    """
    for i, token in enumerate(doc[:-2]):
        if token.text == "Sch" and doc[i+1].is_punct:
            doc[i+2].is_sent_start = False
        if str(doc[i]) == "]" and doc[i+1].is_digit:
            doc[i+2].is_sent_start = False
        if str(doc[i+1]) == ")":
            doc[i+2].is_sent_start = False
        if str(doc[i+1]) == "(":
            doc[i+2].is_sent_start = False
        if str(doc[i+1]) == "]":
            doc[i+2].is_sent_start = False
        if str(doc[i+1]) == "[":
            doc[i+2].is_sent_start = False
        if doc[i+1].is_digit:
            doc[i+2].is_sent_start = False
        if str(doc[i+1]) == ";":
            doc[i+2].is_sent_start = False
        if str(doc[i+1]) == ":":
            doc[i+2].is_sent_start = True
        if str(doc[i+1]) == "\n\n":
            doc[i+2].is_sent_start = True
        if str(doc[i+1]) == "\n":
            doc[i+2].is_sent_start = True
        if str(doc[i+1]) == "-":
            doc[i+2].is_sent_start = False
        if str(doc[i+2]) == "[":
            doc[i+2].is_sent_start = False
        if doc[i].is_digit and str(doc[i+1]) == "]":
            doc[i+1].is_sent_start = False
        if doc[i].is_digit:
            doc[i+1].is_sent_start = False
        if token.text == "?" and doc[i+1].is_quote:
            doc[i+1].is_sent_start = False
        if token.text == "ex":
            doc[i].is_sent_start = False
        if token.text == "ex" and str(doc[i+1]) == "parte":
            doc[i+2].is_sent_start = False
        if token.text == "\n" and str(doc[i+1]) == "\n":
            doc[i+2].is_sent_start = True
        if token.text == "cf" and str(doc[i+1]) == ".":
            doc[i+2].is_sent_start = False
        if token.text == "unreported" and str(doc[i+1]) == ":":
            doc[i+2].is_sent_start = False
        if token.text == "Hon" and str(doc[i+1]) == ".":
            doc[i+2].is_sent_start = False
        if token.text == "." and doc[i+1].is_quote:
            doc[i+1].is_sent_start = False
        if token.text == "?" and str(doc[i+1]) == "!":
            doc[i+1].is_sent_start = False
        if token.text == "!" and str(doc[i+1]) == "?":
            doc[i+1].is_sent_start = False
        if str(doc[i+2]) == "(":
            doc[i+2].is_sent_start = False
        if token.text == "reg" and doc[i+1].is_punct:
            doc[i+2].is_sent_start = False
        if token.text == "’s":
            doc[i].is_sent_start = False
        if doc[i].is_quote:
            doc[i+1].is_sent_start = False
        if token.text == ")" and doc[i+1].is_punct == False:
            doc[i+2].is_sent_start = False
        if token.text == "Eu" and doc[i+1].is_punct:
            doc[i+2].is_sent_start = False

    return doc
