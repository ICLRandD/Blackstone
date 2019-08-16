import spacy
from spacy.pipeline import EntityRuler
from spacy.matcher import Matcher
from spacy.tokens import Doc
from collections import Counter
from blackstone.rules.concept_rules import CONCEPT_PATTERNS


class Concepts:
    """
    A custom pipeline component for identifying legal "concepts"
    in the doc. 

    This process is rules-based as opposed to statistical. 

    The doc is processed as usual, the EntityRuler is applied to the
    end of the pipeline, the patterns to look for are added to
    the ruler, matches are identified in the doc and are labelled 
    as CONCEPT entities. 

    The concept pipe is added after the EntityRuler and the concepts
    in the doc are accessible via doc._.concepts as a Counter object.
    
    Usage:
    concepts_pipe = Concepts(nlp)
    nlp.add_pipe(concepts_pipe)

    """

    def __init__(self, nlp) -> None:
        Doc.set_extension("concepts", default={}, force=True)
        self.ruler = EntityRuler(nlp)
        self.ruler.add_patterns(CONCEPT_PATTERNS)
        pipes = nlp.pipe_names
        if "EntityRuler" not in pipes:
            nlp.add_pipe(self.ruler, last=True)

    def __call__(self, doc: Doc) -> Doc:
        CONCEPTS = [ent.text.lower() for ent in doc.ents if ent.label_ == "CONCEPT"]
        if CONCEPTS:
            # CONCEPTS = list(set(CONCEPTS))
            CONCEPTS.sort()
            # Exclude terms with fewer than 5 occurences
            doc._.concepts = Counter(CONCEPTS).most_common(5)
        else:
            doc._.concepts = "None"
        return doc
