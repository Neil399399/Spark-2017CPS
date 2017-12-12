from django.shortcuts import render
from django.http import JsonResponse
from hello.mllib.SVM import SVM_function
from utilities.spark_context_handler import SparkContextHandler
from pyspark import SparkContext, SparkConf
from pyspark.mllib.classification import SVMWithSGD
from pyspark.mllib.classification import SVMModel

import math
import numpy as np
# Create your views here.

CPS_TEST_SOLR_URL = "http://140.124.183.19:8983/solr/2017CPS/"





def SVM(request):
    response_code = 1
    response_message = ""
    response_data = None
#----------------------------------------------------------------#
    if request.method == 'GET':
       try:
           conf = SparkConf().setAppName('test').setMaster('local')
           sc = SparkContext(conf=conf)
           #InputData=request.POST['input']
           #SparkContextHandler._master_ip = "10.14.24.101"
           #sc = SparkContextHandler.get_spark_sc()

           #share dataset with parallelize or textfile
           #brocast_keys = sc.broadcast(keys)
           print("call data")
           rdd = sc.textFile("file:/home/spark/Downloads/sparkSvm/CPSdata20171120.csv")
           #rdd = sc.parallelize(InputData)
           print("call function")
           response_data = [SVM_function(rdd,sc)]
           print(response_data)
           response_code = 0
           response_message = "Success."
       except:
            response_message = "calculate error."
    else:
        response_message = "Please use POST method."
        SparkContextHandler.stop_spark_sc()
#----------------------------------------------------------------#
    return JsonResponse({"hello":"SVM Prediction",
                         "response_code": response_code,
                         "response_message": response_message,
                         "response_data": response_data})



   

   
