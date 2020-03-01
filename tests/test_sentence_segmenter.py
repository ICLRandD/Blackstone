import unittest
import spacy
from blackstone.pipeline.sentence_segmenter import SentenceSegmenter
from blackstone.rules.citation_rules import CITATION_PATTERNS


class TestSentenceSegmenter(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.nlp = spacy.load("en_blackstone_proto")
        self.sentence_segmenter = SentenceSegmenter(self.nlp.vocab, CITATION_PATTERNS)
        self.nlp.add_pipe(self.sentence_segmenter, before="parser")

    def test_citation(self):
        text = """See, most recently, R. (on the application of ClientEarth) v Secretary of State for the Environment, \
        Food and Rural Affairs (No.2) [2017] P.T.S.R. 203. That's a good place to start."""
        doc = self.nlp(text)
        assert self.sum_iterable(doc.sents) == 2

    def sum_iterable(self, i):
        return sum(1 for e in i)
