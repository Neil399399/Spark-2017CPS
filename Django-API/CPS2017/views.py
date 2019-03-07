from django.shortcuts import render
from django.http import JsonResponse
from CPS2017 import sc,logger_server
from CPS2017 import solr_server,Cloud_Motor_url,Cloud_punch_url,Om2m_url_Motor,Om2m_url_Punch
from CPS2017.mllib.mutiClassification import mutiClassification_function,mutiClassification_function_punch
import json
import requests
import re
import ast


def send_Om2m(url, Source, prediction):
    payload = '{\n\t\"m2m:cin\":\n\t{\n\t\t\"cnf\":\"message\",\n\t\t\"con\":\"{\\\"label\\\":\\\"'+prediction+'\\\",\\\"source\\\":'+str(Source)+'}\"\n\t}\n}'
    headers = {
        'Content-Type': "application/json;ty=4",
        'X-M2M-Origin': "admin:admin",
    }
    requests.post(url, data=payload, headers=headers)

def parser_inputData(string):
    inputData = []
    temp = re.split(r'[,]', string)
    for str in temp :
         b = str.replace("[","").replace("]", "")
         inputData.append(float(b))
    return inputData

def Response(ID,Response_data,Respose_message):
    return JsonResponse({
                         "response_message": Respose_message,
                         "timeStamp": ID,
                         "prediction": Response_data})

# Create your views here.
def mutiClassification_motor(request):
    if request.method == 'GET':
        response_data = "None"
        id = request.GET['ID']
        method = request.GET['Method']
        try:
            my_params = {'second': id}
            response = requests.get(Cloud_Motor_url,params=my_params).json()
        except:
            response_message = "request error."
            logger_server.warning('bad request')
            return Response(id, response_data, response_message)

        input_data= parser_inputData(response[0]['Msg'])
        try:
            response_data = mutiClassification_function(input_data,method)
            response_message = "Success."
            logger_server.info('timestamp: %s'%id)
            logger_server.info('Result: %s'%response_data)
            print('')
            # return prediction back to cloud DB.
            send_Om2m(Om2m_url_Motor, id, response_data)
        except:
               response_message = "prediction error."
               logger_server.warning('prediction error')
    else:
        response_message = "Please use GET method."
    return Response(id,response_data,response_message)


def mutiClassification_punch(request):
    if request.method == 'GET':
        response_data = "None"
        id = request.GET['ID']
        method = request.GET['Method']
        try:
            my_params = {'second': id}
            response = requests.get(Cloud_punch_url,params=my_params).json()
        except:
            response_message = "request error."
            logger_server.warning('bad request')
            return Response(id, response_data, response_message)
        
        input_data= response[0]['Msg']
        # pvdf1,pvdf2,pvdf3 are in dictionary.
        dictionary = ast.literal_eval(input_data)
        try:
            response_data = mutiClassification_function_punch(dictionary,method)
            response_message = "Success."
            logger_server.info('timestamp: %s'%id)
            logger_server.info('Result: %s'%response_data)
            print('')            # return prediction back to cloud DB.
            send_Om2m(Om2m_url_Punch, id, response_data)
        except:
               response_message = "prediction error."
               logger_server.warning('prediction error')
    else:
        response_message = "Please use GET method."
    return Response(id,response_data,response_message)
