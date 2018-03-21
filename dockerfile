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
# passwordless ssh
RUN ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key -y
RUN ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key -y
RUN ssh-keygen -q -N "" -t rsa -f /root/.ssh/id_rsa
RUN cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

# java
RUN apt-get install default-jre -y
ENV JAVA_HOME /usr/java/default
ENV PATH $PATH:$JAVA_HOME/bin

# hadoop
RUN wget http://apache.stu.edu.tw/hadoop/common/hadoop-2.7.5/hadoop-2.7.5.tar.gz
RUN tar zxf hadoop-2.7.5.tar.gz
RUN mv hadoop-2.7.5 /usr/local/hadoop
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
RUN sed -i '/^export JAVA_HOME/ s:.*:export JAVA_HOME=/usr/java/default\nexport HADOOP_PREFIX=/usr/local/hadoop\nexport HADOOP_HOME=/usr/local/hadoop\n:' $HADOOP_HOME/etc/hadoop/hadoop-env.sh
# RUN sed -i '/^export HADOOP_CONF_DIR/ s:.*:export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop/:' $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# #RUN . $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh
# RUN mkdir $HADOOP_PREFIX/input
# RUN cp $HADOOP_PREFIX/etc/hadoop/*.xml $HADOOP_PREFIX/input

# # pseudo distributed
# ADD core-site.xml.template $HADOOP_PREFIX/etc/hadoop/core-site.xml.template
# RUN sed s/HOSTNAME/localhost/ /usr/local/hadoop/etc/hadoop/core-site.xml.template > /usr/local/hadoop/etc/hadoop/core-site.xml
# ADD hdfs-site.xml $HADOOP_PREFIX/etc/hadoop/hdfs-site.xml
# ADD mapred-site.xml $HADOOP_PREFIX/etc/hadoop/mapred-site.xml
# ADD yarn-site.xml $HADOOP_PREFIX/etc/hadoop/yarn-site.xml
# RUN $HADOOP_PREFIX/bin/hdfs namenode -format

# fixing the libhadoop.so like a boss
RUN rm -rf /usr/local/hadoop/lib/native
RUN mv /tmp/native /usr/local/hadoop/lib
ADD ssh_config /root/.ssh/config
RUN chmod 600 /root/.ssh/config
RUN chown root:root /root/.ssh/config


ADD bootstrap.sh /etc/bootstrap.sh
RUN chown root:root /etc/bootstrap.sh
RUN chmod 700 /etc/bootstrap.sh
ENV BOOTSTRAP /etc/bootstrap.sh
# workingaround docker.io build error
RUN ls -la /usr/local/hadoop/etc/hadoop/*-env.sh
RUN chmod +x /usr/local/hadoop/etc/hadoop/*-env.sh
RUN ls -la /usr/local/hadoop/etc/hadoop/*-env.sh

# fix the 254 error code
RUN sed  -i "/^[^#]*UsePAM/ s/.*/#&/"  /etc/ssh/sshd_config
RUN echo "UsePAM no" >> /etc/ssh/sshd_config
RUN echo "Port 2122" >> /etc/ssh/sshd_config
RUN service sshd start && $HADOOP_HOME/etc/hadoop/hadoop-env.sh && $HADOOP_HOME/sbin/start-dfs.sh && $HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/root
RUN service sshd start && $HADOOP_HOME/etc/hadoop/hadoop-env.sh && $HADOOP_HOME/sbin/start-dfs.sh && $HADOOP_HOME/bin/hdfs dfs -put $HADOOP_HOME/etc/hadoop/ input



# RUN wget -s http://apache.stu.edu.tw/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz |  tar -xz -C /usr/local/
# RUN cd /usr/local && ln -s spark-2.3.0-bin-hadoop2.7 spark
# ENV SPARK_HOME /usr/local/spark
# RUN mkdir $SPARK_HOME/yarn-remote-client
# ADD yarn-remote-client $SPARK_HOME/yarn-remote-client
# RUN $BOOTSTRAP && $HADOOP_PREFIX/bin/hadoop dfsadmin -safemode leave && $HADOOP_PREFIX/bin/hdfs dfs -put $SPARK_HOME-1.5.1-bin-hadoop2.6/lib /spark
# ENV YARN_CONF_DIR $HADOOP_PREFIX/etc/hadoop
# ENV PATH $PATH:$SPARK_HOME/bin:$HADOOP_PREFIX/bin

# # update boot script
# COPY bootstrap.sh /etc/bootstrap.sh
# RUN chown root.root /etc/bootstrap.sh
# RUN chmod 700 /etc/bootstrap.sh


# spark ports
EXPOSE 4040
# Hdfs ports
EXPOSE 50010 50020 50070 50075 50090
# Mapred ports
EXPOSE 19888
#Yarn ports
EXPOSE 8030 8031 8032 8033 8040 8042 8088
#Other ports
EXPOSE 49707 2122  
ENTRYPOINT ["/etc/bootstrap.sh"]

