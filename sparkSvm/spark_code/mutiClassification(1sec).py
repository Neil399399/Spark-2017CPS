# Create your tests here.
from time import time
import logging
import os
import math
import numpy as np
from pyspark import SparkContext, SparkConf
from pyspark.mllib.classification import LogisticRegressionModel
from pyspark.mllib.classification import SVMModel
from pyspark.mllib.regression import LabeledPoint
from utilities.spark_context_handler import SparkContextHandler


#setting OS environment
os.environ["PYSPARK_PYTHON"] = "python3"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python3"
logger = logging.getLogger("pyspark")
SparkContextHandler._master_ip = "10.14.24.101"
sc = SparkContextHandler.get_spark_sc()

# Model and Data Dir
firstLayerModel = "hdfs:///spark/Model/FNAL_1SecModel"
secondLayerModel = "hdfs:///spark/Model/FOAL_1SecModel"
thridLayerModel = "hdfs:///spark/Model/FTRL_1SecModel"
testData = "file:/home/spark/Documents/neil-git/dataset/oneBolt_rag/Test_1sec.txt"

#parse the data
def testparsePoint(line):
    values = [float(x) for x in line.split(",")]
    #return values
    return LabeledPoint(values[0],values[1:])

def TimeDomain(line):
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

def FrequencyDomain(line):
    try:
        values = [float(x) for x in line.split("\t")]
    except:
        values = [float(x) for x in line.split(",")]
    # change data used fft and calculate distance ----- root(a**2+b**2)
    newValue = [values[0]]
    complex = np.fft.fft(values[1:826])

    for i in range(0, len(complex)):
        distanceOfComplex = (complex[i].real ** 2 + complex[i].imag ** 2) ** 0.5
        newValue.append(distanceOfComplex)
    newValue.append(values[827])
    newValue.append(values[828])
    return LabeledPoint(newValue[0], newValue[1:])


# Start
startTime = time()
print("load testdata")
test = sc.textFile(testData)
testData = test.map(FrequencyDomain)

## first layer
print("load model")
Model = LogisticRegressionModel.load(sc,firstLayerModel)
print("First Prediction (Normal or unNormal)")
labelsAndPreds = testData.map(lambda p: (p.label, Model.predict(p.features),p.features))
temp = labelsAndPreds.filter(lambda p: p[1]==0)
### count
TotalAmount = float(testData.count())
normalAmount = labelsAndPreds.filter(lambda p: p[1]==1)
oneBoltAmount = labelsAndPreds.filter(lambda p: p[0]==1).count()
ragAmount = labelsAndPreds.filter(lambda p: p[0]==0).count()

## second layer
print("Second Prediction (oneBolt or other)")
Model2 = LogisticRegressionModel.load(sc,secondLayerModel)
temp2 = temp.map(lambda p: (p[0],Model2.predict(p[2]),p[2]))
### count
oneBoltResult = temp2.filter(lambda p: p[1]==1)

## third layer
print("third Prediction (twoBolt or rag)")
Model3 = LogisticRegressionModel.load(sc,thridLayerModel)
temp3 = temp2.filter(lambda p: p[1]==0).map(lambda p: (p[0],Model3.predict(p[2])))

### count
twoBoltResult = temp3.filter(lambda p: p[1]==1)
ragResult = temp3.filter(lambda p: p[0]==p[1]and p[1]==0)

#end
runTime = time()-startTime
print("TotalAmount:",TotalAmount)
print("oneBolt:",oneBoltAmount)
print("rag:",ragAmount)
print("normal result:",normalAmount.count())
print("oneBolt result:",oneBoltResult.count(),oneBoltResult.count()/oneBoltAmount)
print("twoBolt result:",twoBoltResult.count(),twoBoltResult.count()/TotalAmount)
print("rag result:",ragResult.count(),ragResult.count()/ragAmount)
print("Running Time:",runTime)


