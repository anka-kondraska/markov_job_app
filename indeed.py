import csv
# from indeed import IndeedClient
import os
import requests
import json
import math

treat = os.environ["PUB_ID"]


# client = IndeedClient(publisher = PUB_ID)
# search_response = client.search(**params)
# print search_response
URL = "http://api.indeed.com/ads/apisearch?"
# publisher=1321797817350622&q=junior+software+engineer&l=San+Francisco+Bay+Area%2C+CA&radius=25&v=2&format=json"

params = {
    'publisher' : treat,
    'q' : "junior software engineer python",
    'l' : "san francisco",
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
print int(response.json()['totalResults'])/25.
print response.json()['pageNumber']
print 
csv_file = open("indeed_job_apps.csv", "w") 

fieldnames = ["jobtitle","company","city","state","country",
"formattedLocation","source","date","snippet","url","onmousedown",
"latitude","longitude","jobkey","sponsored","expired",
"formattedLocationFull","formattedRelativeTime","stations","indeedApply"]
writer = csv.DictWriter(csv_file, dialect='excel', fieldnames=fieldnames)
writer.writeheader()
for page in xrange(0, int(total_pages)):
    response_pages = requests.get(response.url, params={"page":page})
    print response_pages

    for r in response_pages.json()['results']:
        writer.writerow(dict((k, v.encode('utf-8') if type(v) is unicode else v) for k, v in r.iteritems()))

csv_file.close()








