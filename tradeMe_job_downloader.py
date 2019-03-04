"""
This file is used to download job infomation from trademe.co.nz and save it into the file trademeJobDescriptions.xls
This program only needs to be run during initial set up and when you want to update the job infomation that you have.
Currently takes quite a while to run, no overly easy way to interact with the tradeMe API it seems.
NOTE: Uses python 3.5, since the web libraries are easier to use.

Harrigan Davenport
"""
import time
import xlwt
from pip._vendor import requests
consumer_key = '1B9870060A503CC40B8D38E73D446090'
consumer_secret = '199C122B7ED65222B17FD01799C663A3'
signature = consumer_secret + "%26"
signature.encode('utf-8')
print(int(time.time()))
headers = {"Authorization": "OAuth callback=https%3A%2F%2Fwww.website-tm-access.co.nz%2Ftrademe-callback, oauth_consumer_key=" +consumer_key +', oauth_version=1.0, + oauth_timestamp=' + str(int(time.time())) + ",oauth_nonce = 7O3kEe, oauth_signature_method=PLAINTEXT, oauth_signature=" + signature}

##This request calls to get all jobs from the categories Programming and Development, Web Design, Testing and Architects
response = requests.get("https://api.trademe.co.nz/v1/Search/Jobs.json?category=5119%2C%205123%2C%205124%2C%205113&rows=500", headers=headers)
id_list = []
print(response.json()['List'])
for i in response.json()['List']:
    id_list.append(i['ListingId'])
    print('id', i['ListingId'])

workbook = xlwt.Workbook(encoding="utf-8")
sheet1 = workbook.add_sheet("Sheet 1")
row = 0

for id in id_list:
    try:
        response = requests.get("https://api.trademe.co.nz/v1/Listings/" + str(id) +".json?", headers=headers)
        sheet1.write(row, 0, id)
        sheet1.write(row, 1, response.json()['Body'])
        workbook.save('Job Descriptions/tradeMeJobDescriptions.xls')
    except KeyError:
        pass
    row += 1
    # print(response.json()['Body'])

workbook.save('Job Descriptions/tradeMeJobDescriptions.xls')

