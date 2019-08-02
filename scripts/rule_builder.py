"""
Scrappy little function for generating a JSONL patterns file
from a terminology list for use in Prodigy and spaCy's EntityRuler()
"""


import spacy
from wasabi import Printer
import tqdm as tqdm
import plac
from pathlib import Path

msg = Printer()


@plac.annotations(
    model=("Model name", "positional", None, Path),
    TERMINOLOGY=("Terminlogy file with data", "positional", None, Path),
    output_file=("Output JSONL file", "positional", None, Path),
    label=("Label to add to rules", "positional", None, str),
)
def main(model=None, TERMINOLOGY=None, output_file=None, label=None):
    """
    Create a JSONL patterns file from a terminology list for use in
    Prodigy and spaCy's EntityRuler. This function receives a spaCy model,
    the terminology list (a text file with a term per line), an output path
    and the label to assign to the rule.
    """
    nlp = spacy.load(model)
    RULES = []

    msg.info("Reading terminology list...")
    with open(TERMINOLOGY) as data_in:
        data = data_in.readlines()
    msg.good("Terminlogy list in loaded.")
    msg.info("Applying tokeniser...")

    for i in tqdm.tqdm(data):
        i = i.replace("\n", "")
        i = i.replace("\\", "")
        i = i.replace('"', "")

        doc = nlp(i)
        TOKENS = []
        for token in doc:
            TOKENS.append('{"ORTH": "%s"},' % (token.text))
            rule = '{"label": "%s", "pattern": %s' % (label, TOKENS)
            rule = str(rule).replace("'", "")
            rule = str(rule).replace(",]", "]")
            rule = rule + "}"
            rule = rule.replace(",,", ", ")
            # Get rid of the first determiner
            rule = rule.replace('{"ORTH": "The"},', "")

        RULES.append(rule)
        TOKENS = []

    msg.info("Writing rules to JSONL patterns file...")
    with open(output_file, "a+") as data_out:
        for i in tqdm.tqdm(RULES):
            print(i)
            data_out.write(i + "\n")
    msg.good("Done!")


if __name__ == "__main__":
    plac.call(main)
