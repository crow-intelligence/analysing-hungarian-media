import re
import json
import pickle
from collections import Counter
from os import listdir
from os.path import isfile, join

import trie_search
from nltk.corpus import stopwords

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
text = text.replace("megye", "")

blacklist = list(stopwords.words())
extension = ["Orbán", "Planned Parenthood", "Keret", "Oldal", "Tud", "Lett",
             "Soros", "Open", "Society", "Getty", "Kever", "Elton", "John",
             "Hosszú", "Mély", "Mag", "Boldog", "Magyar", "Angol", "Képi",
             "Viktor", "Angela", "Merkel", "Sebastian", "Rend", "Parlament",
             "Judith", "De Most", "Olasz", "Buta", "Kis", "Civil"]
with open('data/interim/stop_locations.txt', 'r') as f:
    extension2 = f.read().strip().split('\n')
extension = [e.lower() for e in extension]
extension2 = [e.lower() for e in extension2]
blacklist.extend(extension)
blacklist.extend(extension2)
blacklist = set(blacklist)

matchers = list(patterns.keys())
matchers = [e for e in matchers if '|' not in e and e not in blacklist]
non = ["peking", "brüsszel", "moszkva", 'párizs', "bécs", "pozsony",
       "bukarest", "belgrád", "kijev"]
matchers.extend(non)
for e in non:
    patterns[e] = e.title()
trie = trie_search.TrieSearch(matchers)

with open('data/interim/locality_coordinates.p', 'rb') as f:
    loaclity_coordinates = pickle.load(f)
loaclity_coordinates["Peking"] = loaclity_coordinates["Bejing"]
loaclity_coordinates["Moszkva"] = loaclity_coordinates["Moscow"]
loaclity_coordinates["Brüsszel"] = loaclity_coordinates["Bruxelles"]
loaclity_coordinates["Párizs"] = loaclity_coordinates["Paris"]
loaclity_coordinates["Bécs"] = loaclity_coordinates["Vienna"]
loaclity_coordinates["Pozsony"] = loaclity_coordinates["Bratislava"]
loaclity_coordinates["Bukarest"] = loaclity_coordinates["Bucharest"]
loaclity_coordinates["Belgrád"] = loaclity_coordinates["Beograd"]
loaclity_coordinates["Kijev"] = loaclity_coordinates["Kiev"]

locality_counts = {}
for pattern in trie.search_all_patterns(text):
    name = patterns[pattern[0]]
    if name not in locality_counts:
        locality_counts[name] = 1
    else:
        locality_counts[name] += 1

with open('data/processed/count_locations.tsv', 'w') as outfile:
    h = "Location\tLatitude\tLongitude\tCount\n"
    outfile.write(h)
    for location, count in locality_counts.items():
        if count > 20:
            latitude, longitude = loaclity_coordinates[location][0], loaclity_coordinates[location][1]
            o = location + '\t' + str(latitude) + '\t' + str(longitude) + '\t' + str(count) + '\n'
            outfile.write(o)
