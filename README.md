<img src="https://iclr.s3-eu-west-1.amazonaws.com/assets/iclrand/sitecode.svg" width=20%>
<img src="https://iclr.s3-eu-west-1.amazonaws.com/assets/iclrand/blackstone_seal.svg" height=75%>

# Blackstone
Automatic enrichment of unstructured legal text using rules-based and predictive techniques

## Installation

**Note!** It is strongly recommended that you install Blackstone into a virtual environment! See [here](https://realpython.com/python-virtual-environments-a-primer/) for more on virtual environments.

To install Blackstone follow these steps:

### 1. Install the library

The first step is to install the library, which at present contains a handful of custom spaCy components. Install the library like so:

```
pip install blackstone
```

### 2. Install the model

The second step is to install the spaCy model. Install the model like so:

```
pip install https://blackstone-model.s3-eu-west-1.amazonaws.com/en_blackstone_proto-0.0.1.tar.gz
```
## About the model

This is the very first release of Blackstone and the model is best viewed as a *prototype*; it is rough around the edges and represents first step in a large and ongoing programme of open source research into NLP on legal texts. With that out of the way, here's a brief rundown of what's happening in the proto model.

Blackstone is a spaCy model and pipeline, which means you can apply the model to your own text data using spaCy's APIs. 

### The pipeline

Blackstone's model has been built with, and upon, spaCy. This proto release combines a mixture of pipeline components that have been custom built for Blackstone, along with other

The proto model included in this release has the following elements in its pipeline:

<img src="https://iclr.s3-eu-west-1.amazonaws.com/assets/iclrand/Blackstone/blackstone_pipeline.svg">

Owing to a complete dearth of labelled part-of-speech and dependency training data for legal text, the `tokenizer`, `tagger` and `parser` pipeline components have been taken from spaCy's `en_core_web_sm` model. By and large, these components appear to a do a decent job, but it would be good to revisit these components with custom training data at some point in the future. 

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

This release of Blackstone also comes with a text categoriser. In contrast with the NER component (which has been trainined to identify tokens and series of tokens of interest), other text categoriser classifier longer spans of text, such as sentences. 

The Text Categoriser has been trained to classify text according to one of five mutually exclusive categories, which are as follows:

| Cat        | Descriptiom  |
| ------------- |-------------| 
| AXIOM    | The text appears to postulate a well-established principle |
| CONCLUSION     | The text appears to make a finding, holding, determination or conclusion | 
| ISSUE | The text appears to discuss an issue or question   |  
| LEGAL_TEST | The test appears to discuss a legal test |  
| UNCAT | The text does not fall into one of the four categories above  |   

## Usage

### Applying the NER model

Here's an example of how the model is applied to some text taken from para 31 of the Divisional Court's judgment in *R (Miller) v Secretary of State for Exiting the European Union (Birnie intervening)* \[2017] UKSC 5; \[2018] AC 61; :

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

spaCy ships with an excellent set of visualisers, including a visualiser for NER predicts. Blackstone comes with a custom colour palette that can be used to make it easier to distiguish entities on the source text. 

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

* Abbreviation detection - this is *heavily* based on the `AbbreviationDetector()` component in [scispacy] and resolves an abrreviated form to its long form definition, e.g. `HRA 1998` -> `Human Rights Act 1998`.
* Legislation linker - this is an alpha component that attempts to resolve references to provisons to their parent instrument (more on this further down the README).
* Compound case reference detection - again, this is an alpha component that attempts identify `CASENAME` and `CITATION` pairs enabling the merging of a `CITATION` to its parent `CASENAME`.


    
    

  


## Project Name
Blackstone 

## Project Keywords
Natural language processing; machine-learning; unstructured text data

## Problem Space
Automatic enrichment of unstructured legal texts, with an emphasis on judgments and other long-form legal material (e.g. academic articles, reports etc). Enrichment of contracts is already well-served and therefore does not fall within the scope of this project. 

## Project Description
There is no shortage of commercial, closed-source software that uses natural language processing and computational linguists to provide insight into unstructured legal texts, such as contracts, credit agreements and leases.

The purpose of Blackstone is to apply similar techniques, technologies and strategies to other types of unstructured legal texts, particularly judgments, in order to generate an open-source model that can be used and extended by others.

**Phase 1**

The initial focus of the project will be to develop a model that is capable of automatically identifying the following fundamental entity types that are peculiar to legal writing:

Case titles - e.g. Regina v Smith

Neutral citations - e.g. `[2019] EWCA Crim 345`

Regular citations - e.g. `[2015] AC 345` or `[2015] 2 Cr App R 7`

Primary legislation - e.g. `Criminal Justice Act 2003`

Secondary legislation - e.g. `The Wine (Amendment) Regulations 2019`

Regnal years - e.g. `8 & 9 Geo. 6, c. 4`

**Phase 2**

The second phase of the project will focus on extending the model developed in Phase 1 to identify the following:

Instances in which the author appears to postulate an axiom of the law (e.g. It is a well-established principle that...)
Instances of ratio in judgments
Instances in which earlier authority is being subjected to "judicial consideration" going beyond mere citation (e.g. where an earlier authority is subject to positive or negative judicial consideration)

## Tooling
#### Dataset 
XML archive of law reports published by ICLR dating back to 1865 and raw text of unreported judgments dating back to 2000.

#### Runtime 
Python 3.6+

## Core Libraries 
spaCy and Pandas

## Other tools 
Prodigy for model refinement and testing, Jupyter for experiments.
