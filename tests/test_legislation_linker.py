# flake8: noqa
import unittest
import spacy

from blackstone.utils.legislation_linker import (
    filter_spans,
    set_legislation_target,
    set_provision_target,
    extract_legislation_relations,
)


class TestLegislationLinker(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.nlp = spacy.load("en_blackstone_proto")
        self.text = "The Secretary of State was at pains to emphasise that, if a withdrawal agreement is made, it is very likely to be a treaty requiring ratification and as such would have to be submitted for review by Parliament, acting separately, under the negative resolution procedure set out in section 20 of the Constitutional Reform and Governance Act 2010. Theft is defined in section 1 of the Theft Act 1968"

    def test_filter_spans(self):
        # Entity recognition
        doc = self.nlp(self.text)
        NER_entities = list(doc.ents)
        instrument = doc[56:62]  # Constitutional Reform and Governance Act 2010
        assert instrument in NER_entities

        # Include instrument in filtered spans
        doc = self.nlp(self.text)
        noun_chunks = list(doc.noun_chunks)
        NER_entities = list(doc.ents)
        spans = NER_entities + noun_chunks
        filtered_spans = filter_spans(spans)
        assert doc[56:62] in filtered_spans

    def test_set_legislation_target(self):
        # Act look up
        doc = self.nlp("Constitutional Reform and Governance Act 2010")
        instrument = doc[:]
        target = "http://www.legislation.gov.uk/ukpga/2010/25/contents"
        assert set_legislation_target(instrument) == target

        # 'Act' not present
        doc = self.nlp("Constitutional Reform and Governance 2010")
        instrument = doc[:]
        assert set_legislation_target(instrument) == "None"

    def test_set_provision_target(self):
        # Provision look up
        doc = self.nlp("section 20")
        url = "http://www.legislation.gov.uk/ukpga/2010/25/contents"
        target = "http://www.legislation.gov.uk/ukpga/2010/25/section/20"
        assert set_provision_target(url, doc) == target

        # No number matches
        doc = self.nlp("section")
        url = "http://www.legislation.gov.uk/ukpga/2010/25/contents"
        target = "None"
        assert set_provision_target(url, doc) == target

    def test_extract_legislation_relations(self):
        # Instrument is the object of a preposition without a provision reference
        text = "The Secretary of State went on to describe the negative resolution procedure set out in the Constitutional Reform and Governance Act 2010."
        doc = self.nlp(text)
        relations = extract_legislation_relations(doc)
        assert str(relations[0][0]) == "None"
        assert relations[0][1] == "None"
        assert str(relations[0][2]) == "Constitutional Reform and Governance Act 2010"
        assert relations[0][3] == "http://www.legislation.gov.uk/ukpga/2010/25/contents"

        # Instrument is the object of a preposition and includes a provision reference
        text = "The Secretary of State went on to describe the negative resolution procedure set out in section 20 of the Constitutional Reform and Governance Act 2010."
        doc = self.nlp(text)
        relations = extract_legislation_relations(doc)
        assert str(relations[0][0]) == "section 20"
        assert (
            relations[0][1] == "http://www.legislation.gov.uk/ukpga/2010/25/section/20"
        )
        assert str(relations[0][2]) == "Constitutional Reform and Governance Act 2010"
        assert relations[0][3] == "http://www.legislation.gov.uk/ukpga/2010/25/contents"

        # Instrument is a direct object without a provision reference
        text = (
            "The procedure follows the Constitutional Reform and Governance Act 2010."
        )
        doc = self.nlp(text)
        relations = extract_legislation_relations(doc)
        assert str(relations[0][0]) == "None"
        assert relations[0][1] == "None"
        assert str(relations[0][2]) == "Constitutional Reform and Governance Act 2010"
        assert relations[0][3] == "http://www.legislation.gov.uk/ukpga/2010/25/contents"
