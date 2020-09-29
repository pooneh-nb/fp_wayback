#In this code we remove the duplicate script urls from fingerprinting_donains.json (collection of script_urls, resultof web crawling using fp-inspector)
#input: fingerprinting_domains.json
# outout : thirdparties.json
import json
import tldextract as tld

with open("/home/pooneh/PycharmProjects/OpenWPM/datasets/fingerprinting_domains.json") as read_file:
    data = json.load(read_file)
thirdparties = {}
listValue = []
#for i in range(len(data['46ae8bbbe8220fd334b5638705257324'])):
    #print(data['46ae8bbbe8220fd334b5638705257324'][i]['script_url'])

hashes = set()
for key in data.keys():
    hashes.add(key)
a =0;
for hash in hashes:
    for ind in range(len(data[hash])):
        script_url_domain = tld.extract(data[hash][ind]['script_url']).domain
        top_url_domain = tld.extract(data[hash][ind]['top_url']).domain
        if script_url_domain != top_url_domain:
            script_url = data[hash][ind]['script_url']
            top_url = data[hash][ind]['top_url']
            listValue.append({"script_url": script_url, "top_url": top_url})
    if len(listValue) != 0:
        thirdparties[hash] = listValue
        listValue = []


with open('../datasets/thirdparties.json', 'w') as fp:
    json.dump(thirdparties, fp, sort_keys=True, indent=4)
