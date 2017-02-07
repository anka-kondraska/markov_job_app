import csv
# from indeed import IndeedClient
import os
import requests
import json
import math
from bs4 import BeautifulSoup
import pandas as pd


treat = os.environ["PUB_ID"]


# client = IndeedClient(publisher = PUB_ID)
# search_response = client.search(**params)
# print search_response
URL = "http://api.indeed.com/ads/apisearch?"
# publisher=1321797817350622&q=junior+software+engineer&l=San+Francisco+Bay+Area%2C+CA&radius=25&v=2&format=json"

params = {
    'publisher' : treat,
    'q' : "junior software developer OR intern",
    'l' : "san francisco bay area, CA",
    'userip' : "192.168.1.165",
    'useragent' : "Chrome/55.0.2883.95",
    'v' : 2,
    'format' : 'json',
    'limit' : 25
}

response = requests.get(URL, params=params)
total_results = response.json()['totalResults']
total_pages = math.ceil(int(response.json()['totalResults'])/25.)
print total_results
print total_pages
# print int(response.json()['totalResults'])/25.
print 

csv_file = open("indeed_job_apps.csv", "a") 


fieldnames = ["jobtitle","compan","city","state","country",
"formattedLocation","source","date","snippet","url","onmousedown",
"latitude","longitude","jobkey","sponsored","expired",
"formattedLocationFull","formattedRelativeTime","stations","indeedApply","job_summary"]
writer = csv.DictWriter(csv_file, dialect='excel', fieldnames=fieldnames)
writer.writeheader()

df = pd.DataFrame(columns=fieldnames)
i = 0
# going through all pages
for page in xrange(0, int(total_pages)):
    # print "PAGE",response.json()['pageNumber']
    response_pages = requests.get(response.url, params={"page":page})
    print "PAGE",page
    # results per page
    for r in response_pages.json()['results']:
        # print r
        response_job = requests.get(r['url'])
        soup = BeautifulSoup(response_job.text, 'html.parser')
        desc2 = soup.find('span', attrs={'id': 'job_summary'}).get_text()
        desc2 = desc2.encode('utf-8')
        # print desc2

        # print desc2.encode('utf-8')
        df = df.append(r, ignore_index=True)
        df.iloc[i,-2] = desc2
        i += 1
        # print df.head()

        # writer.writerow(dict((k, v.encode('utf-8') if type(v) is unicode else v) for k, v in r.iteritems()))
        
print df.head()
csv_file.close()








