import operator
import json

from tld import get_fld
import networkx as nx
import numpy as np
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

G = nx.Graph()
for node in nodes:
    G.add_node(node, name=node)

for e in url_links:
    G.add_edge(e[0], e[1])

pr = nx.algorithms.pagerank(G)
values = sorted(set(pr.values()))
quartiles = list(np.percentile(values, [25, 50, 75]))


def get_group(url):
    if pr[url] < quartiles[0]:
        return "0"
    elif quartiles[1] > pr[url] > quartiles[0]:
        return "1"
    elif quartiles[2] > pr[url] > quartiles[1]:
        return "2"
    else:
        return "3"


hivedata = []
for node in nodes:
    d = {}
    d['name'] = node
    d['size'] = pr[node]
    group = get_group(node)
    d['group'] = group
    connections = [e for e in url_links if node in e]
    connections = [item for t in connections for item in t if item != node]
    connections = set(connections)
    d['imports'] = []
    for e in connections:
        d['imports'].append(e)
    hivedata.append(d)

with open('data/processed/hive.json', 'w') as f:
    json.dump(hivedata, f)

forced = {}
forced['nodes'] = []
forced['links'] = []

sorted_pr = sorted(pr.items(), key=lambda kv: kv[1], reverse=True)[:100]
top_nodes = [e[0] for e in sorted_pr]
for node in top_nodes:
    d = {}
    d['size'] = pr[node]
    d['group'] = get_group(node)
    d['id'] = node
    forced['nodes'].append(d)

for link in url_links:
    if link[0] in top_nodes and link[1] in top_nodes:
        d = {}
        d['source'] = link[0]
        d['target'] = link[1]
        d['value'] = 1
        forced['links'].append(d)

with open('data/processed/force.json', 'w') as f:
    json.dump(forced, f)

G2 = nx.Graph()
for node in nodes:
    if int(get_group(node)) > 2:
        G2.add_node(node, name=node)

for e in url_links:
    if int(get_group(e[0])) > 2 and int(get_group(e[1])) > 2:
        G2.add_edge(e[0], e[1])

nx.write_graphml(G2, 'data/processed/graph.graphml')

base_counts = {}
for k, v in url_base.items():
    if v not in base_counts and v in nodes:
        base_counts[v] = 1
    else:
        if v in nodes:
            base_counts[v] += 1
sorted_sites = sorted(base_counts.items(), key=lambda kv: kv[1], reverse=True)[:99]
other = sum(list(base_counts.values())) - sum([e[1] for e in sorted_sites])
sorted_sites.append(('Other', other))

with open('data/processed/site_counts.tsv', 'w') as f:
    h = 'site\tcount\n'
    f.write(h)
    for e in sorted_sites:
        o = e[0] + '\t' + str(e[1]) + '\n'
        f.write(o)
