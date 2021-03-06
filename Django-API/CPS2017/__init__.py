from pyspark import SparkContext, SparkConf
from pyspark.mllib.classification import LogisticRegressionModel
from pyspark.mllib.classification import SVMModel
from utilities.spark_context_handler import SparkContextHandler
from pyspark.mllib.tree import RandomForestModel
import pymongo
import pysolr
import logging

# basic config.
CPS_TEST_SOLR_URL = "http://140.124.183.37:8983/solr/2017CPS/"
Cloud_Motor_url = "http://140.124.184.204:8090/Cloud/Motor_Fet/QuerySecond"
Cloud_punch_url = "http://140.124.184.204:8090/Cloud/Motor/QuerySecond"
Cloud_WSN_url = "http://140.124.184.204:8090/Cloud/WSN/QuerySecond"
Cloud_Predict_url = "http://140.124.184.204:8090/Cloud/Prediction/Insert"
# Om2m_url = "http://140.124.184.204:8082/~/in-cse/cnt-947016145"
Om2m_url_Motor = "http://140.124.184.204:8082/~/in-cse/cnt-947016145"
Om2m_url_Punch = "http://140.124.184.204:8082/~/in-cse/cnt-978995845"

# engine model.
LR_Layer1 = "hdfs:///spark/Model/logic_Model1"
LR_Layer2 = "hdfs:///spark/Model/logic_Model2"
LR_Layer3 = "hdfs:///spark/Model/logic_Model3"
SVM_Layer1 = "hdfs:///spark/Model/SVM_Model1_v4"
SVM_Layer2 = "hdfs:///spark/Model/SVM_Model2new"
SVM_Layer3 = "hdfs:///spark/Model/SVM_Model3new"
Random_Forest = "hdfs:///spark/Model/Random_forest_model_30"
# mold model.
Mold_SVM_Layer1 = "hdfs:///spark/Model/mold/pvdf2_v4"
# Mold_SVM_Layer2 = "hdfs:///spark/Model/FOA_1SecModel"
# Mold_SVM_Layer3 = "hdfs:///spark/Model/FTR_1SecModel"
Mold_Random_Forest = "hdfs:///spark/Model/mold/random_forest"

mold_Model = 'hdfs:///spark/Model/mold_Model'
# solr server.
solr_server = pysolr.Solr(CPS_TEST_SOLR_URL, timeout=10)
# mongodb
# client = pymongo.MongoClient(host='localhost', port=27017)
# mongodb = client.dbname


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

# Mold_LR_First_Model= LogisticRegressionModel.load(sc, Mold_LR_Layer1)
# Mold_LR_Second_Model = LogisticRegressionModel.load(sc, Mold_LR_Layer2)
# Mold_LR_Third_Model = LogisticRegressionModel.load(sc, Mold_LR_Layer3)
## SVMModel
SVM_First_Model = SVMModel.load(sc, SVM_Layer1)
SVM_Second_Model = SVMModel.load(sc, SVM_Layer2)
SVM_Third_Model = SVMModel.load(sc, SVM_Layer3)

Mold_SVM_First_Model = SVMModel.load(sc, Mold_SVM_Layer1)
# Mold_SVM_Second_Model = SVMModel.load(sc, Mold_SVM_Layer2)
# Mold_SVM_Third_Model = SVMModel.load(sc, Mold_SVM_Layer3)

## Random forset
Random_Forest_Model = RandomForestModel.load(sc,Random_Forest)
Mold_Random_Forest_Model = RandomForestModel.load(sc,Mold_Random_Forest)
