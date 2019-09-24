<img src="https://iclr.s3-eu-west-1.amazonaws.com/assets/iclrand/sitecode.svg" width=20%>
<img src="https://iclr.s3-eu-west-1.amazonaws.com/assets/iclrand/blackstone_seal.svg" height=75%>

# Blackstone [![Built with spaCy](https://img.shields.io/badge/made%20with%20❤%20and-spaCy-09a3d5.svg)](https://spacy.io)
Blackstone is a [spaCy](https://spacy.io/) model and library for processing long-form, unstructured legal text. Blackstone is an experimental research project from the [Incorporated Council of Law Reporting for England and Wales'](https://iclr.co.uk/) research lab, [ICLR&D](https://research.iclr.co.uk/).

## Contents

[**Why are we building Blackstone?**](https://github.com/ICLRandD/Blackstone#why-are-we-building-blackstone)

[**What's special about Blackstone?**](https://github.com/ICLRandD/Blackstone#whats-special-about-blackstone)

[**Observations and other things worth noting**](https://github.com/ICLRandD/Blackstone#observations-and-other-things-worth-noting)

[**Installation**](https://github.com/ICLRandD/Blackstone#installation)

&nbsp;&nbsp;&nbsp;&nbsp;[Install the library](https://github.com/ICLRandD/Blackstone#1-install-the-library)

&nbsp;&nbsp;&nbsp;&nbsp;[Install the Blackstone model](https://github.com/ICLRandD/Blackstone#2-install-the-blackstone-model)

[**About the model**](https://github.com/ICLRandD/Blackstone#about-the-model)

&nbsp;&nbsp;&nbsp;&nbsp;[The pipeline](https://github.com/ICLRandD/Blackstone#the-pipeline)

&nbsp;&nbsp;&nbsp;&nbsp;[Named-Entity Recogniser](https://github.com/ICLRandD/Blackstone#named-entity-recogniser)

&nbsp;&nbsp;&nbsp;&nbsp;[Text categoriser](https://github.com/ICLRandD/Blackstone#text-categoriser)

[**Usage**](https://github.com/ICLRandD/Blackstone#usage)

&nbsp;&nbsp;&nbsp;&nbsp;[Applying the NER model](https://github.com/ICLRandD/Blackstone#applying-the-ner-model)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[Visualising entities](https://github.com/ICLRandD/Blackstone#visualising-entities)

&nbsp;&nbsp;&nbsp;&nbsp;[Applying the text categoriser model](https://github.com/ICLRandD/Blackstone#applying-the-text-categoriser-model)

[**Custom pipeline extensions**](https://github.com/ICLRandD/Blackstone#custom-pipeline-extensions)

&nbsp;&nbsp;&nbsp;&nbsp;[Abbreviation and long-form definition resolution](https://github.com/ICLRandD/Blackstone#abbreviation-detection-and-long-form-definition-resolution)

&nbsp;&nbsp;&nbsp;&nbsp;[Compound case reference detections](https://github.com/ICLRandD/Blackstone#compound-case-reference-detection)

&nbsp;&nbsp;&nbsp;&nbsp;[Legislation linker](https://github.com/ICLRandD/Blackstone#legislation-linker)

&nbsp;&nbsp;&nbsp;&nbsp;[Sentence segmenter](https://github.com/ICLRandD/Blackstone#sentence-segmenter)



## Why are we building Blackstone?

The past several years have seen a surge in activity at the intersection of law and technology. However, in the United Kingdom, the overwhelming bulk of that activity has taken place in law firms and other commercial contexts. The consequence of this is that notwithstanding the never ending flurry of development in the legal-informatics space, almost none of the research is made available on an open-source basis. 

Moreover, the majoritry of research in the UK legal-informatics domain (whether open or closed) has focussed on the development of NLP applications for automating contracts and other legal documents that are transactional in nature. This is understandable, because the principal benefactors of legal NLP research in the UK are law firms and law firms tend not to find it difficult to get their hands on transactional documentation that can be harnessed as training data. 

The problem, as we see it, is that legal NLP research in the UK has become over concentrated on commercial applications and that it is worthwhile making the investment in developing legal NLP research available with respect to other legal texts, such as judgments, scholarly articles, skeleton arguments and pleadings. 

## What's special about Blackstone?

* So far as we are aware, Blackstone is the first open source model trained for use on long-form texts containing common law entities and concepts.
* Blackstone is built on [spaCy](https://spacy.io/), which makes it easy to pick up and apply to your own data.
* Blackstone has been trained on data spanning a considerable temporal period (as early as texts drafted in the 1860s). This is useful because an interesting quirk of the common law is that older writings (particularly, judgments) go on to remain relevant for many, many years. 
* It is free and open source
* It is imperfect and makes no attempt to hide that fact from you

## Observations and other things worth noting:

* Perfection is the enemy of the good. This is a prototype release of highly experimental project. As such, the accuracy of Blackstone's models leaves something to be desired (F1 on the NER is approx 70%). The accuracy of these models will improve over time. 
* The models have been trained on English case law and the library has been built with the peculiarities of the legal system of England and Wales in mind. That said, the model has generalised well and should do a reasonably good job on Australasian, Canadian and American content, too.
* The data used to train Blackstone's models was derived from the [Incorporated Council of Law Reporting for England and Wales'](https://iclr.co.uk/) archive of case reports and unreported judgments. That archive is proprietary and this prevents us from releasing any of the data used to train Blackstone. 
* Blackstone is not a judge or litigation analytics tool.


## Installation

**Note!** It is strongly recommended that you install Blackstone into a virtual environment! See [here](https://realpython.com/python-virtual-environments-a-primer/) for more on virtual environments. Blackstone should compatible with Python 3.6 and higher.

To install Blackstone follow these steps:

### 1. Install the library

The first step is to install the library, which at present contains a handful of custom [spaCy](https://spacy.io/) components. Install the library like so:

```
pip install blackstone
```

### 2. Install the Blackstone model

The second step is to install the [spaCy](https://spacy.io/) model. Install the model like so:

```
pip install https://blackstone-model.s3-eu-west-1.amazonaws.com/en_blackstone_proto-0.0.1.tar.gz
```
## About the model

This is the very first release of Blackstone and the model is best viewed as a *prototype*; it is rough around the edges and represents the first step in a larger ongoing programme of open source research into NLP on legal texts being carried out by ICLR&D. 

With that out of the way, here's a brief rundown of what's happening in the proto model.

### The pipeline

The proto model included in this release has the following elements in its pipeline:

<img src="https://iclr.s3-eu-west-1.amazonaws.com/assets/iclrand/Blackstone/blackstone_pipeline.svg">

Owing to a scarcity of labelled part-of-speech and dependency training data for legal text, the `tokenizer`, `tagger` and `parser` pipeline components have been taken from [spaCy's](https://spacy.io/) `en_core_web_sm` model. By and large, these components appear to a do a decent job, but it would be good to revisit these components with custom training data at some point in the future. 

The `ner` and `textcat` components are custom components trained especially for Blackstone. 

### Named-Entity Recogniser

The NER component of the Blackstone model has been trained to detect the following entity types:

| Ent        | Name           | Examples  |
| ------------- |-------------| -----:|
| CASENAME    | Case names | e.g. *Smith v Jones*, *In re Jones*, In *Jones'* case |
| CITATION      | Citations (unique identifiers for reported and unreported cases)     |   e.g. (2002) 2 Cr App R 123 |
| INSTRUMENT | Written legal instruments     |    e.g. Theft Act 1968, European Convention on Human Rights, CPR |
| PROVISION | Unit within a written legal instrument   |    e.g. section 1, art 2(3) |
| COURT | Court or tribunal   |    e.g. Court of Appeal, Upper Tribunal |
| JUDGE | References to judges |    e.g. Eady J, Lord Bingham of Cornhill |

### Text Categoriser

This release of Blackstone also comes with a text categoriser. In contrast with the NER component (which has been trainined to identify tokens and series of tokens of interest), the text categoriser classifies longer spans of text, such as sentences. 

The Text Categoriser has been trained to classify text according to one of five mutually exclusive categories, which are as follows:

| Cat        | Description  |
| ------------- |-------------| 
| AXIOM    | The text appears to postulate a well-established principle |
| CONCLUSION     | The text appears to make a finding, holding, determination or conclusion | 
| ISSUE | The text appears to discuss an issue or question   |  
| LEGAL_TEST | The test appears to discuss a legal test |  
| UNCAT | The text does not fall into one of the four categories above  |   

## Usage

### Applying the NER model

Here's an example of how the model is applied to some text taken from para 31 of the Divisional Court's judgment in *R (Miller) v Secretary of State for Exiting the European Union (Birnie intervening)* \[2017] UKSC 5; \[2018] AC 61:

```python
import spacy

# Load the model
nlp = spacy.load("en_blackstone_proto")

text = """ 31 As we shall explain in more detail in examining the submission of the Secretary of State (see paras 77 and following), it is the Secretary of State’s case that nothing has been done by Parliament in the European Communities Act 1972 or any other statute to remove the prerogative power of the Crown, in the conduct of the international relations of the UK, to take steps to remove the UK from the EU by giving notice under article 50EU for the UK to withdraw from the EU Treaty and other relevant EU Treaties. The Secretary of State relies in particular on Attorney General v De Keyser’s Royal Hotel Ltd [1920] AC 508 and R v Secretary of State for Foreign and Commonwealth Affairs, Ex p Rees-Mogg [1994] QB 552; he contends that the Crown’s prerogative power to cause the UK to withdraw from the EU by giving notice under article 50EU could only have been removed by primary legislation using express words to that effect, alternatively by legislation which has that effect by necessary implication. The Secretary of State contends that neither the ECA 1972 nor any of the other Acts of Parliament referred to have abrogated this aspect of the Crown’s prerogative, either by express words or by necessary implication.
"""

# Apply the model to the text
doc = nlp(text)

# Iterate through the entities identified by the model
for ent in doc.ents:
    print(ent.text, ent.label_)

>>> European Communities Act 1972 INSTRUMENT
>>> article 50EU PROVISION
>>> EU Treaty INSTRUMENT
>>> Attorney General v De Keyser’s Royal Hotel Ltd CASENAME
>>> [1920] AC 508 CITATION
>>> R v Secretary of State for Foreign and Commonwealth Affairs, Ex p Rees-Mogg CASENAME
>>> [1994] QB 552 CITATION
>>> article 50EU PROVISION

```
#### Visualising entities

[spaCy](https://spacy.io/) ships with an excellent [set of visualisers](https://spacy.io/usage/visualizers), including a visualiser for NER predicts. Blackstone comes with a custom colour palette that can be used to make it easier to distiguish entities on the source text when using displacy. 

```python
"""
Visualise entities using spaCy's displacy visualiser. 

Blackstone has a custom colour palette: `from blackstone.displacy_palette import ner_displacy options`
"""

import spacy
from spacy import displacy
from blackstone.displacy_palette import ner_displacy_options

nlp = spacy.load("en_blackstone_proto")

text = """
The applicant must satisfy a high standard. This is a case where the action is to be tried by a judge with a jury. The standard is set out in Jameel v Wall Street Journal Europe Sprl [2004] EMLR 89, para 14:
“But every time a meaning is shut out (including any holding that the words complained of either are, or are not, capable of bearing a defamatory meaning) it must be remembered that the judge is taking it upon himself to rule in effect that any jury would be perverse to take a different view on the question. It is a high threshold of exclusion. Ever since Fox’s Act 1792 (32 Geo 3, c 60) the meaning of words in civil as well as criminal libel proceedings has been constitutionally a matter for the jury. The judge’s function is no more and no less than to pre-empt perversity. That being clearly the position with regard to whether or not words are capable of being understood as defamatory or, as the case may be, non-defamatory, I see no basis on which it could sensibly be otherwise with regard to differing levels of defamatory meaning. Often the question whether words are defamatory at all and, if so, what level of defamatory meaning they bear will overlap.”
18 In Berezovsky v Forbes Inc [2001] EMLR 1030, para 16 Sedley LJ had stated the test this way:
“The real question in the present case is how the courts ought to go about ascertaining the range of legitimate meanings. Eady J regarded it as a matter of impression. That is all right, it seems to us, provided that the impression is not of what the words mean but of what a jury could sensibly think they meant. Such an exercise is an exercise in generosity, not in parsimony.”
"""

doc = nlp(text)

# Call displacy and pass `ner_displacy_options` into the option parameter`
displacy.serve(doc, style="ent", options=ner_displacy_options)
```

Which produces something that looks like this:

<img src="https://iclr.s3-eu-west-1.amazonaws.com/assets/iclrand/Blackstone/displacy.png">

### Applying the text categoriser model

Blackstone's text categoriser generates a predicted categorisation for a `doc`. The `textcat` pipeline component has been designed to be applied to individual sentences rather than a single document consisting of many sentences. 

```python
import spacy

# Load the model
nlp = spacy.load("en_blackstone_proto")

def get_top_cat(doc):
    """
    Function to identify the highest scoring category
    prediction generated by the text categoriser. 
    """
    cats = doc.cats
    max_score = max(cats.values()) 
    max_cats = [k for k, v in cats.items() if v == max_score]
    max_cat = max_cats[0]
    return (max_cat, max_score)

text = """
It is a well-established principle of law that the transactions of independent states between each other are governed by other laws than those which municipal courts administer. \
It is, however, in my judgment, insufficient to react to the danger of over-formalisation and “judicialisation” simply by emphasising flexibility and context-sensitivity. \
The question is whether on the facts found by the judge, the (or a) proximate cause of the loss of the rig was “inherent vice or nature of the subject matter insured” within the meaning of clause 4.4 of the Institute Cargo Clauses (A).
"""

# Apply the model to the text
doc = nlp(text)

# Get the sentences in the passage of text
sentences = [sent.text for sent in doc.sents]

# Print the sentence and the corresponding predicted category.
for sentence in sentences:
    doc = nlp(sentence)
    top_category = get_top_cat(doc)
    print (f"\"{sentence}\" {top_category}\n")
    
>>> "In my judgment, it is patently obvious that cats are a type of dog." ('CONCLUSION', 0.9990500807762146)
>>> "It is a well settled principle that theft is wrong." ('AXIOM', 0.556410014629364)
>>> "The question is whether on the facts found by the judge, the (or a) proximate cause of the loss of the rig was “inherent vice or nature of the subject matter insured” within the meaning of clause 4.4 of the Institute Cargo Clauses (A)." ('ISSUE', 0.5040785074234009)
```

## Custom pipeline extensions

In addition to the core model, this proto release of Blackstone comes with three custom components:

* Abbreviation detection - this is *heavily* based on the `AbbreviationDetector()` component in [scispacy] and resolves an abbreviated form to its long form definition, e.g. `ECtHR` -> `European Court of Human Rights`.
* Legislation linker - this is an alpha component that attempts to resolve references to provisons to their parent instrument (more on this further down the README).
* Compound case reference detection - again, this is an alpha component that attempts identify `CASENAME` and `CITATION` pairs enabling the merging of a `CITATION` to its parent `CASENAME`.

### Abbreviation detection and long-form definition resolution

It is not uncommon for authors of legal documents to abbreviate long-winded terms that will be used instead of the long-form througout the rest of the document. For example,

> The European Court of Human Rights ("ECtHR") is the court ultimately responsible for applying the European Convention on Human Rights ("ECHR"). 

The abbreviation detection component in Blackstone seeks to address this by implementing an ever so slightly modified version of [scispaCy's](https://allenai.github.io/scispacy/) `AbbreviationDetector()` (which is itself an implementation of the approach set out in this paper: https://psb.stanford.edu/psb-online/proceedings/psb03/schwartz.pdf). Our implementation still has some problems, but an example of its usage is as follows:

```python
import spacy
from blackstone.abbreviations import AbbreviationDetector

nlp = spacy.load("en_blackstone_proto")

# Add the abbreviation pipe to the spacy pipeline.
abbreviation_pipe = AbbreviationDetector(nlp)
nlp.add_pipe(abbreviation_pipe)

doc = nlp('The European Court of Human Rights ("ECtHR") is the court ultimately responsible for applying the European Convention on Human Rights ("ECHR").')

print("Abbreviation", "\t", "Definition")
for abrv in doc._.abbreviations:
	print(f"{abrv} \t ({abrv.start}, {abrv.end}) {abrv._.long_form}")
    
>>> "ECtHR"          (7, 10) European Court of Human Rights
>>> "ECHR"   (25, 28) European Convention on Human Rights   

```

### Compound case reference detection

The compound case reference detection component in Blackstone is designed to marry up `CITATION` entities with their parent `CASENAME` entities. 

Common law jurisdictions typically relate to case references through a coupling of a name (typically derived from the names of the parties in the case) and some unique citation to identify where the case has been reported, like so:

> Regina v Horncastle \[2010] 2 AC 373

Blackstone's NER model separately attempts to identify the `CASENAME` and `CITATION` entities. However, it is potentially useful (particularly in the context of information extraction) to pull these entities out as pairs. 

`CompoundCases()` applies a custom pipe after the NER and identifies `CASENAME`/`CITATION` pairs in two scenarios:

* The standard scenario: Gelmini v Moriggia \[1913] 2 KB 549
* The possessive scenario (which is a little antiquated): Jone's case \[1915] 1 KB 45

```python
import spacy
from blackstone.compound_cases import CompoundCases

nlp = spacy.load("en_blackstone_proto")

compound_pipe = CompoundCases(nlp)
nlp.add_pipe(compound_pipe)

text = "As I have indicated, this was the central issue before the judge. On this issue the defendants relied (successfully below) on the decision of the High Court in Gelmini v Moriggia [1913] 2 KB 549. In Jone's case [1915] 1 KB 45, the defendant wore a hat."
doc = nlp(text)

for compound_ref in doc._.compound_cases:
    print(compound_ref)
    
>>> Gelmini v Moriggia [1913] 2 KB 549
>>> Jone's case [1915] 1 KB 45
```

### Legislation linker

Blackstone's Legislation Linker attempts to couple a reference to a `PROVISION` to it's parent `INSTRUMENT` by using the NER model to identify the presence of an `INSTRUMENT` and then navigating the dependency tree to identify the child provision. 

Once Blackstone has identified a `PROVISION`:`CASENAME` pair, it will attempt to generate target URLs to both the provision and the instrument on [legislation.gov.uk](https://legislation.gov.uk).

```python
import spacy
from blackstone.legislation_linker import extract_legislation_relations
nlp = spacy.load("en_blackstone_proto")

text = "The Secretary of State was at pains to emphasise that, if a withdrawal agreement is made, it is very likely to be a treaty requiring ratification and as such would have to be submitted for review by Parliament, acting separately, under the negative resolution procedure set out in section 20 of the Constitutional Reform and Governance Act 2010. Theft is defined in section 1 of the Theft Act 1968"

doc = nlp(text) 
relations = extract_legislation_relations(doc)
for provision, provision_url, instrument, instrument_url in relations:
    print(f"\n{provision}\t{provision_url}\t{instrument}\t{instrument_url}")
    
>>> section 20      http://www.legislation.gov.uk/ukpga/2010/25/section/20  Constitutional Reform and Governance Act 2010   http://www.legislation.gov.uk/ukpga/2010/25/contents

>>> section 1       http://www.legislation.gov.uk/ukpga/1968/60/section/1   Theft Act 1968  http://www.legislation.gov.uk/ukpga/1968/60/contents
```

### Sentence segmenter

Blackstone ships with a custom rule-based sentence segmenter that addresses a range of characteristics inherent in legal texts that have a tendency to baffle out-of-the-box sentence segmentation rules.

```python
import spacy
from blackstone.segmenter import sentence_segmenter

nlp = spacy.load("en_blackstone_proto")

# remove the default spaCy sentencizer from the model pipeline
if "sentencizer" in nlp.pipe_names:
    nlp.remove_pipe('sentencizer')

# add the Blackstone sentence_segmenter to the pipeline before the parser
nlp.add_pipe(sentence_segmenter, before="parser")

doc = nlp("Some more legal text goes here. And a little bit more legal text goes here")

for sent in doc.sents:
    print (sent.text)
```

## Thanks

We would like to thank the following people/organisations who have helped us (directly or indirectly) to build this prototype.

* [Mark Neumann](https://twitter.com/MarkNeumannnn) of [AI2](https://allenai.org/) and [scispaCy](https://allenai.github.io/scispacy/)
* [Explosion AI](https://explosion.ai/) for building [spaCy](https://spacy.io/) and [Prodigy](https://prodi.gy/)
* [Kristin Hodgins](https://twitter.com/kristinhodgins) of the Office of the Attorney General of British Columbia
