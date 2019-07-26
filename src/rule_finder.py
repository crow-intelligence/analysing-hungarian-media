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

matchers = patterns.keys()
counts = (text.count(matcher) for matcher in matchers)
matcher_counts = zip(matchers, counts)
matched = (e for e in matcher_counts if e[1] > 0)


with open('data/interim/locality_coordinates.p', 'rb') as f:
    loaclity_coordinates = pickle.load(f)

of = open('data/processed/count_locations.tsv', 'w')
for e in matched:
    name = patterns[e[0]]
    v = e[1]
    coords = loaclity_coordinates[name]
    print("Found %s with %s mentions" % (name, v))
    o = name + '\t' + str(v) + '\t' + str(coords[0]) + '\t' + str(coords[1]) + '\n'
    of.write(o)
of.close()
