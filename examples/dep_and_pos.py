"""
Visualise the dependency tree using spaCy's displaCy visualiser
using Blackstone's custom dep palette.
"""

import spacy
from spacy import displacy
from blackstone.displacy_palette import dep_displacy_options


nlp = spacy.load("en_blackstone_proto")
text = """you must not injure your neighbour"""
doc = nlp(text)
displacy.render(doc, style="dep", options=dep_displacy_options)
