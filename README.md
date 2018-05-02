# Spark-2017CPS
Analyze machine logs and call the  API to prediction machine status with spark cluster.

## Introduction
We're Spark clusters had built with one master and two node.      
Spark-master : 140.124.183.14     
Spark-node 1 : 10.14.24.102     
Spark-node 2 : 10.14.24.103

### Enviroment
OS : Ubuntu 16.04 LTS       
Python version : 3.5.2      
Spark version : 2.2.0     
Hadoop version : 2.7.4

#### Structure
>
    .
    ├── ...
    ├── Django-API                         # ClientUI folder.
    │   ├── migrations                    
    │   ├── mllib                          
    │         ├── SVM.py                   #  Spark fun ction code.
    │   ├── _pycache_                      
    │   ├── aprk-warehouse                 
    │   ├── admin.py         
    │   ├── apps.py                        # Set your app name.
    │   ├── models.py         
    │   ├── urls.py                        # Set the url.
    │   └── views.py                       # Create your views here.
    ├── Model                              # Spark Model folder..
    │   ├── TimeDoaminModel                  
    │   ├── FrequencyDoaminModel                          
    │   ├── SVM.py                         # Spark SVM.
    │   ├── SVM_load.py                    # Spark load models function.          
    ├── Solr                               # Solr folder.
    │   ├── solr.py                        # connect solr and something function code.
    │   ├── data                           
    ├── sparkSvm                           # Something tests and tools.
    │   ├── fft.py                         # Fourier transform.
    │   └── ...                              
    └── ...    



### Precautions
1. We had already built the spark-cluster in server, if you want use or change something , please tell the IT.

2. Before you started, please read a [CPS_test_chip](http://140.124.183.8/104598027/spark_web/tree/master/cps_test_chip) first. Here has some note you to know.

### Classification
1. SVM
2. Logistic Regression
## Django
Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

#### Structure
>
    .
    ├── ...
    ├── API folder                         # API folder.
    │   ├── migrations                    
    │   ├── _pycache_                      
    │   ├── aprk-warehouse                 
    │   ├── admin.py         
    │   ├── apps.py                        # Set your app name.
    │   ├── models.py         
    │   ├── urls.py                        # Set the url.
    │   └── views.py                       # Create your views here.
    └── ...    

