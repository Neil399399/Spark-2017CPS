# Spark-2017CPS
Analyze machine logs and call the  API to prediction machine status with spark cluster.

## Introduction
We're Spark clusters had built with one master and two node.      
Spark-master : 140.124.183.14     
Spark-node 1 : 10.14.24.102     
Spark-node 2 : 10.14.24.103

### Enviroment
OS : Ubuntu 16.04 LTS       
Python version : 3.5.2      
Spark : 2.2.0     
Hadoop : 2.7.4

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
1. We had already built the spark-cluster in server, if you want use or change something , please tell the IT.

2. Before you started, please read a [CPS_test_chip](http://140.124.183.8/104598027/spark_web/tree/master/cps_test_chip) first. Here has some note you to know.


## Establish Spark Cluster
If you want to have one spark cluster in local, please follow the step to setting your enviroment.

### Download and Install 
#### Install Package
Run update for your OS first.
> sudo apt-get update

> sudo apt-get upgrade

Install the packages.
> sudo apt-get install apache2 apache2-dev libapache2-mod-wsgi-py3

>sudo pip3 install django pysolr numppy py4j  jsonpickle django-cors-headers
   
Before we started , please download [Spark](https://spark.apache.org/downloads.html) and [Hadoop](http://hadoop.apache.org/#Download+Hadoop) first.          

Attention, when you download Spark , you should choose the versions which supported your hadoop versions. 

### Install Spark     
After downloaded, unzip in `/usr/local/` and rename to `spark`.

In to spark folder and move `pyspark` to `/usr/local/lib/python3.x/dist-packages/`, `x` is your Python version.
>sudo cp -r python/pyspark /usr/local/lib/python3.x/dist-packages/

Next open your terminal and open `bashrc` :
> sudo vim gedit ~/.bashrc      

import Spark variables :
``` zsh
#SPARK_HOME
export SPARK_HOME=/usr/local/spark
#PATH
export PATH=$PATH:$SPARK_HOME/bin
```
after edited, save and resource `bashrc`.
>source ~ /.bashrc      

and now you can go to terminal to run the `spark-shell`.

#### Setting Spark-shell
First, open your terminal and go to your spark folder.
> cd /usr/local/spark/conf

and copy the `log4j.properties.template` to `log4j.properties`.
> cp log4j.properties.template log4j.properties

edit:
> sudo gedit log4j.properties
```zsh
# Change INFO to WARN.
## Set everything to be logged to console.
log4j.rootCategory = WARN, console
```
### Install Hadoop
After downloaded, unzip in `/usr/local/` and rename to `hadoop`.
#### Setting hostname and IP
> sudo vim /etc/hostname
```zsh
master
```
Remember, different node should have different hostname.

Setting hosts IP
> sudo vim /etc/hosts
```zsh
(your master IP) master
(your node IP) slave1
...
```
#### Setting SSH Connection
> sudo apt-get install ssh

Get a master ssh key.
> ssh-keygen -t rsa -P ""

Give master key to slaves.
> cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys

>scp -r ~/.ssh slave1:~/

After send the key, you can run `ssh slave1` and connect slave1.

#### Install Java 
We need to install java in master and slave.
> sudo apt-get install openjdk-7-jdk  (or other version)        

#### Install Hadoop 

Follow this website step to setting.

1. [Install Hadoop on Ubuntu](https://jerrynest.io/install-hadoop-on-ubuntu/)

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

