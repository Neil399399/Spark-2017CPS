# -*- coding: utf-8 -*-
import csv
import io
import re
import pysolr
import sys

reload(sys)
sys.setdefaultencoding('utf8')

solr = pysolr.Solr('http://localhost:8983/solr/2017CPS', timeout=10)


with open('imdbtrain.csv', 'r') as csvfile:
     Train = [list(map(float,rec)) for rec in csv.reader(csvfile, delimiter=',')]



try:
    solr.add([
        {
            "id": 1,
            "indoor_temperature":20.333,
            "outdoor_temperature":25.142,
            "vibration":[9.723722991,6.219359199,1.563460588,9.06489614,6.219359199,1.457528959]
        },
    ])
except:
    print("error")