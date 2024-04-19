# Use the official Airflow image as a parent image
FROM apache/airflow:2.8.4

LABEL org.opencontainers.image.title="hossein:worker"
# Switch to root to install additional packages
USER root

# Install necessary packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the timezone (example: Asia/Tehran)
ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Switch back to the `airflow` user
USER airflow

# Install additional Python packages
RUN pip install --no-cache-dir jdatetime kafka-python SQLAlchemy confluent-kafka apache-airflow-providers-apache-spark

# Continue with the usual Airflow setup...
