from django.shortcuts import render
from django.http import JsonResponse
from CPS2017.mllib.mutiClassification import mutiClassification_function
from utilities.spark_context_handler import SparkContextHandler
import pysolr
import time
import json
from pyspark import SparkContext, SparkConf

# global
CPS_TEST_SOLR_URL = "http://140.124.183.37:8983/solr/2017CPS/"

# Create your views here.
def mutiClassification(request):
    response_code = 1
    response_message = ""
    response_data = None
#----------------------------------------------------------------#
    if request.method == 'GET':
       start_time = time.time()
       try:
           id = request.GET['ID']
           method = request.GET['Method']
           print(id,method)
           # ----------------------------solr connect-------------------------------------------#
           print("Get Solr data ...")
           solr_server = pysolr.Solr(CPS_TEST_SOLR_URL, timeout=10)
           solr_result = solr_server.search("id:{}".format(id))
           for solr_result in solr_result:
               vibration = format(solr_result['vibration'])
           input_data= json.loads(vibration)
           get_data_time = time.time() - start_time

           # ----------------------------spark connect-------------------------------------------#
           # SparkContextHandler._master_ip = "10.14.24.101"
           # sc = SparkContextHandler.get_spark_sc()
           conf = SparkConf().setAppName('test').setMaster('local')
           sc = SparkContext(conf=conf)
           rdd = sc.parallelize(input_data)
           response_data = mutiClassification_function(rdd,sc,method)
           response_message = "Success."
       except:
            response_message = "calculate error."
    else:
        response_message = "Please use GET method."
    SparkContextHandler.stop_spark_sc()
    Running_time = time.time() - start_time

    #----------------------------------------------------------------#
    return JsonResponse({
                         "response_message": response_message,
                         "response_data": response_data,
                         "Running time": Running_time,
                         "Get data from Solr time": get_data_time,
    })




   
