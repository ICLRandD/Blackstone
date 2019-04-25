from spacy.matcher import Matcher
from spacy.lang.en import English

TEXTS = [
    "The name of the case is R v Horncastle [2009] AC 123",
    "The name of the case is R v Horncastle [2009] 1 AC 123",
    "The name of the case is R v Horncastle [2009] 1 Cr App R 109",
    "The name of the case was Boaty McBoatface [2009] EWCA Civ 123",
    "The name of the case was Boaty McBoatface [2009] 1 All ER 123",
    "The name of the case was Boaty McBoatface [2009] EWHC 123 (Admin) and we like hats.",
    "I shouldn't return any matched entities.",
]

nlp = English()
matcher = Matcher(nlp.vocab)

# Matches [2010] AC 123-style
pattern1 = [
    {"IS_PUNCT": True},
    {"LIKE_NUM": True},
    {"IS_PUNCT": True},
    {"IS_ALPHA": True},
    {"LIKE_NUM": True},
]

# Matches [2010] 1 AC 123-style
pattern2 = [
    {"IS_PUNCT": True},
    {"LIKE_NUM": True},
    {"IS_PUNCT": True},
    {"LIKE_NUM": True},
    {"IS_ALPHA": True},
    {"LIKE_NUM": True},
]

# Matches [2010] 1 All ER 123-style
pattern3 = [
    {"IS_PUNCT": True},
    {"LIKE_NUM": True},
    {"IS_PUNCT": True},
    {"LIKE_NUM": True},
    {"IS_ALPHA": True},
    {"IS_ALPHA": True},
    {"LIKE_NUM": True},
]

# Matches [2010] 1 Cr App R 123-style
pattern4 = [
    {"IS_PUNCT": True},
    {"LIKE_NUM": True},
    {"IS_PUNCT": True},
    {"LIKE_NUM": True},
    {"IS_ALPHA": True},
    {"IS_ALPHA": True},
    {"IS_ALPHA": True},
    {"LIKE_NUM": True},
]

# Matches [2010] EWCA Crim 123-style
pattern5 = [
    {"IS_PUNCT": True},
    {"LIKE_NUM": True},
    {"IS_PUNCT": True},
    {"IS_ALPHA": True},
    {"IS_ALPHA": True},
    {"LIKE_NUM": True},
]

# Matches [2010] EWHC 123 (Admin)-style
pattern6 = [
    {"IS_PUNCT": True},
    {"LIKE_NUM": True},
    {"IS_PUNCT": True},
    {"IS_ALPHA": True},
    {"LIKE_NUM": True},
    {"IS_PUNCT": True},
    {"IS_ALPHA": True},
    {"IS_PUNCT": True},
]

matcher.add(
    "CITATION", None, pattern1, pattern2, pattern3, pattern4, pattern5, pattern6
)

TRAINING_DATA = []

for doc in nlp.pipe(TEXTS):
    # Match on the doc and create a list of matched spans
    spans = [doc[start:end] for match_id, start, end in matcher(doc)]
    # Get (start character, end character, label) tuples of matches
    entities = [(span.start_char, span.end_char, "CITATION") for span in spans]
    # Format the matches as a (doc.text, entities) tuple
    training_example = (doc.text, {"entities": entities})
    TRAINING_DATA.append(training_example)

print(*TRAINING_DATA, sep="\n")
