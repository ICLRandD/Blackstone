"""
Detects relationships between provisions and instruments identified by 
Blackstone's NER mode. 

Example usage:

nlp = spacy.load("model")

TEXTS = [
    "Section 1 of the Theft Act 1968 sets out the definition of theft."
]
for text in TEXTS:
    doc = nlp(text)
    relations = extract_legislation_relations(doc)
    for r1, r2 in relations:
        print("{:<10}\t{}\t{}".format(r1.text, r2.ent_type_, r2.text))

"""
from typing import List, Tuple

def filter_spans(spans) -> List[str]:
    """
    Filter out overlapping spans. Returns a list of strings.
    """
    get_sort_key = lambda span: (span.end - span.start, span.start)
    sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
    result = []
    seen_tokens = set()
    for span in sorted_spans:
        if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
            result.append(span)
            seen_tokens.update(range(span.start, span.end))
    return result


def extract_legislation_relations(doc) -> List[Tuple]:
    """
    Merge entities and noun chunks into one token. 
    Takes a spaCy doc object as input as returns a list of tuples.
    """
    spans = list(doc.ents) + list(doc.noun_chunks)
    spans = filter_spans(spans)
    with doc.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(span)

    relations = []
    for instrument in filter(lambda w: w.ent_type_ == "INSTRUMENT", doc):
        if instrument.dep_ in ("attr", "dobj"):
            subject = [w for w in instrument.head.lefts if w.dep_ == "nsubj"]
            if subject:
                subject = subject[0]
                relations.append((subject, instrument))
        elif instrument.dep_ == "pobj" and instrument.head.dep_ == "prep":
            relations.append((instrument.head.head, instrument))
    return relations
