#!/bin/bash

# Copy SSH public key to Spark worker
ssh-copy-id -i /home/airflow/.ssh/id_ecdsa.pub spark_user@da-spark-worker

# Automatically answer yes to confirmation prompt
ssh -o "StrictHostKeyChecking=no" spark_user@da-spark-worker exit

# Enter password
echo "Spark123@" | ssh spark_user@da-spark-worker sudo -S service ssh start

echo "SSH setup completed"
