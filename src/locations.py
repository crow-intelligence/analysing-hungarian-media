import pickle
from os import listdir
from os.path import isfile, join
from concurrent.futures import ProcessPoolExecutor

import nltk
import spacy
import hu_core_ud_lg

in_path = 'data/raw/filtered'

texts = [f for f in listdir(in_path) if isfile(join(in_path, f))]

nlp = hu_core_ud_lg.load()
nlp2 = spacy.load('models')
tokenizer = nltk.tokenize.PunktSentenceTokenizer()

locations = {}
i = len(texts)
for text in texts:
    with open(join(in_path, text), 'r') as infile:
        txt = infile.read().strip()
        sentences = tokenizer.tokenize(txt)

    stemmed_text = []
    for sentence in sentences:
        word_lemma = {}
        doc = nlp(sentence)
        tokens = nltk.word_tokenize(sentence)
        tokens = ' '.join(tokens)
        doc2 = nlp2(tokens)
        entitiy_types = [(entity.label_, entity.text) for entity in doc2.ents]
        entitiy_types = [entity[1] for entity in entitiy_types
                         if entity[0] == 'LOC' and len(entity[1]) > 1]
        del doc2

        def stem_last(ner):
            ner = ner.strip().split()
            ner = [e.strip().title() for e in ner]
            if len(ner) == 1:
                if ner[0] in word_lemma:
                    return word_lemma[ner[0]]
                elif ner[0].lower().endswith('-ban') or \
                    ner[0].lower().endswith('-ben') or \
                    ner[0].lower().endswith('-nak') or \
                    ner[0].lower().endswith('-nek') or \
                    ner[0].lower().endswith('-on') or \
                    ner[0].lower().endswith('-en') or \
                    ner[0].lower().endswith('-ön') or \
                    ner[0].lower().endswith('-t'):
                    return ner[0].split('-')[0]
                else:
                    return ner[0]
            else:
                first_part = ' '.join(ner[:-1])
                if ner[-1] in word_lemma:
                    stemmed_last = word_lemma[ner[-1]]
                elif '-' in ner[-1]:
                    stemmed_last = ner[-1].split('-')[0]
                else:
                    stemmed_last = ner[-1]
                stemmed_ner = first_part + ' ' + stemmed_last
                return stemmed_ner

        if len(entitiy_types) > 0:
            for token in doc:
                word_lemma[token.text] = token.lemma_
            entitiy_types = [stem_last(e) for e in entitiy_types]
            for e in entitiy_types:
                if e not in locations:
                    locations[e] = 1
                else:
                    locations[e] += 1
    print(i)
    i -= 1

with open('data/processed/locations.tsv', 'w') as outfile:
    for k, v in locations.items():
        o = k + '\t' + str(v) + '\n'
        outfile.write(o)
