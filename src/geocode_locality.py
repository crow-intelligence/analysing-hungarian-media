import pandas as pd

loaclity_coordinates = {}

with open('data/interim/allCountries.txt', 'r') as f:
    for l in f:
        l = l.strip().split('\t')
        locality = l[1]
        lat = l[4]
        long = l[5]
        loaclity_coordinates[locality] = (lat, long)

hungarian_df = pd.read_csv('data/interim/hungarian_geonames.tsv',
                           sep='\t',
                           encoding='utf-8')

hu_loc_coords = zip(hungarian_df['Location'], hungarian_df['Lat'], hungarian_df['Long'])
for e in hu_loc_coords:
    loaclity_coordinates[e[0]] = (e[1], e[2])

df_translate = pd.read_csv('data/interim/Hungarian2English top cities - Sheet1.tsv',
                           sep='\t',
                           encoding='utf-8')
eng_to_hu = zip(df_translate['EN'], df_translate['HU'])
for e in eng_to_hu:
    if e[0] in loaclity_coordinates:
        cords = loaclity_coordinates[e[0]]
        loaclity_coordinates[e[0]] = cords

import pickle
import json
with open('data/interim/locality_coordinates.p', 'wb') as f:
    pickle.dump(loaclity_coordinates, f)

matcher_match = {}
for k in loaclity_coordinates.keys():
    name = k.lower()
    if ' ' in name:
        matcher_match[name] = k
        matcher_match[name.replace(' ', '|')] = k
    else:
        matcher_match[name] = k

with open('data/interim/patterns.json', 'wb') as f:
    pickle.dump(matcher_match, f)
