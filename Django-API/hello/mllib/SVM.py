def TimeDomain(line):
    import math
    try:
       values = [float(x) for x in line.split("\t")]
    except:
       values = [float(x) for x in line.split(",")]
    #Max
    Max = max(values[0:])
    #Min
    Min = min(values[0:])

    #Average   range-1 because of label
    Sum = 0
    for i in range(0,len(values)):
        Sum = Sum + values[i]
    Average = Sum / len(values[0:])

    #RMS---root of (sum(Xi-average)**2/X)
    RMSSum = 0
    for i in range(0,len(values)):
        RMSSum = RMSSum+(values[i]-Average)**2
    RMS=math.pow(RMSSum/len(values[0:]),0.5)

    #CF---Max/RMS
    CF = Max/RMS

    #SK---(sum(Xi-average)**3 /x /RMS**3
    SKSum = 0
    for i in range(0,len(values)):
        SKSum = SKSum+(values[i]-Average)**3
    SK= SKSum/len(values[0:])/RMS**3

    #K---(sum(Xi-average)**4 /x /RMS**4
    KSum = 0
    for i in range(0, len(values)):
        KSum = KSum + (values[i] - Average) ** 4
    K = KSum / len(values[0:]) / RMS ** 4

    newValue=[Max,Min,RMS,CF,SK,K]
    return newValue

def frequencyDomain(line):
    import numpy as np
    try:
       values = [float(x) for x in line.split("\t")]
    except:
       values = [float(x) for x in line.split(",")]
    #change data used fft and calculate distance ----- root(a**2+b**2)
    newValue = []
    complex = np.fft.fft(values[0:])

    for i in range(0,len(complex)):
        distanceOfComplex = (complex[i].real**2+complex[i].imag**2)**0.5
        newValue.append(distanceOfComplex)

    return newValue


#spark code
#------------------------------------------------------------#
def SVM_function(rdd,sc):
    #method
    from pyspark.mllib.classification import SVMModel
    print("rdd map")
    testData = rdd.map(TimeDomain)
    print(testData.collect())
    #load model
    print("load model")
    try:
        Model = SVMModel.load(sc,"file:///home/spark/Desktop/TimeDomainModel")
#------------------------------------------------------------#
    #input data and prediction
        print("labelsAndPreds")
        labelsAndPreds = Model.predict(testData)
        return labelsAndPreds.collect()
    except:
        return "error"






   
