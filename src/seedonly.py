from os import listdir
from os.path import isfile, join
from shutil import copy2

from tld import get_fld
import pandas as pd

in_path = 'data/final'
out_path = 'data/seedonly'

df_seed = pd.read_csv('data/raw/Crawler.tsv', sep='\t', encoding='utf-8')
df_codes = pd.read_csv('data/raw/site_codes.tsv', sep='\t', encoding='utf-8')

seed_urls = df_seed['URL']
file_url = zip(df_codes['url'], df_codes['file'])


def clean_url(url):
    p = get_fld(url)
    if p.startswith("www."):
        p = p[4:]
    if p.startswith("m."):
        p = p[2:]
    if p.startswith("dex.hu"):
        p = "index.hu"
    if p.startswith("l."):
        p = p[2:]
    if p.startswith("goog.gl"):
        p = "google.com"
    if p.startswith("youtu.be"):
        p = "youtube.com"
    return p


seed_urls = [clean_url(url) for url in seed_urls]
good_files = (e[1] for e in file_url if clean_url(e[0]) in seed_urls)
for e in good_files:
    try:
        copy2(join(in_path, e), join(out_path, e))
    except Exception as e:
        print(e)
        continue
