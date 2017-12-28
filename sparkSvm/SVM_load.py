# Create your tests here.
from time import time
import logging
import os
#from utilities.spark_context_handler import SparkContextHandler
from pyspark import SparkContext, SparkConf
from pyspark.mllib.classification import SVMWithSGD
from pyspark.mllib.classification import SVMModel
from pyspark.mllib.regression import LabeledPoint

#setting OS environment
os.environ["PYSPARK_PYTHON"] = "python3"
os.environ["PYSPARK_DRIVER_PYTHON"] = "python3"
logger = logging.getLogger("pyspark")

#parse the data
def testparsePoint(line):
    values = [float(x) for x in line.split(",")]
    #return values
    return LabeledPoint(values[0],values[1:])
#print
def f(x):
    print(x)
#------------------------------------------------------------#
conf = SparkConf().setAppName('test').setMaster('local')
sc = SparkContext(conf=conf)
#------------------------------------------------------------#\
print("load testdata")
test = sc.textFile("file:/home/spark/Downloads/sparkSvm/CPSdata20171120.csv")
testData = test.map(testparsePoint)
#------------------------------------------------------------#
print("load model")
Model = SVMModel.load(sc,"file:///home/spark/Desktop/model")
#labelsAndPreds = Model.predict(testData)
print("Prediction")
labelsAndPreds = testData.map(lambda p: (p.label,Model.predict(p.features)))

#
accuracy = labelsAndPreds.filter(lambda p: p[0] ==p[1]).count()/float(testData.count())
truePositive = labelsAndPreds.filter(lambda p: p[0] == p[1] and p[1] == 1).count()
falsePositive = labelsAndPreds.filter(lambda p: p[0] != p[1] and p[1] == 1).count()
trueNegative = labelsAndPreds.filter(lambda p: p[0] == p[1] and p[1] == 0).count()
falseNegative = labelsAndPreds.filter(lambda p: p[0] != p[1] and p[1] == 0).count()
Precision = truePositive / (truePositive + falsePositive)
Recall = truePositive / (truePositive + falseNegative)
#print result
print("accuracy:",str(accuracy)+"\n"+
      "Precision:",str(Precision)+"\n"+
      "Recall:",str(Recall)+"\n"+
      "F-Measure = "+str(2*(Precision)*(Recall)/((Precision)+(Recall))))
