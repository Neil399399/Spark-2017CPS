from django.shortcuts import render
from django.http import JsonResponse
from CPS2017 import sc,logger_server
from CPS2017 import solr_server
from CPS2017.mllib.mutiClassification import mutiClassification_function,mutiClassification_function_module
import time
import json

# Create your views here.
def mutiClassification_motor(request):
    if request.method == 'GET':
       start_time = time.time()
       try:
           id = request.GET['ID']
           method = request.GET['Method']
           # ----------------------------solr connect-------------------------------------------#
           solr_result = solr_server.search("id:{}".format(id))
           for solr_result in solr_result:
               vibration = format(solr_result['vibration'])
           input_data= json.loads(vibration)
           get_data_time = time.time() - start_time
           # ----------------------------spark connect-------------------------------------------#
           rdd = sc.parallelize(input_data)
           try:
               response_data = mutiClassification_function(rdd,method)
               response_message = "Success."
               if response_data == 'error':
                   response_message = "error."
           except:
               response_message = "prediction error."
               logger_server.warning('prediction error')
       except:
            response_message = "request error."
            logger_server.warning('bad request')
    else:
        response_message = "Please use GET method."

    Running_time = time.time() - start_time
    return JsonResponse({
                         "response_message": response_message,
                         "response_data": response_data,
                         "Running time": Running_time,
                         "Get data from solr time": get_data_time})

def mutiClassification_module(request):
    if request.method == 'GET':
       start_time = time.time()
       try:
           id = request.GET['ID']
           method = request.GET['Method']
           # ----------------------------solr connect-------------------------------------------#
           solr_result = solr_server.search("id:{}".format(id))
           for solr_result in solr_result:
               vibration = format(solr_result['vibration'])
           input_data= json.loads(vibration)
           get_data_time = time.time() - start_time
           # ----------------------------spark connect-------------------------------------------#
           rdd = sc.parallelize(input_data)
           try:
               response_data = mutiClassification_function_module(rdd,method)
               response_message = "Success."
               if response_data == 'error':
                   response_message = "error."
           except:
               response_message = "prediction error."
               logger_server.warning('prediction error')
       except:
            response_message = "request error."
            logger_server.warning('bad request')
    else:
        response_message = "Please use GET method."

    Running_time = time.time() - start_time
    return JsonResponse({
                         "response_message": response_message,
                         "response_data": response_data,
                         "Running time": Running_time,
                         "Get data from solr time": get_data_time})

def environmental_information(request):
    if request.method == 'GET':
       start_time = time.time()
       try:
           id = request.GET['ID']
           method = request.GET['Method']
       except:
            response_message = "request error."
            logger_server.warning('bad request')
    else:
        response_message = "Please use GET method."

    Running_time = time.time() - start_time
    return JsonResponse({})