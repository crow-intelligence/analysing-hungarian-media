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
processed = [f for f in listdir(out_path) if isfile(join(out_path, f))]
texts = [t for t in texts if t not in processed]

nlp = hu_core_ud_lg.load()
nlp2 = spacy.load('models')
tokenizer = nltk.tokenize.PunktSentenceTokenizer()

#entities = []


def startswithalpha(wd):
    if wd[0].isalpha():
        return True
    else:
        return False


def stem_text(text):
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
        del doc2

        def stem_last(ner):
            ner = ner.strip().split()
            ner = [e.strip().title() for e in ner]
            if len(ner) == 1:
                if ner[0] in word_lemma:
                    return word_lemma[ner[0]]
                else:
                    return ner[0]
            else:
                first_part = ' '.join(ner[:-1])
                if ner[-1] in word_lemma:
                    stemmed_last = word_lemma[ner[-1]]
                else:
                    stemmed_last = ner[-1]
                stemmed_ner = first_part + ' ' + stemmed_last
                return stemmed_ner

        for token in doc:
            word_lemma[token.text] = token.lemma_
        entitiy_types = [(e[0], stem_last(e[1])) for e in entitiy_types]
        #entities.append(entitiy_types)
        stemmed_sentence = [word.text for word in doc]
        del doc
        stemmed_sentence = [wd for wd in stemmed_sentence if startswithalpha(
            wd)]
        stemmed_sentence = ' '.join(stemmed_sentence)

        if len(entitiy_types) > 0:
            for e in entitiy_types:
                stuff = e[1]
                if len(stuff.split()) > 1:
                    new_stuff = '|'.join(stuff.split())
                    stemmed_sentence = stemmed_sentence.replace(stuff,
                                                                new_stuff)
        stemmed_sentence = stemmed_sentence.split()

        def final_stem(wd):
            if wd in word_lemma:
                return word_lemma[wd].lower()
            elif '|' in wd:
                return wd.lower()
            else:
                return ''
        stemmed_sentence = [final_stem(wd) for wd in stemmed_sentence]
        stemmed_sentence = [wd for wd in stemmed_sentence if len(wd) > 0]
        stemmed_sentence = ' '.join(stemmed_sentence)
        stemmed_text.append(stemmed_sentence)

    stemmed_text = '\n'.join(stemmed_text)
    with open(join(out_path, text), 'w') as outfile:
        outfile.write(stemmed_text)


for t in texts:
    stem_text(t)
# with ProcessPoolExecutor(max_workers=2) as executor:
#     executor.map(stem_text, texts)

#with open('data/interim/entities.p', 'wb') as outfile:
#    pickle.dumps(entities, outfile)

