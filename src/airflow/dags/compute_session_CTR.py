# from airflow import DAG 
# from airflow.providers.ssh.operators.ssh import SSHOperator

# from airflow.operators.bash import BashOperator
# from airflow.hooks.base import BaseHook
# from datetime import datetime, timedelta

# default_args = {
#     'owner': 'airscholar',
#     'start_date': datetime(2024, 1, 1, 00, 00),
# }

# # Define Airflow DAG
# with DAG('sparksql_to_elasticsearch_ssh', 
#          default_args=default_args, 
#          schedule_interval='*/10 * * * *', catchup=False) as dag:
    
#         task = SSHOperator(
#                 task_id='submit_job',
#                 ssh_conn_id='ssh_spark',
#                 command=f'spark-submit --total-executor-cores 1 --executor-cores 1 --executor-memory 2g --num-executors 1 --driver-memory 2g /opt/spark/apps/pyspark_script.py  --driver-class-path /opt/spark/data/postgresql-42.7.3.jar --jars /opt/spark/data/postgresql-42.7.3.jar'
#             )
        
############### version two ##########################
from airflow import DAG 
from airflow.providers.ssh.operators.ssh import SSHOperator

from airflow.operators.bash import BashOperator
from airflow.hooks.base import BaseHook
from datetime import datetime, timedelta

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2024, 1, 1, 00, 00),
}

# Define Airflow DAG
with DAG('sparksql_to_elasticsearch_ssh', 
         default_args=default_args, 
         schedule_interval='*/10 * * * *', catchup=False) as dag:
    
    task = SSHOperator(
        task_id='submit_job',
        ssh_conn_id='ssh_spark',
        command='python /opt/spark/apps/pyspark_script.py',
    )