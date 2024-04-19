# FROM python:3.9.19-bullseye as spark-base

# ARG SPARK_VERSION=3.4.0

# RUN apt-get update & \
#     apt-get install -y --no-install-recommends \
#         sudo \
#         curl \
#         vim \
#         unzip \
#         rsync \
#         openjdk-11-jdk \
#         build-essential \
#         software-propertise-common \
#         ssh & \
#     apt-get clean & \
#     rm -rf /var/lib/apt/lists/*

# ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
# ENV HADOOP_HOME=${HADOOP_HOME:-"/opt/hadoop"}  

# RUN mkdir -p ${HADOOP_HOME} && mkdir -p ${SPARK_HOME}
# WORKDIR ${SPARK_HOME}

# # RUN curl https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz -o spark-3.5.1-bin-hadoop3.tgz \
# #  &&
# USER root
# COPY ./spark-3.5.1-bin-hadoop3.gz .
# RUN tar xvzf spark-3.5.1-bin-hadoop3.gz --directory /opt/spark --strip-components 1 

# # RUN echo "nameserver 10.202.10.202" | tee /etc/resolv.conf > /dev/null   
# #  && rm -rf spark-3.5.1-bin-hadoop3.gz

# COPY ./requirements.txt .
# RUN pip3 install -r requirements.txt

# ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"
# ENV SPARK_HOME="/opt/spark"
# ENV SPARK_MASTER="spark://spark-master:7077"
# ENV SPARK_MASTER_HOST spark-master
# ENV SPARK_MASTER_PORT 7077
# ENV PYSPARK_PYTHON python3

# COPY ./spark-defaults.conf "$SPARK_HOME/conf"

# RUN chmod u+x /opt/spark/sbin/* && \
#     chmod u+x /opt/spark/bin/*

# ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

# COPY entrypoint.sh .

# RUN chmod +x entrypoint.sh

# ENTRYPOINT ["./entrypoint.sh"]  


######### TEST #############################



FROM python:3.9.19-bullseye as spark-base

ARG SPARK_VERSION=3.4.0

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sudo \
        curl \
        vim \
        unzip \
        rsync \
        openjdk-11-jdk \
        build-essential \
        software-properties-common \
        ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV SPARK_HOME=${SPARK_HOME:-"/opt/spark"}
ENV HADOOP_HOME=${HADOOP_HOME:-"/opt/hadoop"}

RUN mkdir -p ${HADOOP_HOME} && mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}

COPY ./spark-3.5.1-bin-hadoop3.gz .
RUN tar xvzf spark-3.5.1-bin-hadoop3.gz --directory /opt/spark --strip-components 1 && \
    rm spark-3.5.1-bin-hadoop3.gz

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"
ENV SPARK_HOME="/opt/spark"
ENV SPARK_MASTER="spark://spark-master:7077"
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3
ENV JAVA_HOME='/usr/lib/jvm/java-11-openjdk-amd64'
ENV PATH $JAVA_HOME/bin:$PATH

COPY ./spark-defaults.conf "$SPARK_HOME/conf"
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH

ENTRYPOINT ["./entrypoint.sh"]
