import unittest
import spacy

from blackstone.pipeline.abbreviations import (
    AbbreviationDetector,
    find_abbreviation,
    contains,
    filter_matches
)


class TestAbbreviationDetector(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.nlp = spacy.load("en_blackstone_proto")
        self.detector = AbbreviationDetector(self.nlp)
        self.text = "The European Court of Human Rights (ECtHR) is \
            responsible for applying the European Convention of Human \
            Rights. The Proceeds of Crime Act 2002 has is nothing to the point."

    def test_containsQuotes(self):
        # Straight double quote
        QUOTES = ['"', "'", "‘", "’", "“", "”"]
        doc = self.nlp('abbreviation ("abbrn")')
        long = doc[0:1]
        short = doc[2:5]
        short_form = short.text
        _, long_form = find_abbreviation(long, short)
        assert contains(short_form, QUOTES) is True

        # Straight single quote
        doc = self.nlp("abbreviation ('abbrn')")
        long = doc[0:1]
        short = doc[2:5]
        short_form = short.text
        _, long_form = find_abbreviation(long, short)
        assert contains(short_form, QUOTES) is True

        # Opening and closing single quotes
        doc = self.nlp("abbreviation (‘abbrn’)")
        long = doc[0:1]
        short = doc[2:5]
        short_form = short.text
        _, long_form = find_abbreviation(long, short)
        assert contains(short_form, QUOTES) is True

        # Opening and closing double quotes
        doc = self.nlp("abbreviation (“abbrn”)")
        long = doc[0:1]
        short = doc[2:5]
        short_form = short.text
        _, long_form = find_abbreviation(long, short)
        assert contains(short_form, QUOTES) is True

        # No quotes
        doc = self.nlp("abbreviation (abbrn)")
        long = doc[0:1]
        short = doc[2:5]
        short_form = short.text
        _, long_form = find_abbreviation(long, short)
        assert contains(short_form, QUOTES) is False

    def test_find_abbreviation(self):
        # Basic case
        doc = self.nlp("abbreviation (abbrn)")
        long = doc[0:1]
        short = doc[2:3]
        _, long_form = find_abbreviation(long, short)
        assert long_form.text == "abbreviation"

        # Hypenation and numbers within abbreviation
        doc = self.nlp("abbreviation (ab-b9rn)")
        long = doc[0:1]
        short = doc[2:3]
        _, long_form = find_abbreviation(long, short)
        assert long_form.text == "abbreviation"

        # No match
        doc = self.nlp("abbreviation (aeb-b9rn)")
        long = doc[0:1]
        short = doc[2:3]
        _, long_form = find_abbreviation(long, short)
        assert long_form is None

        # First letter must match start of word.
        doc = self.nlp("aaaabbreviation (ab-b9rn)")
        long = doc[0:1]
        short = doc[2:3]
        _, long_form = find_abbreviation(long, short)
        assert long_form.text == "aaaabbreviation"

        # Matching is greedy for first letter (are is not included).
        doc = self.nlp("more words are considered aaaabbreviation (ab-b9rn)")
        long = doc[0:5]
        short = doc[6:7]
        _, long_form = find_abbreviation(long, short)
        assert long_form.text == "aaaabbreviation"

    def test_filter_matches(self):
        # Act and year separated with a space
        doc = self.nlp("Companies Act 2006 (CA 2006)")
        filtered = filter_matches([(1, 4, 6)], doc)
        long_form_candidate = filtered[0][0]
        short_form_candidate = filtered[0][1]
        assert long_form_candidate.text == "Companies Act 2006"
        assert short_form_candidate.text == "CA 2006"

        # Act and year separated with a space, with quote marks
        doc = self.nlp("Companies Act 2006 ('CA 2006')")
        filtered = filter_matches([(1, 4, 8)], doc)
        long_form_candidate = filtered[0][0]
        short_form_candidate = filtered[0][1]
        assert long_form_candidate.text == "Companies Act 2006"
        assert short_form_candidate.text == "CA 2006"

    def test_find(self):
        doc = self.nlp(self.text)
        long, shorts = self.detector.find(doc[1:6], doc)
        assert long.string == "European Court of Human Rights "
