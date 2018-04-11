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
firstLayerModel = "hdfs:///spark/Model/FNA_1SecModel"
secondLayerModel = "hdfs:///spark/Model/FOA_1SecModel"
thridLayerModel = "hdfs:///spark/Model/FTR_1SecModel"
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

def InputLayer(originRDD,Model):
    Model1 = Model.load(sc,firstLayerModel)
    outputRDD = originRDD.map(lambda p: (p.label, Model1.predict(p.features),p.features))
    return outputRDD

def HiddenLayer(InputRDD,Model):
    Model2 = Model.load(sc,secondLayerModel)
    outputRDD = InputRDD.filter(lambda p: p[1]==0).map(lambda p: (p[0],Model2.predict(p[2]),p[2]))
    return outputRDD

def OutputLayer(InputRDD,Model):
    Model3 = Model.load(sc,thridLayerModel)
    outputRDD = InputRDD.filter(lambda p: p[1]==0).map(lambda p: (p[0],Model3.predict(p[2])))
    return outputRDD


# Start
startTime = time()
print("load testdata")
test = sc.textFile(testData)
testData = test.map(FrequencyDomain)

# count
TotalAmount = testData.count()

# run first layer
print("First Prediction (Normal or unNormal)")
first_output = InputLayer(testData,SVMModel)
normalAmount = first_output.filter(lambda p: p[1]==1).count()
oneBoltAmount = first_output.filter(lambda p: p[0]==1).count()
ragAmount = first_output.filter(lambda p: p[0]==0).count()

# run hidden1 layer
print("Second Prediction (oneBolt or other)")
second_output = HiddenLayer(first_output,SVMModel)
oneBoltResult = second_output.filter(lambda p: p[1]==1).count()

# run output layer
print("third Prediction (twoBolt or rag)")
final_output = OutputLayer(second_output,SVMModel)
twoBoltResult = final_output.filter(lambda p: p[1]==1).count()
ragResult = final_output.filter(lambda p: p[0]==p[1]and p[1]==0).count()

# end
runTime = time()-startTime
print("Total amount:",TotalAmount)
print("OneBolt amount:",oneBoltAmount)
print("Rag amount:",ragAmount)
## predicted
print("Normal prediction:",normalAmount)
print("OneBolt prediction:",oneBoltResult," Percent:",oneBoltResult*100/oneBoltAmount)
print("TwoBolt prediction:",twoBoltResult)
print("Rag prediction:",ragResult," Percent:",ragResult*100/ragAmount)
print("Running Time (sec):",runTime)


