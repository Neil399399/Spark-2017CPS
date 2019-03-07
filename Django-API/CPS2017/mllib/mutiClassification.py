# Model and Data Dir
import time
from CPS2017 import sc,logger_server
from CPS2017 import LR_First_Model,LR_Second_Model,LR_Third_Model
from CPS2017 import SVM_First_Model,SVM_Second_Model,SVM_Third_Model
# from CPS2017 import Mold_LR_First_Model,Mold_LR_Second_Model,Mold_LR_Third_Model
from CPS2017 import Mold_SVM_First_Model
from CPS2017 import Random_Forest_Model,Mold_Random_Forest_Model
from pyspark.mllib.regression import LabeledPoint

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


def mutiClassification_function(testData,method):
    # -----------------------Start predict.-------------------------------------#
    logger_server.info('prediction')
    start_time = time.time()
    if method == 'LogisticRegression':
        rdd = sc.parallelize(testData)
        logger_server.info('First Predict.(Normal or unNormal)')
        first_output = InputLayer(rdd, LR_First_Model)
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
        rdd = sc.parallelize(testData)
        logger_server.info('First Predict.(Normal or unNormal)')
        first_output = InputLayer(rdd, SVM_First_Model)
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
        logger_server.info('do punch prediction.')
        predict = Random_Forest_Model.predict(testData)
        if predict == 0:
            return 'Normal'
        elif predict == 1:
            return 'OneBolt'
        elif predict == 2:
            return 'TwoBolt'
        elif predict == 3:
            return 'rag'
    else:
        logger_server.warning('prediction failed')
        return "error"

def mutiClassification_function_punch(dictionary,method):
    # -----------------------Start predict.-------------------------------------#
    logger_server.info('prediction')
    # split three feature.
    pvdf1 = dictionary['pvdf1']
    pvdf2 = dictionary['pvdf2']
    pvdf3 = dictionary['pvdf3']

    if method == 'random_forest':
        logger_server.info('do random forest.')
        predict = Mold_Random_Forest_Model.predict(pvdf2)
        if predict == 0:
            return 'stop'
        else:
            logger_server.info('(empty punch or puch)')
            rdd = sc.parallelize([pvdf2])
            first_output = InputLayer(rdd, Mold_SVM_First_Model)
            if first_output == 'Normal':
                return 'punch'
            else:
                return 'empty_punch'
    else:
        logger_server.warning('prediction failed')
        return "error"


