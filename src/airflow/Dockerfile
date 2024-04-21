# # Use the official Airflow image as a parent image
# FROM apache/airflow:2.8.4

# LABEL org.opencontainers.image.title="hossein:worker"
# # Switch to root to install additional packages
# # USER root

# # Install necessary packages
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends \
#         build-essential \
#         tzdata \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/* \
#     && openjdk-11-jdk && 

# # USER root
# RUN sudo apt-get install -y default-jre
# # RUN apt update -qq \
# #     && apt install -yq openjdk-11-jdk


# # Set the timezone (example: Asia/Tehran)
# ENV TZ=Asia/Tehran
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# # Set Java Directorydoc
# ENV JAVA_HOME='/usr/lib/jvm/java-11-openjdk-amd64'

# # Switch back to the `airflow` user
# USER airflow

# # Install additional Python packages
# RUN pip install --no-cache-dir jdatetime kafka-python SQLAlchemy confluent-kafka apache-airflow-providers-apache-spark

# # Continue with the usual Airflow setup...

###              version 1 #########################


# # Use the official Airflow image as a parent image
# FROM apache/airflow:2.8.4

# LABEL org.opencontainers.image.title="hossein:worker"

# # Switch to root to install additional packages
# USER root

# # Create the missing directory and set appropriate permissions
# RUN mkdir -p /var/lib/apt/lists/partial && \
#     chmod 644 /var/lib/apt/lists/partial

# RUN wget https://download.java.net/java/GA/jdk11/13/GPL/openjdk-11.0.1_linux-x64_bin.tar.gz \
#     && tar -xzf openjdk-11.0.1_linux-x64_bin.tar.gz \
#     && sudo mv jdk-11.0.1 /usr/lib/jvm/ \
#     && update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk-11.0.1/bin/java 1 \
#     && update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/jdk-11.0.1/bin/javac 1 \
#     && sudo rm -rf /usr/lib/jvm/jdk-11.0.1


# # Update package lists and upgrade installed packages
# RUN apt-get update && \
#     apt-get upgrade -y && \
#     apt-get install -y --no-install-recommends \
#         build-essential \
#         tzdata \
#         #default-jre && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# # Set the timezone (example: Asia/Tehran)
# ENV TZ=Asia/Tehran
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# # Set Java Directory
# ENV JAVA_HOME='/usr/lib/jvm/java-11-openjdk-amd64'

# # Switch back to the `airflow` user
# USER airflow

# # Install additional Python packages
# RUN pip install --no-cache-dir jdatetime kafka-python SQLAlchemy confluent-kafka apache-airflow-providers-apache-spark

############## version 2 #######################
# Use the official Airflow image as a parent image
FROM apache/airflow:2.8.4

LABEL org.opencontainers.image.title="hossein:worker"

# Switch to root to install additional packages
USER root

# Create the missing directory and set appropriate permissions
RUN mkdir -p /var/lib/apt/lists/partial && \
    chmod 644 /var/lib/apt/lists/partial  && \
    mkdir /usr/lib/jvm
    # mkdir /usr/bin/java && \
    # mkdir /usr/bin/java

# Copy the OpenJDK 11 tarball into the Docker image
COPY openjdk-11.0.1_linux-x64_bin.tar.gz /tmp/

# Install OpenJDK 11
RUN tar -xzf /tmp/openjdk-11.0.1_linux-x64_bin.tar.gz -C /usr/lib/jvm/ \
    && update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk-11.0.1/bin/java 1 \
    && update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/jdk-11.0.1/bin/javac 1

# Update package lists and upgrade installed packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        tzdata && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the timezone (example: Asia/Tehran)
ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set Java Directory
ENV JAVA_HOME='/usr/lib/jvm/jdk-11.0.1'

# Switch back to the `airflow` user
USER airflow

# Install additional Python packages
RUN pip install --no-cache-dir jdatetime kafka-python SQLAlchemy confluent-kafka apache-airflow-providers-apache-spark pyspark

RUN ssh-keygen -t ecdsa -b 521 -f /home/airflow/.ssh/id_ecdsa -N ''