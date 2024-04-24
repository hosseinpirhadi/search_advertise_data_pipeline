from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow import DAG
from datetime import datetime

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2024, 1, 1, 00, 00),
}

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the logging level to INFO

import os
logging.info(f"print pwd {os.getcwd()}")

# Define Airflow DAG
with DAG('sparksql_to_elasticsearch', 
         default_args=default_args, 
         schedule_interval='*/10 * * * *', catchup=False) as dag:
    # Define PythonOperator to execute SparkSQL job
    submit_job = SparkSubmitOperator(
        task_id='submit_job',
        application='/opt/spark/apps/pyspark_script.py',
        conn_id='spark_default',
        total_executor_cores='1',
        executor_cores='1',
        executor_memory='2g',
        num_executors='1',
        driver_memory='2g',
        verbose=False
    )
    # spark_sql_task = PythonOperator(
    #     task_id='spark_sql_job',
    #     python_callable=spark_sql_job
    # )
