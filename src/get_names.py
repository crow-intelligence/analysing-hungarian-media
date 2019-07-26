import operator
from collections import Counter
from os import listdir
from os.path import isfile, join

from nltk.corpus import stopwords

in_path = 'data/seedonly'

txt_files = [f for f in listdir(in_path) if isfile(join(in_path, f))]


ffi = []
no = []

with open('data/raw/osszesffi.txt', 'r', encoding='iso-8859-2') as f:
    male = f.read().strip().split('\n')
male = [name.lower() for name in male]

with open('data/raw/osszesnoi.txt', 'r', encoding='iso-8859-2') as f:
    female = f.read().strip().split('\n')
female = [name.lower() for name in female]


def analyze_name(ner):
    if ner[-1] in male:
        ffi.append(' '.join(ner))
    if ner[-1].endswith('né') and ner[-1][:-2] in male:
        no.append(' '.join(ner))
    if ner[-1] in female:
        no.append(' '.join(ner))


functionwords = set(stopwords.words())

wds = set()
for txt_file in txt_files:
    with open(join(in_path, txt_file), 'r') as infile:
        txt = infile.read().split()
        words = [wd for wd in txt if wd not in functionwords]
        words = set([' '.join(wd.split('|')) for wd in words if len(wd) > 2])
        for wd in words:
            if wd not in wds:
                wds.add(wd)
        ners = [wd.split('|') for wd in txt if '|' in wd]
        for ner in ners:
            analyze_name(ner)

ffi = Counter(ffi)
sorted_ffi = sorted(ffi.items(), key=operator.itemgetter(1), reverse=True)
with open('data/processed/ffi_nevek.tsv', 'w') as outfile:
    for e in sorted_ffi:
        o = e[0].title() + '\t' + str(e[1]) + '\n'
        outfile.write(o)

no = Counter(no)
sorted_no = sorted(no.items(), key=operator.itemgetter(1), reverse=True)
with open('data/processed/noi_nevek.tsv', 'w') as outfile:
    for e in sorted_no:
        o = e[0].title() + '\t' + str(e[1]) + '\n'
        outfile.write(o)

wds = {wd for wd in wds if wd not in ffi and wd not in no}
print(len(wds))
with open('data/interim/togeocode.txt', 'w') as f:
    for e in wds:
        f.write(e + '\n')
