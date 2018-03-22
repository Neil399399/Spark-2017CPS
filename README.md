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
1. We had already built the spark-cluster in server, if you want use or change something , please tell the IT.

2. Before you started, please read a [CPS_test_chip](http://140.124.183.8/104598027/spark_web/tree/master/cps_test_chip) first. Here has some note you to know.


## Establish Spark Cluster
If you want to have one spark cluster in local, please follow the step to setting your enviroment.

### Download and Install
Please downloads or clone the project in local, and install [Docker](https://docs.docker.com/install/) first.
#### Step1
After complete install ans start docker, please open the project and run the command to build the docker image.
```zsh
docker build -t spark/hadoop .
```
#### Step2
After build the docker image, please run the command to create the docker containers(one master and one slave or more).
```zsh
#for master
docker run -it --name spark-master -p 8088:8088 -p 50070:50070 -p 50010:50010 -p 4040:4040 -p 8042:8042 -p 8888:8888 spark/hadoop:v10 bash
```
```zsh
#for slaves
docker run -it --name spark-slave1 --link spark-master spark/hadoop:v10 bash
```
#### Step3
After finished create container, we should set the hosts to each container. Attach the container and start setting.     
```zsh
# Set hosts
cd ~/etc && vim hosts # go set the docker ID and IP address to each containers.
```
next we need to open the `PermitRootLogin` to access the ssh can connect with the root authority.
```zsh
# open PermitRootLogin
cd etc/ssh
 vim sshd_config  # PermitRootLogin => yes.
...
# If finish changed, go run:
service ssh restart
```
  ![ssh setting](https://i.imgur.com/FThJ9LH.png)
#### Setp4
Started setting spark environments(both master and slaves):
```zsh
# Setting spark-env.sh.
cd usr/local/spark/conf
vim spark-env.sh
```
add this setting:
>export SPARK_MASTER_IP={your master IP}  
export SPARK_MASTER_CORES=1     
export SPARK_WORKER_MEMORY=512m     
export SPARK_EXECUTOR_INSTANCES=4   

and here add your slaves(only master).

```zsh
# Setting slaves file.
cd usr/local/spark/conf
cp slaves.template slaves  #copy and rename.
vim slaves
```
#### Setp5
Started setting hadoop environments(both master and slaves):    
core-site.xml
```zsh
# Setting core-site.xml
cd usr/local/hadoop/etc/hadoop
vim core-site.xml
```
add this setting :
```zsh
<property>
    <name>fs.default.name</name>
    <value>hdfs://{your master ID or name}:9000</value></property>
</property>
```
yarn-site.xml
```zsh
# Setting yarn-site.xml
cd usr/local/hadoop/etc/hadoop
vim yarn-site.xml
```
add this setting :
```zsh
<property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
        </property>
<property>
        <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
        <value>org.apache.hadoop.mapred/ShuffleHandler</value>
</property>
<property>
        <name>yarn.resourcemanager.resource-tracker.address</name>
        <value>{your master ID or name}:8025</value>
</property>
<property>
        <name>yarn.resourcemanager.scheduler.address</name>
        <value>{your master ID or name}:8030</value>
</property>
<property>
        <name>yarn.resourcemanager.address</name>
        <value>{your master ID or name}:8050</value>
</property>
```
mapred-site.xml
```zsh
# Setting mapred-site.xml
cd usr/local/hadoop/etc/hadoop
cp mapred-site.xml.templete mapred-site.xml
vim mapred-site.xml
```
add this setting :
```zsh
<property>
        <name>mapred.job.tracker</name>
        <value>{your master ID or name}:54311</value>
</property>
```
hdfs-site.xml
```zsh
# Setting hdfs-site.xml
cd usr/local/hadoop/etc/hadoop
vim hdfs-site.xml
```
add this setting(for master) :
```
<property>
        <name>dfs.replication</name>
        <value>{your slaves amount }</value>
</property>
<property>
        <name>dfs.datanode.data.dir</name>
        <value>file:/usr/local/hadoop/hadoop_data/hdfs/datanode</value>
</property>
```
add this setting(for slaves) :
```
<property>
        <name>dfs.replication</name>
        <value>{your slaves amount }</value>
</property>
<property>
        <name>dfs.datanode.data.dir</name>
        <value>file:/usr/local/hadoop/hadoop_data/hdfs/namenode</value>
</property>
```
<!-- Slaves
```zsh
cd usr/local/hadoop/etc/hadoop
vim slaves
``` -->
#### Step5 
Create hdfs folder and format(both master and slaves).
```zsh
# For master
cd usr/local/hadoop/hadoop_data/hdfs
rm -r datanode

# For slaves
cd usr/local/hadoop/hadoop_data/hdfs
rm -r namenode
```
After setting, go to master container and format hdfs folder.
```zsh
hadoop namenode -format
```
#### Step6
Run Spark and test.
```zsh
pyspark --master spark://172.17.0.2:7077 --num-executors 1 --total-executor-cores=1 --executor-memory 512m
```


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

