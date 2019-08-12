"""
Extract entities using the `en_blackstone_proto model.
"""

import spacy

nlp = spacy.load("en_blackstone_proto")
text = """There was before us no dispute as to the relevant statutory scheme or the law as the judge had to apply it. There was no dispute but that the judge had to consider in particular the circumstances in which the evidence came to be made (see section 114(2)(d)), the reliability of the witness Wilson (section 114(2)(e)) and how reliable the making of the statement appears to be (section 114(2)(f)). There was no dispute between the parties that the judge was bound to apply section 114(2) in considering the propriety of reading the transcripts pursuant to section 116 (see R v Cole & Ors [2008] 1 Cr App R No 5, paragraph 6, 7 and 21). Quite apart from those specific provisions the ultimate consideration had to be and remains the fairness of allowing that course to be adopted as Pitchford LJ said in R v Ibrahim [2010] EWCA Crim 1176"""
doc = nlp(text)

for ent in doc.ents:
    print(f"{ent.text} is a {ent.label_}")
