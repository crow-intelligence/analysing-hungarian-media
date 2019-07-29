import re
import json
import pickle
from os import listdir
from os.path import isfile, join

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
matchers = [e.replace("'", "").replace('"', '') for e in matchers if '|' not in e]
counts = (len(re.findall(r"\b" + matcher + r"\b", text, re.UNICODE)) for matcher in matchers)
matcher_counts = zip(matchers, counts)
matched = (e for e in matcher_counts if e[1] > 1)


with open('data/interim/locality_coordinates.p', 'rb') as f:
    loaclity_coordinates = pickle.load(f)

with open('data/processed/count_locations.tsv', 'w') as of:
    for e in matched:
        try:
            name = patterns[e[0]]
            v = e[1]
            coords = loaclity_coordinates[name]
            print("Found %s with %s mentions" % (name, v))
            o = name + '\t' + str(v) + '\t' + str(coords[0]) + '\t' + str(coords[1]) + '\n'
            of.write(o)
        except Exception as e:
            print(e)
            continue

