from spacy.matcher import Matcher
from spacy.tokens import Doc


class CompoundCases:
    """
    Detects compound references to cases. Two styles of referencing are
    accommodated: common_pattern (e.g. Smith v Jones [2000] 1 WLR 123) and
    the slightly old fashioned possessive_pattern (e.g in Hoadley's case 
    [2018] 1 WLR 123).

    This class sets the `._.compound_cases` attribute on the spaCy doc.

    Note! This class merges all of the entities in the doc and replaces
    the spans.

    Usage:

    compound_pipe = CompoundCases(nlp)
    nlp.add_pipe(compound_pipe)

    for compound in doc._.compound_cases:
        ...
    """

    def __init__(self, nlp) -> None:
        Doc.set_extension("compound_cases", default=[], force=True)
        self.matcher = Matcher(nlp.vocab)
        common_pattern = [{"ent_type": "CASENAME"}, {"ent_type": "CITATION", "OP": "+"}]
        possessive_pattern = [
            {"ent_type": "CASENAME"},
            {"lower": "case"},
            {"ent_type": "CITATION"},
        ]
        self.matcher.add("compound_case", None, common_pattern, possessive_pattern)
        self.global_matcher = Matcher(nlp.vocab)
        merge_ents = nlp.create_pipe("merge_entities")
        nlp.add_pipe(merge_ents)

    def __call__(self, doc: Doc) -> Doc:

        compound_cases = self.matcher(doc)
        for match_id, start, end in compound_cases:
            span = doc[start:end]  # The matched span
            doc._.compound_cases.append(span.text)

        return doc
