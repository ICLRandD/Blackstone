#!/usr/bin/env python

# Generate word embeddings for use when initialising the base model

from pathlib import Path
from gensim.models import Word2Vec, Phrases
from gensim.models.word2vec import LineSentence

import plac
import logging

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)


def compute_vectors(input_path: Path, output_path: Path):
    """
    Builds word embeddings using gensim Word2Vec. This function takes
    a file contained single sentences per line and writes to computed
    vectors in text format to the specified output path. 
    """
    print(f"Processing {input_path}")
    sentences = LineSentence(input_path)
    bigram_transformer = Phrases(sentences)
    model = Word2Vec(
        bigram_transformer[sentences], size=150, window=5, min_count=5, workers=4
    )
    print(f"Saving vectors to {output_path}")
    model.wv.save_word2vec_format(output_path, binary=False)


@plac.annotations(
    sent_loc=("Location of input sentences file", "positional", None, Path),
    output_dir=("Location of output vector file", "positional", None, Path),
)
def main(sent_loc: Path, output_dir: Path):
    compute_vectors(sent_loc, output_dir)


if __name__ == "__main__":
    plac.call(main)
