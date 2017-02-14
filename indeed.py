import csv
# from indeed import IndeedClient
import os
import requests
import json
import math
from bs4 import BeautifulSoup
import pandas as pd
import markov
import re


treat = os.environ["PUB_ID"]


# client = IndeedClient(publisher = PUB_ID)
# search_response = client.search(**params)
# print search_response
URL = "http://api.indeed.com/ads/apisearch?"
# publisher=1321797817350622&q=junior+software+engineer&l=San+Francisco+Bay+Area%2C+CA&radius=25&v=2&format=json"
# https://www.indeed.com/jobs?q=junior+or+entry-level+or+web+or+software+or+engineer+or+developer+title%3A%28software+or+engineer+or+web+or+developer+or+software+or+developer%2C+-senior%2C+-mid-level%2C+-lead%2C+-principle%29&l=San+Francisco+Bay+Area%2C+CA&radius=25&start=10

params = {
    'publisher' : treat,
    'q' : "junior or entry-level or software or web or engineer or developer or intern title:(junior or software or enigneer or web or developer, -Senior, -Sr., -mid-level, -Lead, -Principle, -Front End, -Java)",
    'l' : "san francisco bay area, CA",
    'userip' : "192.168.1.165",
    'useragent' : "Chrome/55.0.2883.95",
    'v' : 2,
    'format' : 'json',
    'limit' : 25
}

response = requests.get(URL, params=params)
print response.url
total_results = response.json()['totalResults']
total_pages = math.ceil(int(response.json()['totalResults'])/25.)
print total_results
print total_pages
# print int(response.json()['totalResults'])/25.
print 

csv_file = open("indeed_job_apps.csv", "a") 


fieldnames = ["jobtitle","city","state","country",
"formattedLocation","source","date","snippet","url","onmousedown",
"latitude","longitude","jobkey","sponsored","expired",
"formattedLocationFull","formattedRelativeTime","stations","indeedApply","job_summary","company","markov_text"]
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
        #for each result get the job url job summary
        response_job = requests.get(r['url'])
        soup = BeautifulSoup(response_job.text, 'html.parser')
        desc2 = soup.find('span', attrs={'id': 'job_summary'}).get_text()
        desc2 = desc2.encode('ascii', 'ignore').decode('utf-8')
        # print desc2

        # print desc2.encode('utf-8')
        # append each result to pd and each job summary to the second to last column
        df = df.append(r, ignore_index=True)
        df.iloc[i,-2] = desc2
        
        # desc = desc2.split()
        # marky = ' '.join(desc)
        # print desc
        marky = desc2.strip('\n')
        marky = re.split("[.,:;!?]", marky)
        marky = ' '.join(marky)
        marky = re.split("([A-Z][^A-Z]*)", marky)
        marky = ' '.join(marky)
        chains = markov.make_chains(str(marky))
        text = markov.make_text(chains)
        df.iloc[i,-1] = text
        i += 1
        


        # writer.writerow(dict((k, v.encode('utf-8') if type(v) is unicode else v) for k, v in r.iteritems()))
        
print df
# csv_file.close()








