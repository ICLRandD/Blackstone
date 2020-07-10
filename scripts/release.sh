
set -e

# Notes
# Important to install spacy-lookups-data before running this script, as otherwise
# models don't have lemmatization and normalization data.
# TODO: 
# - add version not from metadata files
# - try out pretraining with raw text
# - clean up release models after the fact
# - explicitly clone the EWT repo

mkdir release

spacy init-model en ./release/base_small --freqs-loc ./for_mark/word_freqs.txt
spacy init-model en ./release/base_medium --freqs-loc ./for_mark/word_freqs.txt -v ./word2vec.txt


# Parser, starting from base model
spacy train en ./release/parser_tagger_small ../UD_English-EWT/en_ewt-ud-train.json ../UD_English-EWT/en_ewt-ud-dev.json -G --pipeline tagger,parser --n-iter 10 --base-model ./release/base_small --meta-path ./data/meta_small.json
# NER, starting from best parsing model
spacy train en ./release/ner_small ./train.json ./dev.json -G --pipeline ner --n-iter 10 --base-model ./release/parser_tagger_small/model-best --meta-path ./data/meta_small.json

# Package
spacy package release/ner_small/model-best release/ -m ./data/meta_small.json

# Pop down in to directory, build package, copy it back up and return.
current=${pwd}
cd release/en_core_law_sm-0.1.0
python setup.py sdist
cp dist* ../
cd ${current}
