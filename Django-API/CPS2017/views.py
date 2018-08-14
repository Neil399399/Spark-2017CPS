from django.shortcuts import render
from django.http import JsonResponse
from CPS2017 import sc
from CPS2017 import solr_server
from CPS2017.mllib.mutiClassification import mutiClassification_function
from CPS2017.mllib.mold import mold_function
import time
import json

# Create your views here.
def mutiClassification(request):
#----------------------------------------------------------------#
    if request.method == 'GET':
       start_time = time.time()
       try:
           id = request.GET['ID']
           method = request.GET['Method']
           print(id,method)
           # ----------------------------solr connect-------------------------------------------#
           solr_result = solr_server.search("id:{}".format(id))
           for solr_result in solr_result:
               vibration = format(solr_result['vibration'])
           input_data= json.loads(vibration)
           get_data_time = time.time() - start_time
           # ----------------------------spark connect-------------------------------------------#
           rdd = sc.parallelize(input_data)
           response_data = mutiClassification_function(rdd,method)
           response_message = "Success."
       except:
            response_message = "calculate error."
    else:
        response_message = "Please use GET method."

    Running_time = time.time() - start_time
    return JsonResponse({
                         "response_message": response_message,
                         "response_data": response_data,
                         "Running time": Running_time,
                         "Get data from solr time": get_data_time})


def mold(request):
    #----------------------------------------------------------------#
    if request.method == 'GET':
       start_time = time.time()
       try:
           id = request.GET['ID']
           method = request.GET['Method']
           print(id,method)
           # ----------------------------solr connect-------------------------------------------#
           solr_result = solr_server.search("id:{}".format(id))
           for solr_result in solr_result:
               vibration = format(solr_result['vibration'])
           input_data= json.loads(vibration)
           get_data_time = time.time() - start_time
           # ----------------------------spark connect-------------------------------------------#
           rdd = sc.parallelize(input_data)
           response_data = mold_function(rdd,method)
           response_message = "Success."
       except:
            response_message = "calculate error."
    else:
        response_message = "Please use GET method."

    Running_time = time.time() - start_time
    return JsonResponse({
                         "response_message": response_message,
                         "response_data": response_data,
                         "Running time": Running_time,
                         "Get data from solr time": get_data_time})
