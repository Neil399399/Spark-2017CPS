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

# Setting OS environment
os.environ["PYSPARK_PYTHON"] = "python3"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python3"
logger = logging.getLogger("pyspark")
trainDir = "file:/home/spark/Documents/neil-git/dataset/normal_abnormal/Train_1sec.txt"
testDir = "file:/home/spark/Documents/neil-git/dataset/normal_abnormal/Test_1sec.txt"
firstLayerModel = "hdfs:///home/spark/Desktop/FNO_1SecModel"
secondLayerModel = "hdfs:///home/spark/Desktop/FOR_1SecModel"

# Parse the data
def parsePoint(line):
    values = [float(x) for x in line.split("\t")]
    return LabeledPoint(values[0],values[1:])

def testparsePoint(line):
    values = [float(x) for x in line.split(",")]
    return LabeledPoint(values[0],values[1:])

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
     complex = np.fft.fft(values[1:1000])

     for i in range(0,len(complex)):
        distanceOfComplex = (complex[i].real**2+complex[i].imag**2)**0.5
        newValue.append(distanceOfComplex)
     newValue.append(values[1001])
     newValue.append(values[1002])
     return LabeledPoint(newValue[0],newValue[1:])



# # Spark code
#------------------------------------------------------------#-
SparkContextHandler._master_ip = "10.14.24.101"
sc = SparkContextHandler.get_spark_sc()
#------------------------------------------------------------#
#conf = SparkConf().setAppName('test').setMaster("local")
#sc = SparkContext(conf=conf)
#----------------------------#
method = FrequencyDomain
Iterations =100
stepSize =1
reqParam = 0.01
temptrainErr = 0
tempacc = 0
tempPrecision = 0
tempRecall = 0
#----------------------------#
mylog = []
# Parse data
data = sc.textFile(trainDir)
startTime = time()
trainData = data.map(method)
#------------------start-----------------------------#
print("start training!!")
#Build the model
model = SVMWithSGD.train(trainData,iterations=Iterations,step=stepSize,regParam=reqParam)
runTime = time()-startTime

# Evaluating the model on training data
for x in range(0,5):
    print("start testing!!" + str(x))
    #test = sc.textFile("file:/home/spark/Downloads/sparkSvm/newdata1125/test(" + str(x + 1) + ").txt")
    test = sc.textFile(testDir)
    testData = test.map(method)
    labelsAndPreds = testData.map(lambda p: (p.label,model.predict(p.features)))
    #In python3 ,lambda(x,y):x+y => lambda x_y:x_y[0] + x_y[1]
    trainErr = labelsAndPreds.filter(lambda p: p[0] !=p[1]).count()/float(testData.count())
    accuracy = labelsAndPreds.filter(lambda p: p[0] ==p[1]).count()/float(testData.count())
    truePositive = labelsAndPreds.filter(lambda p: p[0] == p[1] and p[1] == 1).count()
    falsePositive = labelsAndPreds.filter(lambda p: p[0] != p[1] and p[1] == 1).count()
    trueNegative = labelsAndPreds.filter(lambda p: p[0] == p[1] and p[1] == 0).count()
    falseNegative = labelsAndPreds.filter(lambda p: p[0] != p[1] and p[1] == 0).count()

    print(truePositive,falsePositive,float(testData.count()))
    Precision = truePositive/(truePositive + falsePositive)
    Recall = truePositive/(truePositive + falseNegative)
    #save result
    temptrainErr = temptrainErr+trainErr
    tempacc = tempacc+accuracy
    tempPrecision = tempPrecision+Precision
    tempRecall = tempRecall+Recall



#-------------print result --------------------#
print("Train setting:\n"
        + "Iterations:" + str(Iterations) + "\n"
        + "stepSize:" + str(stepSize) + "\n"
        + "reqParam:" + str(reqParam) + "\n"
        + "Time:" + str(runTime) + "\n"
        + "Training Error = " + str(temptrainErr/5)+"\n"
        + "Accuracy = " + str(tempacc/5)+"\n"
        + "Precision = "+str(tempPrecision/5)+"\n"
        + "Recall = "+str(tempRecall/5)+"\n"
        + "F-Measure = "+str(2*(tempPrecision/5)*(tempRecall/5)/((tempPrecision/5)+(tempRecall/5))))


# Save logir
#sc.parallelize(mylog).saveAsTextFile("/user/spark/eventLog/")

# Save and load model
model.save(sc,"hdfs:///home/spark/Desktop/FNA_1SecModel")
#sameModel = SVMModel.load(sc,"file:///home/spark/Desktop/model")

