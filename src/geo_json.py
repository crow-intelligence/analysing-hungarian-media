import json
import pandas as pd

f = 'data/processed/count_locations.tsv'
df = pd.read_csv(f, sep='\t', encoding='utf-8')
data = zip(df['Location'], df['Latitude'], df['Longitude'], df['Count'])

js = []

for e in data:
    d = {}
    d['name'] = e[0]
    d['country'] = ''
    d['type'] = ''
    d['lat'] = e[1]
    d['lon'] = e[2]
    d['elevation'] = e[3]
    js.append(d)

with open('data/processed/geo_json.json', 'w') as outfile:
    json.dump(js, outfile)
