# Model and Data Dir
import time
from CPS2017 import sc
from CPS2017 import LR_First_Model,LR_Second_Model,LR_Third_Model
from CPS2017 import SVM_First_Model,SVM_Second_Model,SVM_Third_Model


def FFT(line):
    import numpy as np
    # change data used fft and calculate distance ----- root(a**2+b**2)
    newValue = []
    temp = line.collect()
    complex = np.fft.fft(temp[0:825])
    for i in range(0, len(complex)):
        distanceOfComplex = (complex[i].real ** 2 + complex[i].imag ** 2) ** 0.5
        newValue.append(distanceOfComplex)
    newValue.append(temp[826])
    newValue.append(temp[827])
    return newValue

def InputLayer(originRDD,Model):
    outputRDD = originRDD.map(lambda p: (Model.predict(p),p))
    Normal = outputRDD.filter(lambda p: p[0] == 1).count()
    if Normal != 0:
        return 'Normal'
    else:
        return outputRDD

def HiddenLayer(InputRDD,Model):
    outputRDD = InputRDD.filter(lambda p: p[0]==0).map(lambda p: (Model.predict(p[1]),p[1]))
    OneBolt = outputRDD.filter(lambda p: p[0] == 1).count()
    if OneBolt != 0:
        return 'OneBolt'
    else:
        return outputRDD

def OutputLayer(InputRDD,Model):
    outputRDD = InputRDD.filter(lambda p: p[0]==0).map(lambda p: Model.predict(p[1]))
    TwoBolt = outputRDD.filter(lambda p: p == 1).count()
    if TwoBolt != 0:
       return 'TwoBolt'
    else:
       return 'Rag'

def mutiClassification_function(rdd,method):
    print("Start do fft parser ...")
    Start_time = time.time()
    output = FFT(rdd)
    testData = sc.parallelize([output])
    print('fft_parser_time:',time.time() - Start_time)

    # -----------------------Start predict.-------------------------------------#
    print("Start predict ...")
    start_time = time.time()
    if method == 'LogisticRegression':
        print("First Predict ... (Normal or unNormal)")
        first_output = InputLayer(testData, LR_First_Model)
        if first_output =='Normal':
            print('Predict time:', time.time() - start_time)
            return 'Normal'
        else:
            print("Second Predict ... (oneBolt or other)")
            second_output = HiddenLayer(first_output, LR_Second_Model)
            if second_output == 'OneBolt':
                print('Predict time:', time.time() - start_time)
                return 'OneBolt'
            else:
                print("third Predict ... (twoBolt or rag)")
                final_output = OutputLayer(second_output, LR_Third_Model)
                if final_output == 'TwoBolt':
                    print('Predict time:', time.time() - start_time)
                    return 'TwoBolt'
                else:
                    print('Predict time:', time.time() - start_time)
                    return 'Rag'

    elif method == 'SVM':
        print("First Predict ... (Normal or unNormal)")
        first_output = InputLayer(testData, SVM_First_Model)
        if first_output =='Normal':
            print('Predict time:', time.time() - start_time)
            return 'Normal'
        else:
            print("Second Predict ... (oneBolt or other)")
            second_output = HiddenLayer(first_output, SVM_Second_Model)
            if second_output == 'OneBolt':
                print('Predict time:', time.time() - start_time)
                return 'OneBolt'
            else:
                print("third Predict ... (twoBolt or rag)")
                final_output = OutputLayer(second_output, SVM_Third_Model)
                if final_output == 'TwoBolt':
                    print('Predict time:', time.time() - start_time)
                    return 'TwoBolt'
                else:
                    print('Predict time:', time.time() - start_time)
                    return 'Rag'
    else:
        return "error"