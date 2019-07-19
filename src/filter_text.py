import json
from os.path import join
from shutil import copy2

import pandas as pd
from tld import get_fld

with open('data/processed/graph.json', 'r') as f:
    d = json.load(f)

nodes = d['nodes']
nodes = [e['site'] for e in nodes]


def normalize_url(url):
    p = get_fld(url)
    if p.startswith('www.'):
        p = p[4:]
    if p.startswith('m.'):
        p = p[2:]
    if p.startswith('dex.hu'):
        p = 'index.hu'
    if p.startswith('l.'):
        p = p[2:]
    return p


df = pd.read_csv('data/raw/site_codes.tsv', sep='\t', encoding='utf-8')
id_url = zip(df['file'], df['url'])
good_ids = (e[0] for e in id_url if normalize_url(e[1]) in nodes)

in_path = 'data/raw/text'
out_path = 'data/raw/filtered'
for e in good_ids:
    try:
        copy2(join(in_path, e), join(out_path, e))
    except Exception as e:
        print(e)
        continue
