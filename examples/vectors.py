"""
Query Blackstone's vector to find synonyms of a given word (in this case, defamation). 
"""

import spacy

nlp = spacy.load("en_blackstone_proto")


def most_similar(word):
    queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
    by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
    return by_similarity[:15]


print([w.lower_ for w in most_similar(nlp.vocab[u"defamation"])])
