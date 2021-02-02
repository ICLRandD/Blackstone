
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

spacy init-model en ./release/base_medium --freqs-loc ./for_mark/word_freqs.txt -v ./word2vec.txt

# Parser, starting from base model
spacy train en ./release/parser_tagger_medium ../UD_English-EWT/en_ewt-ud-train.json ../UD_English-EWT/en_ewt-ud-dev.json -G --pipeline tagger,parser --n-iter 10 --base-model ./release/base_medium
# NER, starting from best parsing model
spacy train en ./release/ner_medium ./train.json ./dev.json -G --pipeline ner --n-iter 10 --base-model ./release/parser_tagger_medium/model-best

# Package
spacy package release/ner_medium/model-best release/ -m ./data/meta_medium.json

# Pop down in to directory, build package, copy it back up and return.
current=${pwd}
cd release/en_core_law_md-${VERSION}
python setup.py sdist
cp dist/* ../
cd ${current}
