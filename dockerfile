# This is the docker images for run the Lib-Analysis API.
# VERSION 1.0.0
# Author: NEIL

FROM ubuntu
USER root

# Neil Huang <neil399399@gmail.com>
# install dev tools
RUN apt-get update
RUN apt-get install wget -y
RUN apt-get install vim -y
RUN apt-get install python -y
RUN apt-get install ssh -y
RUN apt-get install rsync -y
RUN apt-get install -y bzip2
RUN apt-get install net-tools
# RUN apt-get install python-pip -y
# passwordless ssh
RUN ssh-keygen -t dsa -P '' -f /root/.ssh/id_dsa
RUN cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys

# java
RUN apt-get install default-jre -y
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
ENV PATH $PATH:$JAVA_HOME/bin

# hadoop
RUN wget http://apache.stu.edu.tw/hadoop/common/hadoop-2.7.5/hadoop-2.7.5.tar.gz
RUN tar -zxvf hadoop-2.7.5.tar.gz && mv hadoop-2.7.5 /usr/local/hadoop
ENV HADOOP_HOME /usr/local/hadoop
ENV HADOOP_COMMON_HOME /usr/local/hadoop
ENV HADOOP_HDFS_HOME /usr/local/hadoop
ENV HADOOP_MAPRED_HOME /usr/local/hadoop
ENV HADOOP_YARN_HOME /usr/local/hadoop
ENV HADOOP_COMMON_LIB_NATIVE_DIR /usr/local/hadoop/lib/native
ENV HADOOP-OPTS '-Djava.library.path=/usr/local/hadoop/lib'
ENV JAVA_LIBRARY_PATH /usr/local/hadoop/lib/native:$JAVA_LIBRARY_PATH

ENV PATH $PATH:$HADOOP_HOME/bin
ENV PATH $PATH:$HADOOP_HOME/sbin

ENV HADOOP_CONF_DIR /usr/local/hadoop/etc/hadoop
ENV YARN_CONF_DIR $HADOOP_PREFIX/etc/hadoop
RUN sed -i '/^export JAVA_HOME/ s:.*:export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64\nexport HADOOP_HOME=/usr/local/hadoop\n:' $HADOOP_HOME/etc/hadoop/hadoop-env.sh
RUN sed -i '/^export HADOOP_CONF_DIR/ s:.*:export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop/:' $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# HDFS folder.
RUN mkdir -p /usr/local/hadoop/hadoop_data/hdfs/namenode
RUN mkdir -p /usr/local/hadoop/hadoop_data/hdfs/datanode



# Spark 
RUN wget http://apache.stu.edu.tw/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz
RUN tar -zxvf spark-2.3.0-bin-hadoop2.7.tgz && mv spark-2.3.0-bin-hadoop2.7 /usr/local/spark
ENV SPARK_HOME /usr/local/spark
RUN cp /usr/local/spark/conf/spark-env.sh.template /usr/local/spark/conf/spark-env.sh
RUN sed -i '/^export SPARK_MASTER_IP/ s:.*:export SPARK_MASTER_IP=master\nexport SPARK_WORKER_CORES=1\nexport SPARK_WORKER_MEMORY=1g\nexport SPARK_EXECUTOR_INSTANCES=4:' $SPARK_HOME/conf/spark-env.sh
ENV PATH $PATH:$SPARK_HOME/bin
ENV PATH $PATH:$SPARK_HOME/sbin

# Anaconda2-2.5.0
# RUN wget https://repo.continuum.io/archive/Anaconda3-5.0.0.1-Linux-x86_64.sh && bash Anaconda3-5.0.0.1-Linux-x86_64.sh -b
# ENV PATH $PATH:~/anaconda3/bin
# ENV ANACONDA_PATH ~/anaconda3
# ENV PYSPARK_DRIVER_PYTHON $ANACONDA_PATH/bin/ipython
# ENV PYSPARK_PYTHON $ANACONDA_PATH/bin/python

# Ipynotebook
RUN mkdir -p ~/pythonwork/ipynotebook
RUN echo "root:123456" | chpasswd


# spark ports
EXPOSE 4040 7077 8080 8081
# Hdfs ports
EXPOSE 50010 50020 50070 50075 50090 8025 8030 8050 54311 9000
# Mapred ports
EXPOSE 19888
#Yarn ports
EXPOSE 8030 8031 8032 8033 8040 8042 8088 8888
#Other ports
EXPOSE 49707 2122 22
CMD ["executable","param1","param2"]

