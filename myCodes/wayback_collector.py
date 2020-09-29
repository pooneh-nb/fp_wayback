import json
import requests
from datetime import date, timedelta
import pandas as pd
import urllib as lib
import hashlib as hash
import os.path
import time

# load script_url.json
results = set()
with open("/home/pooneh/PycharmProjects/OpenWPM/datasets/script_urls.json", 'rt') as f:
    h_url = json.load(f)
# json to set
script_urls = set()
for h in h_url:
    script_urls.add(h)
script_urls = sorted(script_urls)
# empty dataframe- log of script urls in 10yrs
history_df = pd.DataFrame(columns=['requestedDate', 'closestDate', 'URL'])
wayback_url = {}

err_logs = {'errors': []}


# availability API, check the previous snapshots of a url
def availability_api():

    for script_url in script_urls:
        start_date = date(2010, 1, 1)
        end_date = date(2020, 12, 1)
        delta = timedelta(days=30)
        print("requested url: " + script_url)
        while start_date <= end_date:
            record = []
            try:
                start = time.time()
                requested_time = start_date.strftime("%Y%m%d")
                start_date += delta
                response = requests.get(
                    "http://archive.org/wayback/available?url=" + script_url + "&timestamp=" + requested_time)
                print("requested time" + requested_time)
                #time.sleep(2)

                print(response.raise_for_status())
                if response.status_code == 200:
                    # if not response.raise_for_status():
                    response_json = response.json()
                    if response_json['archived_snapshots'] != {}:
                        if requested_time[0:6] == response_json['archived_snapshots']['closest']['timestamp'][0:6]:
                            hash_script = js_content_download(response_json['archived_snapshots']['closest']['url'][42:])
                            if hash_script:
                                'requestedDate', 'closestDate', 'URL'
                                wayback_url[hash_script] = \
                                    {"requestedDate": requested_time,
                                     "closestDate":
                                     response_json['archived_snapshots']['closest']['timestamp'][0:8],
                                     "url": response_json['archived_snapshots']['closest']['url'][42:]}
                                print("your req time: " + response_json['timestamp'], "my closest time: " +
                                      response_json['archived_snapshots']['closest']['timestamp'][0:8])
                end = time.time()
                print(end - start)

            except requests.exceptions.HTTPError as errh:
                if errh.code == 429:
                    print("OOps: 429, too many requests", errh)
                    err_logs['errors'].append(
                        {"script_url": script_url, "requested_time": requested_time, "error": "429, too many requests"})
                    with open('/home/pooneh/PycharmProjects/OpenWPM/jsons/err_logs.json', 'w') as fp:
                        json.dump(err_logs, fp, sort_keys=True, indent=4)
                    time.sleep(30)
                    pass
                else:
                    print("Http Error:", errh)
                    err_logs['errors'].append(
                        {"script_url": script_url, "requested_time": requested_time, "error": "Http Error"})
                    with open('/home/pooneh/PycharmProjects/OpenWPM/jsons/err_logs.json', 'w') as fp:
                        json.dump(err_logs, fp, sort_keys=True, indent=4)
                    pass
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
                err_logs['errors'].append(
                    {"script_url": script_url, "requested_time": requested_time, "error": "Error Connecting"})
                with open('/home/pooneh/PycharmProjects/OpenWPM/jsons/err_logs.json', 'w') as fp:
                    json.dump(err_logs, fp, sort_keys=True, indent=4)
                pass
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
                err_logs['errors'].append(
                    {"script_url": script_url, "requested_time": requested_time, "error": "Timeout Error"})
                with open('/home/pooneh/PycharmProjects/OpenWPM/jsons/err_logs.json', 'w') as fp:
                    json.dump(err_logs, fp, sort_keys=True, indent=4)
                pass
            except requests.exceptions.RequestException as errn:
                print("OOps: another request error", errn)
                err_logs['errors'].append(
                    {"script_url": script_url, "requested_time": requested_time, "error": "another request error"})
                with open('/home/pooneh/PycharmProjects/OpenWPM/jsons/err_logs.json', 'w') as fp:
                    json.dump(err_logs, fp, sort_keys=True, indent=4)
                pass
            except:
                print("OOps: unexpected!")
                err_logs['errors'].append({"script_url": script_url, "requested_time": requested_time, "error": "unexpected"})
                with open('/home/pooneh/PycharmProjects/OpenWPM/jsons/err_logs.json', 'w') as fp:
                    json.dump(err_logs, fp, sort_keys=True, indent=4)
                time.sleep(15)
                pass


with open('/home/pooneh/PycharmProjects/OpenWPM/jsons/wayback_js_ds.json', 'w') as fp:
    json.dump(wayback_url, fp, sort_keys=True, indent=4)


# API detecting url change
def url_archive(script_url):
    times = {'2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'}
    for time in times:
        response = requests.get(
            "https://web.archive.org/web/2019*/" + script_url + "*")
        print(response)


def js_content_download(script_url):
    try:
        response = requests.get(script_url, allow_redirects=True)
        if response.status_code == 200:
            hash_url = hash.md5(response.content).hexdigest()
            if hash_url not in wayback_url:
                path = os.path.join("/home/pooneh/PycharmProjects/OpenWPM/javascript_files", hash_url + ".js")
                open(path, 'wb').write(response.content)
                return hash_url
            return False
        return False
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


def wayback_changes_api():
    script_url = "https://web.archive.org/web/changes/https://www.kelete.com/statics/js/common.js"
    response = requests.get("https://web.archive.org/web/changes/" + script_url)
    print(response.content)


def test():
    url = "https://js.ad-score.com/score.min.js?pid=1000476#tid=&l1=&l2=&l3=&l4=&l5=www.weddingchicks.com&pub_domain=www.weddingchicks.com&ref=&utid=errorObtainingIdForProTMediaTag&cb=0.6062874534188464"
    record = []
    try:
        start = time.time()
        response = requests.get(
            "http://archive.org/wayback/available?url=" + url + "&timestamp=20100101")
        time.sleep(2)
        print(response.raise_for_status())
        if response.status_code == 200:
            # if not response.raise_for_status():
            response_json = response.json()
            if response_json['archived_snapshots'] != {}:
                if "201001" == response_json['archived_snapshots']['closest']['timestamp'][
                               0:6]:
                    hash = js_content_download(response_json['archived_snapshots']['closest']['url'][42:])
                    if hash:
                        'requestedDate', 'closestDate', 'URL'
                        wayback_url[hash] = {"requestedDate": response_json['timestamp'],
                                             "closestDate": response_json['archived_snapshots']['closest'][
                                                                'timestamp'][0:8],
                                             "url": response_json['archived_snapshots']['closest']['url'][42:]}
                        print("your req time: " + response_json['timestamp'], "my closest time: " +
                              response_json['archived_snapshots']['closest']['timestamp'][0:8])
        end = time.time()
        print(end - start)

    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)


availability_api()
# wayback_changes_api()
# test()
