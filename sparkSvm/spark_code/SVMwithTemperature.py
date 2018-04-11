# Create your tests here.
from time import time
import logging
import os
import math
import numpy as np
from utilities.spark_context_handler import SparkContextHandler
from pyspark import SparkContext, SparkConf
from pyspark.mllib.classification import SVMWithSGD
from pyspark.mllib.classification import SVMModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithLBFGS

# Setting OS environment
os.environ["PYSPARK_PYTHON"] = "python3"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python3"
logger = logging.getLogger("pyspark")
SparkContextHandler._master_ip = "10.14.24.101"
sc = SparkContextHandler.get_spark_sc()


def TimeDomain(line):

    try:
       values = [float(x) for x in line.split("\t")]
    except:
       values = [float(x) for x in line.split(",")]
    #Max
    Max = max(values[1:4000])
    #Min
    Min = min(values[1:4000])

    #Average   range-1 because of label
    Sum = 0
    for i in range(1,len(values)-2):
        Sum = Sum + values[i]
    Average = Sum / len(values[1:4000])

    #RMS---root of (sum(Xi-average)**2/X)
    RMSSum = 0
    for i in range(1,len(values)-2):
        RMSSum = RMSSum+(values[i]-Average)**2
    RMS=math.pow(RMSSum/len(values[1:4000]),0.5)

    #CF---Max/RMS
    CF = Max/RMS

    #SK---(sum(Xi-average)**3 /x /RMS**3
    SKSum = 0
    for i in range(1,len(values)-2):
        SKSum = SKSum+(values[i]-Average)**3
    SK= SKSum/len(values[1:4000])/RMS**3

    #K---(sum(Xi-average)**4 /x /RMS**4
    KSum = 0
    for i in range(1, len(values)-2):
        KSum = KSum + (values[i] - Average) ** 4
    K = KSum / len(values[1:4000]) / RMS ** 4

    newValue=[values[0],Max,Min,RMS,CF,SK,K,values[4001],values[4002]]
    return LabeledPoint(newValue[0],newValue[1:])

def FrequencyDomain(line):
     try:
       values = [float(x) for x in line.split("\t")]
     except:
       values = [float(x) for x in line.split(",")]
    #change data used fft and calculate distance ----- root(a**2+b**2)
     newValue = [values[0]]
     complex = np.fft.fft(values[1:826])

     for i in range(0,len(complex)):
        distanceOfComplex = (complex[i].real**2+complex[i].imag**2)**0.5
        newValue.append(distanceOfComplex)
     newValue.append(values[827])
     newValue.append(values[828])
     return LabeledPoint(newValue[0],newValue[1:])

def Train_Model(trainingRDD, method, parameter_Iterations, parameter_stepSize, parameter_reqParam):
    # model load in.
    if method == 'Logistic':
        Logistic_Model = LogisticRegressionWithLBFGS.train(trainingRDD, iterations=parameter_Iterations, regParam=parameter_reqParam)
        return Logistic_Model
    elif method == 'SVM':
        SVM_Model = SVMWithSGD.train(trainingRDD,iterations=parameter_Iterations,step=parameter_stepSize,regParam=parameter_reqParam)
        return SVM_Model
    else:
        return "No this method."

def Test_Model(testingRDD, Model):
    temptrainErr = 0
    tempacc = 0
    tempPrecision = 0
    tempRecall = 0

    for x in range(0,5):
        print("start testing!!" + str(x))
        labelsAndPreds = testingRDD.map(lambda p: (p.label,Model.predict(p.features)))
        trainErr = labelsAndPreds.filter(lambda p: p[0] !=p[1]).count()/float(testingRDD.count())
        accuracy = labelsAndPreds.filter(lambda p: p[0] ==p[1]).count()/float(testingRDD.count())
        truePositive = labelsAndPreds.filter(lambda p: p[0] == p[1] and p[1] == 1).count()
        falsePositive = labelsAndPreds.filter(lambda p: p[0] != p[1] and p[1] == 1).count()
        trueNegative = labelsAndPreds.filter(lambda p: p[0] == p[1] and p[1] == 0).count()
        falseNegative = labelsAndPreds.filter(lambda p: p[0] != p[1] and p[1] == 0).count()

        print(truePositive,falsePositive,float(testingRDD.count()))
        Precision = truePositive/(truePositive + falsePositive)
        Recall = truePositive/(truePositive + falseNegative)
        #save result
        temptrainErr = temptrainErr+trainErr
        tempacc = tempacc+accuracy
        tempPrecision = tempPrecision+Precision
        tempRecall = tempRecall+Recall
    return [temptrainErr/5,tempacc/5,tempPrecision/5,tempRecall/5]


# Input.
startTime = time()
data = sc.textFile("file:/home/spark/Documents/neil-git/dataset/twoBolt_rag/Train_1sec.txt")
test = sc.textFile("file:/home/spark/Documents/neil-git/dataset/twoBolt_rag/Test_1sec.txt")
trainData = data.map(FrequencyDomain)
testData = test.map(FrequencyDomain)

print("start training!!")
SVM_Model = Train_Model(trainData,'SVM',100,1,0.01)
result = Test_Model(testData,SVM_Model)
runTime = time()-startTime


#-------------print result --------------------#
print("Train setting:\n"
        + "Time:" + str(runTime) + "\n"
        + "Training Error = " + str(result[0])+"\n"
        + "Accuracy = " + str(result[1])+"\n"
        + "Precision = "+str(result[2])+"\n"
        + "Recall = "+str(result[3])+"\n"
        + "F-Measure = "+str(2*(result[2])*(result[3])/(result[2]+result[3])))


#Save and load model
# SVM_Model.save(sc,"hdfs:///spark/Model/FTR_1SecModel")
#sameModel = SVMModel.load(sc,"file:///home/spark/Desktop/model")

