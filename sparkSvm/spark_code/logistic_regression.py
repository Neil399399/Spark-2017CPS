
from __future__ import print_function
from time import time
import sys
import numpy as np
import os
import math
import logging
from pyspark.ml.classification import LogisticRegression
from pyspark import SparkContext, SparkConf
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.mllib.regression import LabeledPoint

#setting OS environment
os.environ["PYSPARK_PYTHON"] = "python3"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python3"
#logger = logging.getLogger("pyspark")


if __name__ == "__main__":

  conf = SparkConf().setAppName('LogisticRegressionWithLBFGSModel_RDD').setMaster('local')
  sc = SparkContext(conf=conf)

  # Load and parse the data
  def parsePoint(line):
      values = [float(x) for x in line.split(",")]
      return LabeledPoint(values[0], values[1:])

  def timeDomain(line):

    try:
      values = [float(x) for x in line.split("\t")]
    except:
      values = [float(x) for x in line.split(",")]
    # Max
    Max = max(values[1:])
    # Min
    Min = min(values[1:])

    # Average   range-1 because of label
    Sum = 0
    for i in range(1, len(values)):
      Sum = Sum + values[i]
    Average = Sum / len(values[1:])

    # RMS---root of (sum(Xi-average)**2/X)
    RMSSum = 0
    for i in range(1, len(values)):
      RMSSum = RMSSum + (values[i] - Average) ** 2
    RMS = math.pow(RMSSum / len(values[1:]), 0.5)

    # CF---Max/RMS
    CF = Max / RMS

    # SK---(sum(Xi-average)**3 /x /RMS**3
    SKSum = 0
    for i in range(1, len(values)):
      SKSum = SKSum + (values[i] - Average) ** 3
    SK = SKSum / len(values[1:]) / RMS ** 3

    # K---(sum(Xi-average)**4 /x /RMS**4
    KSum = 0
    for i in range(1, len(values)):
      KSum = KSum + (values[i] - Average) ** 4
    K = KSum / len(values[1:]) / RMS ** 4

    newValue = [values[0], Max, Min, RMS, CF, SK, K]
    return LabeledPoint(newValue[0], newValue[1:])

  def frequencyDomain(line):
    try:
      values = [float(x) for x in line.split("\t")]
    except:
      values = [float(x) for x in line.split(",")]
    # change data used fft and calculate distance ----- root(a**2+b**2)
    newValue = [values[0]]
    complex = np.fft.fft(values[1:])

    for i in range(0, len(complex)):
        distanceOfComplex = (complex[i].real**2+complex[i].imag**2)**0.5
        newValue.append(distanceOfComplex)

    return LabeledPoint(newValue[0], newValue[1:])


  print("****** start get data ******", "\n")
  data = sc.textFile("file:/home/spark/Downloads/sparkSvm/merge.txt")

  # ----------------------------#
  method = frequencyDomain
  Iterations = 0
  regParam = 0.01
  temptrainErr = 0
  tempacc = 0
  tempPrecision = 0
  tempRecall = 0
  finalF_Measure = 0
  finalIterations = 0
  finalTime = 0
  finalTrainingError = 0
  finalAccuracy = 0
  finalPrecision = 0
  finalRecall = 0
  # ----------------------------#
  totalCostTime = time()

  for Iterations in range(1, 151):

    startTime = time()
    trainDataMethod = data.map(method)
    #print(trainDataMethod.collect())

    # Build the model
    print("****** start training model ******", "\n")
    model = LogisticRegressionWithLBFGS.train(trainDataMethod, iterations=Iterations, regParam=regParam)

    # calculate training time
    trainTime = time() - startTime
    print("****** training finish ******", "\n")

    # Evaluating the model on training data
    print("****** start Evaluating the model on training data ******", "\n")

    temptrainErr = 0
    tempacc = 0
    tempPrecision = 0
    tempRecall = 0

    for i in range(0, 5):
      # Loading text Data
      #print("start testing file " + str(i), "\n")
      test = sc.textFile("file:/home/spark/Downloads/sparkSvm/test(" + str(i + 1) + ").txt")
      # Model predict
      testData = test.map(method)
      #print(testData.count())
      labelsAndPreds = testData.map(lambda p: (p.label, model.predict(p.features)))
      #print(labelsAndPreds.collect())
      trainErr = labelsAndPreds.filter(lambda p: p[0] != p[1]).count() / float(testData.count())
      accuracy = labelsAndPreds.filter(lambda p: p[0] == p[1]).count() / float(testData.count())
      truePositive = labelsAndPreds.filter(lambda p: p[0] == p[1] and p[1] == 1).count()
      falsePositive = labelsAndPreds.filter(lambda p: p[0] != p[1] and p[1] == 1).count()
      trueNegative = labelsAndPreds.filter(lambda p: p[0] == p[1] and p[1] == 0).count()
      falseNegative = labelsAndPreds.filter(lambda p: p[0] != p[1] and p[1] == 0).count()
      # Calculate Precision and Recall
      if(truePositive==0 and falsePositive ==0):
        Precision = 0
      else:
        Precision = truePositive / (truePositive + falsePositive)
      Recall = truePositive / (truePositive + falseNegative)
      # save result
      temptrainErr = temptrainErr + trainErr
      tempacc = tempacc + accuracy
      tempPrecision = tempPrecision + Precision
      tempRecall = tempRecall + Recall
      """
      print("=================================================\n")
      print("TrainErr :", trainErr)
      print("Accuracy :", accuracy)
      print("truePositive :", truePositive)
      print("falsePositive :", falsePositive)
      print("trueNegative :", trueNegative)
      print("falseNegative :", falseNegative)
      print("Precision :", Precision)
      print("Recall :", Recall)
      print("temptrainErr :", temptrainErr)
      print("tempacc :", tempacc)
      print("tempPrecision :", tempPrecision)
      print("tempRecall :", tempRecall)
      print("=================================================\n")
      """


    if (tempPrecision==0 and tempRecall==0):
      tempF_Measure = 0
    else:
      tempF_Measure = 2*(tempPrecision/5)*(tempRecall/5)/((tempPrecision/5)+(tempRecall/5))


    if finalF_Measure < tempF_Measure and tempF_Measure != 1.0:
      finalIterations = Iterations
      finalTime = trainTime
      finalTrainingError = temptrainErr
      finalAccuracy = tempacc
      finalPrecision = tempPrecision
      finalRecall = tempRecall
      finalF_Measure = tempF_Measure

    print("=================================================\n")
    print("CurrentRoundCostTime :", time() - startTime, "  sec")
    print("CurrentIteration :", Iterations)
    print("CurrentF-Measure :", str(tempF_Measure))
    print("BestIteration: ", finalIterations)
    print("BestF-Measure :", str(finalF_Measure))
    print("TotalCostTime :", time()-totalCostTime, "  sec")
    print("\n=================================================\n")






  # -------------print result --------------------#
  print("*******  Train setting  *******\n\n"
        + "Iterations:" + str(finalIterations) + "\n"
#        + "RegParam:" + str(regParam) + "\n"
        + "Time:" + str(finalTime) + "\n"
        + "Training Error = " + str(finalTrainingError / 5) + "\n"
        + "Accuracy = " + str(finalAccuracy / 5) + "\n"
        + "Precision = " + str(finalPrecision / 5) + "\n"
        + "Recall = " + str(finalRecall / 5) + "\n"
        + "F-Measure = " + str(finalF_Measure) + "\n\n"
        + "*******  Train setting  *******")





  # Save Model
  #print("--start save model--", "\n")
  #model.save(sc, "file:/home/spark/Documents/spark_web/xuan/model")


