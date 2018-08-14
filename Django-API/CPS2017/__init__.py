from pyspark import SparkContext, SparkConf
from pyspark.mllib.classification import LogisticRegressionModel
from pyspark.mllib.classification import SVMModel
from utilities.spark_context_handler import SparkContextHandler
import pysolr

# basic config.
CPS_TEST_SOLR_URL = "http://140.124.183.37:8983/solr/2017CPS/"
LR_Layer1 = "hdfs:///spark/Model/FNAL_1SecModel"
LR_Layer2 = "hdfs:///spark/Model/FOAL_1SecModel"
LR_Layer3 = "hdfs:///spark/Model/FTRL_1SecModel"

SVM_Layer1 = "hdfs:///spark/Model/FNA_1SecModel"
SVM_Layer2 = "hdfs:///spark/Model/FOA_1SecModel"
SVM_Layer3 = "hdfs:///spark/Model/FTR_1SecModel"

mold_Model = 'hdfs:///spark/Model/mold_Model'
# solr server.
solr_server = pysolr.Solr(CPS_TEST_SOLR_URL, timeout=10)

# spark config.
# SparkContextHandler._master_ip = "10.14.24.101"
# sc = SparkContextHandler.get_spark_sc()
conf = SparkConf().setAppName('test').setMaster('local')
sc = SparkContext(conf=conf)

# load Model.
## LogisticRegressionModel
LR_First_Model = LogisticRegressionModel.load(sc, LR_Layer1)
LR_Second_Model = LogisticRegressionModel.load(sc, LR_Layer2)
LR_Third_Model = LogisticRegressionModel.load(sc, LR_Layer3)
## SVMModel
SVM_First_Model = SVMModel.load(sc, SVM_Layer1)
SVM_Second_Model = SVMModel.load(sc, SVM_Layer2)
SVM_Third_Model = SVMModel.load(sc, SVM_Layer3)