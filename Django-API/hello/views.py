from django.shortcuts import render
from django.http import JsonResponse
from hello.mllib.SVM import SVM_function
from utilities.spark_context_handler import SparkContextHandler
from pyspark import SparkContext, SparkConf

import pysolr
import json
# Create your views here.

CPS_TEST_SOLR_URL = "http://140.124.183.37:8983/solr/2017CPS/"

def SVM(request):
    response_code = 1
    response_message = ""
    response_data = None
#----------------------------------------------------------------#
    if request.method == 'POST':
       try:
           id = request.POST['ID']
           method = request.POST['Method']
           # ----------------------------solr connect-------------------------------------------#
           print("solr connecct")
           solr_server = pysolr.Solr(CPS_TEST_SOLR_URL, timeout=10)
           solr_result = solr_server.search("id:{}".format(id))
           for solr_result in solr_result:
               vibration = format(solr_result['vibration'])
           a = json.loads(vibration)

           # ----------------------------spark connect-------------------------------------------#
           #conf = SparkConf().setAppName('test').setMaster('local')
           #sc = SparkContext(conf=conf)
           SparkContextHandler._master_ip = "10.14.24.101"
           sc = SparkContextHandler.get_spark_sc()
           #share dataset with parallelize or textfile
           #brocast_keys = sc.broadcast(keys)
           print("call data")
           rdd = sc.parallelize(a)
           #rdd = sc.parallelize(InputData)
           print("call function")
           response_data = SVM_function(rdd,sc,method)
           response_message = "Success."
           response_code = 0
       except:
            response_message = "calculate error."
    else:
        response_message = "Please use POST method."
        response_code = 0
    SparkContextHandler.stop_spark_sc()
#----------------------------------------------------------------#
    return JsonResponse({"response_code":response_code,
                         "response_message": response_message,
                         "response_data": response_data})



   

   
