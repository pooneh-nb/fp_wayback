import sqlite3 as lite
from fuzzywuzzy import fuzz
import pandas as pd

def create_connection(db_file):
    # creat a database connection to SQLite database
    # input: address to the database
    #output: connection object
    conn = None
    try:
        conn = lite.connect(db_file)
    except Error as e:
        print(e)
    return conn

database_vanilla = "/media/pooneh/Pouneh/Desktop/Summer/shafiq/OpenWPM/OpenWPM/datasets/250-vanila/250-vanilla-crawl-data.sqlite"
database_adBlocked = "/media/pooneh/Pouneh/Desktop/Summer/shafiq/OpenWPM/OpenWPM/datasets/250-adblocked/250-adblocked-crawl-data.sqlite"
# create a database connection
conn = create_connection(database_vanilla)
conn2 = create_connection(database_adBlocked)

DF_vanilla = pd.DataFrame(columns=['visit_id', 'url'])
DF_blocked = pd.DataFrame(columns=['visit_id', 'url'])

# vanilla
vanila =0
cur = conn.cursor()
cur.execute("SELECT visit_id, url FROM http_requests")
rows = cur.fetchall()
DF_vanilla = pd.DataFrame(rows, columns=['visit_id', 'url'])
print(DF_vanilla.head(10))
for url in DF_vanilla['url']:
    if (fuzz.partial_ratio('google-analytics',url)>70):
        print(url)
        vanila+=1
print("vanila")
print(vanila)

# adblocker
ad=0
cur2 = conn2.cursor()
cur2.execute("SELECT visit_id, url FROM http_requests")
rows2 = cur2.fetchall()
DF_blocked = pd.DataFrame(rows2, columns=['visit_id', 'url'])
for url2 in DF_blocked['url']:
    if (fuzz.partial_ratio('google-analytics',url2)>70):
        print(url)
        ad+=1
print("adblocker")
print(ad)