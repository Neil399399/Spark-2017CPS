from django.shortcuts import render
from django.http import JsonResponse
from CPS2017 import sc,logger_server
from CPS2017 import solr_server,Cloud_Motor_url,Cloud_WSN_url,Cloud_Predict_url,Om2m_url
from CPS2017.mllib.mutiClassification import mutiClassification_function,mutiClassification_function_module
import time
import json
import requests


def send_Om2m(Source, prediction):
    payload = '{\n\t\"m2m:cin\":\n\t{\n\t\t\"cnf\":\"message\",\n\t\t\"con\":\"{\\\"label\\\":'+prediction+',\\\"source\\\":'+str(Source)+'}\"\n\t}\n}'
    headers = {
        'Content-Type': "application/json;ty=4",
        'X-M2M-Origin': "admin:admin",
    }
    requests.post(Om2m_url, data=payload, headers=headers)

def send_Cloud(Source, prediction):
    response = '{"label":' + prediction + ',"source":' + Source + '}'
    requests.post(Cloud_Predict_url, data=response)


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

           # my_params = {'second': id}
           # response = requests.get(Cloud_Motor_url,params=my_params).json()
           # print(response[0])

           get_data_time = time.time() - start_time
           # ----------------------------spark connect-------------------------------------------#
           rdd = sc.parallelize(input_data)
           try:
               response_data = mutiClassification_function(rdd,method)
               # return prediction back to cloud DB.
               send_Cloud(id,response_data)
               send_Om2m(id, 'normal')
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
                         "timestamp": id,
                         "response_data": response_data,
                         "Running time": Running_time })

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
               # return prediction back to cloud DB.
               response = '{"label":' + response_data + ',"source":' + id + '}'
               requests.post(Cloud_Predict_url, data=response)
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
       # try:
        id = request.GET['ID']
        timeStamp = {'second': id}
        response = requests.get(Cloud_WSN_url,params=timeStamp).json()
        print(response)
       # except:
        response_message = "request error."
        # logger_server.warning('bad request')

        # send_Om2m(id,'normal')

    else:
        response_message = "Please use GET method."

    Running_time = time.time() - start_time
    return JsonResponse({})
