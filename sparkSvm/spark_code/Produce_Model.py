# Create your tests here.
from time import time
import logging
import os
import math
import numpy as np
from utilities.spark_context_handler import SparkContextHandler
from pyspark.mllib.classification import SVMWithSGD,SVMModel
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.util import MLUtils

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
     complex = np.fft.fft(values[1:825])

     for i in range(0,len(complex)):
        distanceOfComplex = (complex[i].real**2+complex[i].imag**2)**0.5
        newValue.append(distanceOfComplex)
     newValue.append(values[826])
     newValue.append(values[827])
     return LabeledPoint(newValue[0],newValue[1:])

def MoldParser(line):
    try:
        values = [float(x) for x in line.split("\t")]
    except:
        values = [float(x) for x in line.split(",")]
    newValue = [values[0]]
    complex = np.fft.fft(values[1:])

    for i in range(0, len(complex)):
        distanceOfComplex = (complex[i].real ** 2 + complex[i].imag ** 2) ** 0.5
        newValue.append(distanceOfComplex)

    return LabeledPoint(newValue[0], newValue[1:])


def Train_Model(trainingRDD, method, parameter_Iterations, parameter_stepSize, parameter_reqParam):
    # model load in.
    if method == 'Logistic':
        Logistic_Model = LogisticRegressionWithLBFGS.train(trainingRDD, iterations=parameter_Iterations, regParam=parameter_reqParam)
        return Logistic_Model
    elif method == 'SVM':
        SVM_Model = SVMWithSGD.train(trainingRDD,iterations=parameter_Iterations,step=parameter_stepSize,regParam=parameter_reqParam)
        return SVM_Model
    elif method == 'random_foreset':
        from pyspark.mllib.tree import RandomForest, RandomForestModel
        RandomForest_Model = RandomForest.trainClassifier(trainingRDD,numClasses=4, categoricalFeaturesInfo={},
                                     numTrees=4, featureSubsetStrategy="auto",
                                     impurity='gini', maxDepth=20, maxBins=32)
        return RandomForest_Model

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

        print(truePositive,trueNegative,float(testingRDD.count()))
        Precision = truePositive/(truePositive + falsePositive)
        Recall = truePositive/(truePositive + falseNegative)
        # save result
        temptrainErr = temptrainErr+trainErr
        tempacc = tempacc+accuracy
        tempPrecision = tempPrecision+Precision
        tempRecall = tempRecall+Recall
    return [temptrainErr/5,tempacc/5,tempPrecision/5,tempRecall/5]


def Test_Model2(testingRDD,Model):
    class_0_true =0
    class_1_true =0
    class_2_true =0
    class_3_true =0

    class_0_false1=0
    class_0_false2 =0
    class_0_false3=0

    class_1_false0 =0
    class_1_false2 =0
    class_1_false3 =0

    class_2_false0 = 0
    class_2_false1 = 0
    class_2_false3= 0

    class_3_false0 =0
    class_3_false1 =0
    class_3_false2 =0


    accuracy = 0
    trainErr = 0
    total_amount = len(testingRDD.collect())
    for test_data in testingRDD.collect():
        predict = Model.predict(test_data.features)
        label = test_data.label
        # label-predict
        ## class 0
        if (label == 0 and predict == 0):
            class_0_true+=1
        elif (label == 0  and predict == 1):
            class_0_false1+=1
        elif (label == 0  and predict == 2):
            class_0_false2+=1
        elif (label == 0  and predict == 3):
            class_0_false3+=1

        ## class1
        if (label == 1 and predict == 0):
            class_1_false0+=1
        elif (label == 1  and predict == 1):
            class_1_true+=1
        elif (label == 1  and predict == 2):
            class_1_false2+=1
        elif (label == 1  and predict == 3):
            class_1_false3+=1

        ## class2
        if (label == 2 and predict == 0):
            class_2_false0+=1
        elif (label == 2  and predict == 1):
            class_2_false1+=1
        elif (label == 2  and predict == 2):
            class_2_true+=1
        elif (label == 2  and predict == 3):
            class_2_false3+=1

        ## class3
        if (label == 3 and predict == 0):
            class_3_false0+=1
        elif (label == 3  and predict == 1):
            class_3_false1+=1
        elif (label == 3  and predict == 2):
            class_3_false2+=1
        elif (label == 3  and predict == 3):
            class_3_true+=1




    class0_amount = len(testingRDD.filter(lambda p: p.label == 0).collect())
    class1_amount = len(testingRDD.filter(lambda p: p.label == 1).collect())
    class2_amount = len(testingRDD.filter(lambda p: p.label == 2).collect())
    class3_amount = len(testingRDD.filter(lambda p: p.label == 3).collect())

    class0 = [class_0_true,class_0_false1,class_0_false2,class_0_false3,class0_amount]
    class1 = [class_1_false0,class_1_true,class_1_false2,class_1_false3,class1_amount]
    class2 = [class_2_false0,class_2_false1,class_2_true,class_2_false3,class2_amount]
    class3 = [class_3_false0,class_3_false1,class_3_false2,class_3_true,class3_amount]

    return [class0,class1,class2,class3]




# Input.
startTime = time()
data = sc.textFile("file:/home/spark/Documents/neil-git/dataset/Random_Forest_Train.txt")
test = sc.textFile("file:/home/spark/Documents/neil-git/dataset/Random_Forest_Test.txt")
trainData = data.map(FrequencyDomain)
testData = test.map(FrequencyDomain)

# for random forest.
print("start training!!")
model = Train_Model(trainData,'random_foreset',None,None,None)
result = Test_Model2(testData,model)
runTime = time()-startTime
#
#
# #-------------print result --------------------#
# print("Result:\n"
#         + "Time:" + str(runTime) + "\n"
#         + "Training Error = " + str(result[0])+"\n"
#         + "Accuracy = " + str(result[1])+"\n"
#         + "Precision = "+str(result[2])+"\n"
#         + "Recall = "+str(result[3])+"\n"
#         + "F-Measure = "+str(2*(result[2])*(result[3])/(result[2]+result[3])))
#
print('Reault:\n')
i =0
for res in result:
    print('Class:',i)
    print('result',res)
    print('#############################################')
    i+=1


#Save and load model
model.save(sc,"hdfs:///spark/Model/random_forest_Model")
