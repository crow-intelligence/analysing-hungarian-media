from collections import Counter
from os import listdir
from os.path import isfile, join

# from nltk.corpus import stopwords
# from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder

in_path = 'data/stemmed_text'
out_path = 'data/final'

txt_files = [f for f in listdir(in_path) if isfile(join(in_path, f))]

full_text = []
for txt_file in txt_files:
    with open(join(in_path, txt_file), 'r') as infile:
        for l in infile:
            l = l.strip().split()
            l = [wd for wd in l if len(wd) < 50 and len(wd) > 0]
            #l = [wd for wd in l if '|' not in wd]
            full_text.extend(l)

wfreq = Counter(full_text)
filtered_text = set([wd for wd in full_text if wfreq[wd] > 30])

for txt_file in txt_files:
    text_filtered = []
    with open(join(in_path, txt_file), 'r') as infile:
        for l in infile:
            l = l.strip().split()
            l = [wd for wd in l if wd in filtered_text]
            if len(l) > 1:
                l = ' '.join(l)
                text_filtered.append(l)
    text_filtered = '\n'.join(text_filtered)
    if len(text_filtered) > 0:
        with open(join(out_path, txt_file), 'w') as outfile:
            outfile.write(text_filtered)

with open('data/interim/word_freq.tsv', 'w') as outfile:
    for wd in filtered_text:
        o = wd + '\t' + str(wfreq[wd]) + '\n'
        outfile.write(o)

# def bag_of_bigrams_words(words, score_fn=BigramAssocMeasures.chi_sq, n=500):
#     bigram_finder = BigramCollocationFinder.from_words(words)
#     bigrams = bigram_finder.nbest(score_fn, n)
#     return bigrams
#
#
# sigbigs = bag_of_bigrams_words(filtered_text)
# with open('data/interim/sigbigs.tsv', 'w') as outfile:
#     for e in sigbigs:
#         o = e[0] + '\t' + e[1] + '\n'
#         outfile.write(o)
