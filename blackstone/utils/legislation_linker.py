"""
Detects relationships between provisions and instruments identified by 
Blackstone's NER model. 

Example usage:

nlp = spacy.load("model")

TEXTS = [
    "Section 1 of the Theft Act 1968 sets out the definition of theft."
]
for text in TEXTS:
    doc = nlp(text) 
    relations = extract_legislation_relations(doc)
    for provision, provision_url, instrument, instrument_url in relations:
        print(f"\n{provision}\t{provision_url}\t{instrument}\t{instrument_url}")

"""
from typing import List, Tuple
import re
import requests
import time


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


def hasNumbers(inputString: str) -> bool:
    """
    Check if the provision candidate contains a digit.
    """
    return any(char.isdigit() for char in inputString)


def extract_legislation_relations(doc) -> List[Tuple]:
    """
    Extract relationships between provisions and instruments identified
    by Blackstone's NER with the assistance of the dependency parser. 

    This function receives a spaCy doc and returns a list of tuples, each 
    tuple containing the following elements:

    (provision, provision_URL, instrument, instrument_URL)
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
                if hasNumbers(subject):
                    # Get the URL for the instrument on legislation.gov.uk
                    target = set_legislation_target(instrument)
                    # Get the URL for the provision
                    if target:
                        provision = set_provision_target(target, subject)

                else:
                    provision = "None"
            relations.append((subject, provision, instrument, target))
        elif instrument.dep_ == "pobj" and instrument.head.dep_ == "prep":
            target = set_legislation_target(instrument)
            if target:
                if hasNumbers(str(instrument.head.head)):
                    provision = set_provision_target(target, instrument.head.head)
                    head = instrument.head.head
                else:
                    provision = "None"
                    head = "None"
            relations.append((head, provision, instrument, target))
    return relations


def set_legislation_target(instrument: str) -> str:
    """
    Returns the legislation.gov.uk for the identified instrument, 
    e.g. http://www.legislation.gov.uk/ukpga/1999/17/contents. 
    """
    if "Act" not in instrument.text:
        target_url = "None"
    elif "Act" in instrument.text:
        url = f"http://www.legislation.gov.uk/id?title={instrument.text}"
        page = requests.get(url)
        if page.status_code == 200:
            # allow time for the URL to resolve to the stable target
            time.sleep(0.1)
            target_url = page.url
        else:
            target_url = "None"

    url_targert = target_url

    return url_targert


def set_provision_target(url: str, subject: str) -> str:
    """
    Returns the legislation.gov.uk URL for the identified provision, 
    e.g. http://www.legislation.gov.uk/ukpga/1998/42/section/20.
    """
    url = url.replace("contents", "section/")
    provision_number = re.findall(r"\d+", str(subject))
    matches = [match for match in provision_number]
    if matches:
        url = url + str(matches[0])
    else:
        url = "None"
    return url
