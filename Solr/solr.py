# -*- coding: utf-8 -*-
import csv
import io
import re
import pysolr
import sys
import json

reload(sys)
sys.setdefaultencoding('utf8')

solr = pysolr.Solr('http://140.124.183.37:8983/solr/2017CPS', timeout=10)


#parse the data
# with open ("data/test(1).txt","r") as csvfile:
#     Data= [list(map(float,rec)) for rec in csv.reader(csvfile,delimiter=",")]
        
# add data in solr
# for i in range (0,len(Data)):
#     try:
#         solr.add([
#             {
#                 "id": i,
#                 "indoor_temperature":20.333,
#                 "outdoor_temperature":25.142,
#                 "vibration": Data[i][1:]
#             },
#         ])
#     except:
#         print("error")


# select solr data
result=solr.search('id:5')
for result in result:
    vibration=format(result['vibration'])


json = json.loads(vibration)
a=json.split(",")
print(len(a))
print(a)
