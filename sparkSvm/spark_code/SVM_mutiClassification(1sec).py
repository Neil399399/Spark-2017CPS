# Create your tests here.
from time import time
import logging
import os
import math
import numpy as np
from pyspark import SparkContext, SparkConf
from pyspark.mllib.classification import SVMWithSGD
from pyspark.mllib.classification import SVMModel
from pyspark.mllib.regression import LabeledPoint
from utilities.spark_context_handler import SparkContextHandler


#setting OS environment
os.environ["PYSPARK_PYTHON"] = "python3"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python3"
logger = logging.getLogger("pyspark")

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
SparkContextHandler._master_ip = "10.14.24.101"
sc = SparkContextHandler.get_spark_sc()
#------------------------------------------------------------#
startTime = time()
#------------------------------------------------------------#\
print("load testdata")
test = sc.textFile("file:/home/spark/Documents/neil-git/dataset/oneBolt_rag/Test_1sec.txt")
testData = test.map(FrequencyDomain)
#------------------------------------------------------------#
print("load model")
Model = SVMModel.load(sc,"hdfs:////spark/Model/FNA_1SecModel")
print("First Prediction (Normal or unNormal)")
# labelsAndPreds = Model.predict(testData)
# labelsAndPreds = testData.map(lambda p: (Model.predict(p),p))
labelsAndPreds = testData.map(lambda p: (p.label, Model.predict(p.features),p.features))
TotalAmount = float(testData.count())
normalAmount = labelsAndPreds.filter(lambda p: p[1]==1)
oneBoltAmount = labelsAndPreds.filter(lambda p: p[0]==1).count()
ragAmount = labelsAndPreds.filter(lambda p: p[0]==0).count()

temp = labelsAndPreds.filter(lambda p: p[1]==0)

print("Second Prediction (oneBolt or other)")
Model2 = SVMModel.load(sc,"hdfs:///spark/Model/FOA_1SecModel")
temp2 = temp.map(lambda p: (p[0],Model2.predict(p[2]),p[2]))
oneBoltResult = temp2.filter(lambda p: p[1]==1)

print("third Prediction (twoBolt or rag)")
Model3 = SVMModel.load(sc,"hdfs:///spark/Model/FTR_1SecModel")
temp3 = temp2.map(lambda p: (p[0],Model3.predict(p[2])))
twoBoltResult = temp3.filter(lambda p: p[0]==p[1]and p[1]==1)
ragResult = temp3.filter(lambda p: p[0]==p[1]and p[1]==0)

#end
runTime = time()-startTime
print("TotalAmount:",TotalAmount)
print("oneBolt:",oneBoltAmount)
print("rag:",ragAmount)
print("normal result:",normalAmount.count())
print("oneBolt result:",oneBoltResult.count()/oneBoltAmount)
print("twoBolt result:",twoBoltResult.count())
print("rag result:",ragResult.count()/ragAmount)
print("Running Time:",runTime)


