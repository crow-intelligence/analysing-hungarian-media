from time import sleep

from geopy.geocoders import Nominatim

with open('data/interim/togeocode.txt', 'r') as f:
    tocode = f.read().strip().split('\n')

geolocator = Nominatim(user_agent="https://artificialintelligence.hu")

i = len(tocode)
with open('data/processed/geocoded.tsv', 'w') as outfile:
    for e in tocode:
        try:
            location = geolocator.geocode(e.title())
            if e in location.address:
                o = e.title() + '\t' + str(location.latitude) + '\t' + str(location.longitude) + '\n'
                outfile.write(o)
                print(o)
            sleep(2)
        except Exception as e:
            print(e)
            continue
            sleep(1.1)
        print(i)
        i -= 1
