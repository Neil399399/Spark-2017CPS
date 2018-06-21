from pyspark import SparkContext, SparkConf
from pyspark.mllib.classification import LogisticRegressionModel
from pyspark.mllib.classification import SVMModel
from utilities.spark_context_handler import SparkContextHandler
from pyspark.mllib.tree import RandomForestModel

import pysolr
import logging

# basic config.
CPS_TEST_SOLR_URL = "http://140.124.183.37:8983/solr/2017CPS/"
# engine model.
LR_Layer1 = "hdfs:///spark/Model/FNAL_1SecModel"
LR_Layer2 = "hdfs:///spark/Model/FOAL_1SecModel"
LR_Layer3 = "hdfs:///spark/Model/FTRL_1SecModel"
SVM_Layer1 = "hdfs:///spark/Model/FNA_1SecModel"
SVM_Layer2 = "hdfs:///spark/Model/FOA_1SecModel"
SVM_Layer3 = "hdfs:///spark/Model/FTR_1SecModel"
Random_Forest = "hdfs:///spark/Model/random_forest_Model"
# module model.
Module_LR_Layer1 = "hdfs:///spark/Model/FNAL_1SecModel"
Module_LR_Layer2 = "hdfs:///spark/Model/FOAL_1SecModel"
Module_LR_Layer3 = "hdfs:///spark/Model/FTRL_1SecModel"
Module_SVM_Layer1 = "hdfs:///spark/Model/FNA_1SecModel"
Module_SVM_Layer2 = "hdfs:///spark/Model/FOA_1SecModel"
Module_SVM_Layer3 = "hdfs:///spark/Model/FTR_1SecModel"
Module_Random_Forest = "hdfs:///spark/Model/random_forest_Model"

# solr server.
solr_server = pysolr.Solr(CPS_TEST_SOLR_URL, timeout=10)

# spark config.
# SparkContextHandler._master_ip = "10.14.24.101"
# sc = SparkContextHandler.get_spark_sc()
conf = SparkConf().setAppName('test').setMaster('local')
sc = SparkContext(conf=conf)

# logging
# 基礎設定
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    handlers=[logging.FileHandler('my.log', 'w', 'utf-8'), ])

# 定義 handler 輸出 sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 設定輸出格式
formatter = logging.Formatter('%(asctime)s %(name)-s: %(levelname)-6s %(message)s')
# handler 設定輸出格式
console.setFormatter(formatter)
# 加入 hander 到 root logger
logging.getLogger('').addHandler(console)
# 定義另兩個 logger
logger_server = logging.getLogger('Server')




# load Model.
## LogisticRegressionModel
LR_First_Model = LogisticRegressionModel.load(sc, LR_Layer1)
LR_Second_Model = LogisticRegressionModel.load(sc, LR_Layer2)
LR_Third_Model = LogisticRegressionModel.load(sc, LR_Layer3)

Module_LR_First_Model= LogisticRegressionModel.load(sc, Module_LR_Layer1)
Module_LR_Second_Model = LogisticRegressionModel.load(sc, Module_LR_Layer2)
Module_LR_Third_Model = LogisticRegressionModel.load(sc, Module_LR_Layer3)
## SVMModel
SVM_First_Model = SVMModel.load(sc, SVM_Layer1)
SVM_Second_Model = SVMModel.load(sc, SVM_Layer2)
SVM_Third_Model = SVMModel.load(sc, SVM_Layer3)

Module_SVM_First_Model = SVMModel.load(sc, Module_SVM_Layer1)
Module_SVM_Second_Model = SVMModel.load(sc, Module_SVM_Layer2)
Module_SVM_Third_Model = SVMModel.load(sc, Module_SVM_Layer3)

## Random forset
Random_Forest_Model = RandomForestModel.load(sc,Random_Forest)
Module_Random_Forest_Model = RandomForestModel.load(sc,Random_Forest)