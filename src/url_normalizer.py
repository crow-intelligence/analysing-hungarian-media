import json

from tld import get_fld
import pandas as pd

url_df = pd.read_csv('data/raw/urllist.csv', sep=',', encoding='utf-8')
urls = list(url_df['url'])

hu_urls_df = pd.read_csv('data/raw/site_codes.tsv',
                         sep='\t', encoding='utf-8')
hu_urls = set(hu_urls_df['url'])

url_base = {}


for url in urls:
    if url in hu_urls:
        p = get_fld(url)
        if p.startswith('www.'):
            p = p[4:]
        if p.startswith('m.'):
            p = p[2:]
        if p.startswith('dex.hu'):
            p = 'index.hu'
        if p.startswith('l.'):
            p = p[2:]
        url_base[url] = p

print('checked urls')

links_df = pd.read_csv('data/raw/link.csv', sep=',', encoding='utf-8')
url_links_codes = zip(links_df['fromid'], links_df['toid'])


def add_url_link(code):
    node1 = code[0] -1
    node2 = code[1] - 1
    url1 = urls[node1]
    url2 = urls[node2]
    if url1 in hu_urls and url2 in hu_urls:
        base1 = url_base[url1]
        base2 = url_base[url2]
        if base1 != base2:
            return (base1, base2)
        else:
            return None
    else:
        return None


print('before gen comprehension')
url_links = (add_url_link(c) for c in url_links_codes)
print('after gen comprehension')
# with ProcessPoolExecutor(max_workers=20) as executor:
#     executor.map(add_url_link, url_links_codes)

#nodes = list(set(list(url_base.values())))
url_links = set(url_links)
url_links = {e for e in url_links if e}
nodes = set()
for e in url_links:
    if e[0] not in nodes:
        nodes.add(e[0])
    if e[1] not in nodes:
        nodes.add(e[1])
nodes = list(nodes)
print(len(nodes), len(url_links))

dataset = {}
dataset["nodes"] = []
dataset["links"] = []

for node in nodes:
    d = {}
    d["id"] = str(nodes.index(node))
    d["site"] = node
    dataset["nodes"].append(d)

for link in url_links:
    d = {}
    d["source"] = str(nodes.index(link[0]))
    d["target"] = str(nodes.index(link[1]))
    dataset["links"].append(d)

with open('data/processed/graph.json', 'w') as f:
    json.dump(dataset, f)

hivedata = []
for node in nodes:
    t = {}
    t['name'] = node
    t['imports'] = []
    connections = [e for e in url_links if node in e]
    connections = [item for t in connections for item in t if item != node]
    connections = set(connections)
    for e in connections:
        t['imports'].append(e)
    t['size'] = len(connections)
    hivedata.append(t)

with open('data/processed/hive.json', 'w') as f:
    json.dump(hivedata, f)
