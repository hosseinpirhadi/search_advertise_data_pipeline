# #!/bin/bash

# # Copy SSH public key to Spark worker

# # Automatically answer yes to confirmation prompt
# ssh -o "StrictHostKeyChecking=no" spark_user@da-spark-worker exit

# # Enter password
# echo "Spark123@" #| ssh spark_user@da-spark-worker

# echo "SSH setup completed"


#!/bin/bash

# ssh-keygen -t ecdsa -b 521 -f /home/airflow/.ssh/id_ecdsa -N ''

sudo ssh-copy-id -i /home/airflow/.ssh/id_ecdsa.pub spark_user@da-spark-worker

# Variables
SPARK_USER="spark_user"
SPARK_HOST="da-spark-worker"
KEY_PATH="/home/airflow/.ssh/id_ecdsa.pub"
PASSWORD="Spark123@"  # Caution: Storing passwords in scripts is insecure

# Copy the SSH key using sshpass
sshpass -p "$PASSWORD" ssh-copy-id -i "$KEY_PATH" -o StrictHostKeyChecking=no "$SPARK_USER@$SPARK_HOST"
