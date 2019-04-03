import os, re, pathlib
import spacy
import pandas as pd

def custom_sentencizer(doc):
    for i, token in enumerate(doc[:-2]):
        if token.text == "]" and doc[i+1].like_num:
            doc[i+1].is_sent_start = False
        elif token.text == '[':
            doc[i + 1].is_sent_start = False
        elif token.text == ')':
            doc[i + 1].is_sent_start = False
        elif token.text == ']':
            doc[i + 1].is_sent_start = False
        elif doc[i].like_num and doc[i+1].is_punct:
            doc[i + 2].is_sent_start = False
        elif doc[i].like_num:
            doc[i + 1].is_sent_start = False





    return doc

path='/Users/Daniel/export-searchables/judgments/xml'
print(os.getcwd())
print(path)
os.chdir(path)
nlp = spacy.load('en_core_web_lg')
nlp.add_pipe(custom_sentencizer, before="parser")
print("Model loaded!")

for filename in os.listdir(path):
    if '2006002499' in filename:

        f=open(filename)
        content=f.read()

        print("Cleaning text....")
        content=content.replace('<year>', '')
        content = content.replace('</year>', '')
        content = content.replace('<vol>', '')
        content = content.replace('</vol>', '')
        content = content.replace('<pub>', '')
        content = content.replace('</pub>', '')
        content = content.replace('<pages>', '')
        content = content.replace('</pages>', '')
        print("Text cleaned!")

        doc=nlp(content)

        for sent in doc.sents:
            print('****', sent.text)