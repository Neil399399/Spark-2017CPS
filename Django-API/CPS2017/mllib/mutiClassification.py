# Model and Data Dir
import time
from CPS2017 import sc,logger_server
from CPS2017 import LR_First_Model,LR_Second_Model,LR_Third_Model
from CPS2017 import SVM_First_Model,SVM_Second_Model,SVM_Third_Model
from CPS2017 import Module_LR_First_Model,Module_LR_Second_Model,Module_LR_Third_Model
from CPS2017 import Module_SVM_First_Model,Module_SVM_Second_Model,Module_SVM_Third_Model
from CPS2017 import Random_Forest_Model,Module_Random_Forest_Model

def FFT(line):
    import numpy as np
    # change data used fft and calculate distance ----- root(a**2+b**2)
    newValue = []
    temp = line.collect()
    print(len(temp))
    complex = np.fft.fft(temp[0:1650])
    for i in range(0,825):
        distanceOfComplex = (complex[i].real ** 2 + complex[i].imag ** 2) ** 0.5
        newValue.append(distanceOfComplex)
    print(len(newValue))
    newValue.append(temp[1651])
    newValue.append(temp[1652])
    return newValue

def InputLayer(originRDD,Model):
    outputRDD = originRDD.map(lambda p: (Model.predict(p),p))
    Normal = outputRDD.filter(lambda p: p[0] == 0).count()
    if Normal != 0:
        return 'Normal'
    else:
        return 'unNormal'

def HiddenLayer(InputRDD,Model):
    outputRDD = InputRDD.filter(lambda p: p[0]==0).map(lambda p: (Model.predict(p[1]),p[1]))
    OneBolt = outputRDD.filter(lambda p: p[0] == 0).count()
    if OneBolt != 0:
        return 'OneBolt'
    else:
        return outputRDD

def OutputLayer(InputRDD,Model):
    outputRDD = InputRDD.filter(lambda p: p[0]==0).map(lambda p: Model.predict(p[1]))
    TwoBolt = outputRDD.filter(lambda p: p == 0).count()
    if TwoBolt != 0:
       return 'TwoBolt'
    else:
       return 'Rag'

def mutiClassification_function(rdd,method):
    output = FrequencyDomain(rdd)
    testData = sc.parallelize([output])
    # -----------------------Start predict.-------------------------------------#
    logger_server.info('prediction')
    start_time = time.time()
    if method == 'LogisticRegression':
        logger_server.info('First Predict.(Normal or unNormal)')
        first_output = InputLayer(testData, LR_First_Model)
        if first_output =='Normal':
            return 'Normal'
        else:
            logger_server.info('Second Predict.(oneBolt or other)')
            second_output = HiddenLayer(first_output, LR_Second_Model)
            if second_output == 'OneBolt':
                return 'OneBolt'
            else:
                logger_server.info('third Predict.(twoBolt or rag)')
                final_output = OutputLayer(second_output, LR_Third_Model)
                if final_output == 'TwoBolt':
                    return 'TwoBolt'
                else:
                    return 'Rag'

    elif method == 'SVM':
        logger_server.info('First Predict.(Normal or unNormal)')
        first_output = InputLayer(testData, SVM_First_Model)
        if first_output =='Normal':
            return 'Normal'
        else:
            return 'unNormal'
            # logger_server.info('Second Predict.(oneBolt or other)')
            # second_output = HiddenLayer(first_output, SVM_Second_Model)
            # if second_output == 'OneBolt':
            #     return 'OneBolt'
            # else:
            #     logger_server.info('third Predict.(twoBolt or rag)')
            #     final_output = OutputLayer(second_output, SVM_Third_Model)
            #     if final_output == 'TwoBolt':
            #         return 'TwoBolt'
            #     else:
            #         return 'Rag'

    elif method == 'random_forest':
        logger_server.info('do random forest.')
        for test in testData.collect():
            predict = Random_Forest_Model.predict(test)
            if predict == 0:
                return 'Normal'
            elif predict == 1:
                return 'OneBolt'
            elif predict == 2:
                return 'TwoBolt'
            elif predict == 3:
                return 'Rag'
    else:
        logger_server.warning('prediction failed')
        return "error"

def mutiClassification_function_module(rdd,method):
    output = FrequencyDomain(rdd)
    testData = sc.parallelize([output])
    # -----------------------Start predict.-------------------------------------#
    logger_server.info('prediction')
    start_time = time.time()
    if method == 'LogisticRegression':
        logger_server.info('First Predict.(Normal or unNormal)')
        first_output = InputLayer(testData, Module_LR_First_Model)
        if first_output =='Normal':
            return 'Normal'
        else:
            logger_server.info('Second Predict.(oneBolt or other)')
            second_output = HiddenLayer(first_output, Module_LR_Second_Model)
            if second_output == 'OneBolt':
                return 'OneBolt'
            else:
                logger_server.info('third Predict.(twoBolt or rag)')
                final_output = OutputLayer(second_output, Module_LR_Third_Model)
                if final_output == 'TwoBolt':
                    return 'TwoBolt'
                else:
                    return 'Rag'

    elif method == 'SVM':
        logger_server.info('First Predict.(Normal or unNormal)')
        first_output = InputLayer(testData, Module_SVM_First_Model)
        if first_output =='Normal':
            return 'Normal'
        else:
            logger_server.info('Second Predict.(oneBolt or other)')
            second_output = HiddenLayer(first_output, Module_SVM_Second_Model)
            if second_output == 'OneBolt':
                return 'OneBolt'
            else:
                logger_server.info('third Predict.(twoBolt or rag)')
                final_output = OutputLayer(second_output, Module_SVM_Third_Model)
                if final_output == 'TwoBolt':
                    return 'TwoBolt'
                else:
                    return 'Rag'

    elif method == 'random_forest':
        logger_server.info('do random forest.')
        for test in testData.collect():
            predict = Module_Random_Forest_Model.predict(test)
            if predict == 0:
                return 'Normal'
            elif predict == 1:
                return 'OneBolt'
            elif predict == 2:
                return 'TwoBolt'
            elif predict == 3:
                return 'Rag'
    else:
        logger_server.warning('prediction failed')
        return "error"

def environmental_threshold(environmental_info):
    return True
