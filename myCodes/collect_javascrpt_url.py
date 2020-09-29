import json
import pandas as pd

with open("/datasets/fingerprinting_domains.json") as read_file:
    data = json.load(read_file)


hashes = set()
links = []
for key in data.keys():
    hashes.add(key)

for hash in hashes:
        links.append(data[hash][0]['script_url'])

df = pd.DataFrame(list(links))

with open('../datasets/script_urls.json', 'w') as fp:
    json.dump(links, fp, sort_keys=True, indent=4)
#df.to_csv('scrpt_urls')
