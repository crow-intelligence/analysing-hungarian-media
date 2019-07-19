import pickle
from os import listdir
from os.path import isfile, join
from concurrent.futures import ProcessPoolExecutor

import nltk
import spacy
import hu_core_ud_lg

in_path = 'data/raw/filtered'
out_path = 'data/stemmed_text'

texts = [f for f in listdir(in_path) if isfile(join(in_path, f))]

nlp = hu_core_ud_lg.load()
tokenizer = nltk.tokenize.PunktSentenceTokenizer()


def startswithalpha(wd):
    if wd[0].isalpha():
        return True
    else:
        return False


word_lemma = []


def stem_text(text):
    with open(join(in_path, text), 'r') as infile:
        txt = infile.read().strip()
        sentences = tokenizer.tokenize(txt)
    stemmed_text = []
    for sentence in sentences:
        doc = nlp(sentence)
        for token in doc:
            stemmed_text.append(token.lemma_.lower())
            wd_stem = (token, token.lemma_)
            if wd_stem not in word_lemma:
                word_lemma.append(wd_stem)
    stemmed_text = [wd for wd in stemmed_text if startswithalpha(wd)]
    stemmed_text = ' '.join(stemmed_text)
    with open(join(out_path, text), 'w') as outfile:
        outfile.write(stemmed_text)


with ProcessPoolExecutor(max_workers=10) as executor:
    executor.map(stem_text, texts)


with open('data/interim/vocab.p', 'wb') as f:
    pickle.dump(word_lemma, f)

