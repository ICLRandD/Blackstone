
set -e
VERSION=${1}

# Notes
# Important to install spacy-lookups-data before running this script, as otherwise
# models don't have lemmatization and normalization data.
# TODO: 
# - add version not from metadata files
# - try out pretraining with raw text
# - clean up release models after the fact
# - explicitly clone the EWT repo

mkdir -p release

spacy init-model en ./release/base_small --freqs-loc ./for_mark/word_freqs.txt

# Parser, starting from base model
spacy train en ./release/parser_tagger_small ../UD_English-EWT/en_ewt-ud-train.json ../UD_English-EWT/en_ewt-ud-dev.json -G --pipeline tagger,parser --n-iter 10 --base-model ./release/base_small
# NER, starting from best parsing model
spacy train en ./release/ner_small ./train.json ./dev.json -G --pipeline ner --n-iter 10 --base-model ./release/parser_tagger_small/model-best

# Package
spacy package release/ner_small/model-best release/ -m ./data/meta_small.json

# Pop down in to directory, build package, copy it back up and return.
current=${pwd}
cd release/en_core_law_sm-${VERSION}
python setup.py sdist
cp dist* ../
cd ${current}
