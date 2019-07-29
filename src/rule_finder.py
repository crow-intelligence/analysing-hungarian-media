import re
import json
import pickle
from collections import Counter
from os import listdir
from os.path import isfile, join

from flashtext import KeywordProcessor

with open('data/interim/patterns.json', 'rb') as f:
    patterns = pickle.load(f)

text = []
in_path = 'data/seedonly'
text_files = [f for f in listdir(in_path) if isfile(join(in_path, f))]
for text_file in text_files:
    with open(join(in_path, text_file), 'r') as infile:
        for l in infile:
            text.append(l)

text = '\n'.join(text)
text = text.replace('|', ' ')
text = text.replace("'", "")
text = text.replace('"', '')

matchers = list(patterns.keys())
matchers = [e for e in matchers if '|' not in e]

with open('data/interim/locality_coordinates.p', 'rb') as f:
    loaclity_coordinates = pickle.load(f)

locality_counts = {}
for i in range(0, len(matchers), 10000):
    print(len(list(locality_counts.keys())))
    keyword_processor = KeywordProcessor()
    matchers_p = matchers[i-500:i]
    for e in matchers_p:
        keyword_processor.add_keyword(e, patterns[e])
    kf = keyword_processor.extract_keywords(text)
    kf = Counter(kf)
    for k,v in kf.items():
        locality_counts[k] = v

