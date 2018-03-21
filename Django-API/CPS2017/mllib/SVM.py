def TimeDomain(rdd):
    import math
    Max = rdd.max()
    Min = rdd.min()
    Mean = rdd.mean()
    #RMS---root of (sum(Xi-average)**2/X)
    RMSfractions=rdd.map(lambda x: (x-Mean)**2).sum()
    RMS = math.pow(RMSfractions/1000,0.5)
    #CF---Max/RMS
    CF  = Max/RMS
    #SK---(sum(Xi-average)**3 /x /RMS**3
    SKfractions=rdd.map(lambda x: (x-Mean)**3).sum()
    SK = SKfractions/1000/(RMS**3)
    #K---(sum(Xi-average)**4 /x /RMS**4
    Kfractions = rdd.map(lambda x: (x - Mean) ** 4).sum()
    K = Kfractions / 1000 / (RMS ** 4)

    newValue=[Max,Min,RMS,CF,SK,K]
    
    return newValue

def frequencyDomain(rdd):
    import numpy as np
    #change data used fft and calculate distance ----- root(a**2+b**2)
    newValue = []
    complex = np.fft.fft(rdd.collect())
    for i in range(0,len(complex)):
        distanceOfComplex = (complex[i].real**2+complex[i].imag**2)**0.5
        newValue.append(distanceOfComplex)

    return newValue


#spark code
#------------------------------------------------------------#
def SVM_function(rdd,sc,method):
    #method
    from pyspark.mllib.classification import SVMModel
    print("rdd map")
    if method =='TimeDomain':
        output = TimeDomain(rdd)
        testData = sc.parallelize([output])

    if method =='FrequencyDomain':
        output=frequencyDomain(rdd)
        testData=sc.parallelize([output])

    
    #load model
    print("load model")
    Model = SVMModel.load(sc,"hdfs:///home/spark/Desktop/"+method+"Model")
#------------------------------------------------------------#
    #input data and prediction
    print("labelsAndPreds")
    labelsAndPreds = Model.predict(testData)
    return labelsAndPreds.collect()






   
