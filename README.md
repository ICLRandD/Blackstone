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

| Ent        | Name           | Descriptiom  |
| ------------- |-------------| -----:|
| CASENAME    | Case names | e.g. *Smith v Jones*, *In re Jones*, In *Jones'* case |
| CITATION      | Citations (unique identifiers for reported and unreported cases)     |   e.g. (2002) 2 Cr App R 123 |
| INSTRUMENT | Written legal instruments     |    e.g. Theft Act 1968, European Convention on Human Rights, CPR |
| PROVISION | Unit within a written legal instrument   |    e.g. section 1, art 2(3) |
| COURT | Court or tribunal   |    e.g. Court of Appeal, Upper Tribunal |
| JUDGE | References to judges |    e.g. Eady J, Lord Bingham of Cornhill |

### Text Categoriser



<img src="https://iclr.s3-eu-west-1.amazonaws.com/assets/iclrand/Blackstone/displacy.png">

 

  


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
