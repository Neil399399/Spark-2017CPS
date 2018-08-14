import time
from CPS2017 import sc
from CPS2017 import mold_Model


def FFT(line):
    import numpy as np
    # change data used fft and calculate distance ----- root(a**2+b**2)
    newValue = []
    temp = line.collect()
    complex = np.fft.fft(temp[0:824])
    for i in range(0, len(complex)):
        distanceOfComplex = (complex[i].real ** 2 + complex[i].imag ** 2) ** 0.5
        newValue.append(distanceOfComplex)
    newValue.append(temp[824])
    newValue.append(temp[824])
    return newValue

def InputLayer(originRDD,Model):
    outputRDD = originRDD.map(lambda p: (Model.predict(p),p))
    Normal = outputRDD.filter(lambda p: p[0] == 1).count()
    if Normal != 0:
        return 'Normal'
    else:
        return 'abNormal'


def mold_function(rdd,method):
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
        output = InputLayer(testData, mold_Model)
        print('Predict time:', time.time() - start_time)
        return output

    elif method == 'SVM':
        print("First Predict ... (Normal or unNormal)")
        output = InputLayer(testData, mold_Model)
        print('Predict time:', time.time() - start_time)
        return output
    else:
        return "error"