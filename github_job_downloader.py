"""
This file is used to download job infomation from jobs.github.com and save it into the file gitHubJobDescriptions.xls
This program only needs to be run during initial set up and when you want to update the job information that you have.
Currently takes quite a while to run, no overly easy way to interact with the tradeMe API it seems.
NOTE: Uses python 3.5, since the web libraries are easier to use.

Harrigan Davenport
"""
import re
import xlwt
from pip._vendor import requests

def cleanhtml(raw_html):
    """https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string"""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


descriptionSet = set()

for pageCount in range(0, 4):
    response = requests.get("https://jobs.github.com/positions.json?page=" + str(pageCount))
    print(response.json())
    for i in response.json():
        descriptionSet.add(cleanhtml(i['description']))

for i in descriptionSet:
    print(i)
    print('###########################################################')

workbook = xlwt.Workbook(encoding="utf-8")
sheet1 = workbook.add_sheet("Sheet 1")
row = 0

for description in descriptionSet:
    sheet1.write(row, 1, description)
    row += 1

workbook.save('Job Descriptions/githubJobDescriptions.xls')


