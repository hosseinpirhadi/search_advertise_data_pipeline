
from datetime import datetime, timedelta
import psycopg2
import json
import uuid
import logging
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define default arguments for the DAG
default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2024, 1, 1, 00, 00),
}

# Kafka consumer configuration
consumer_conf = {
    'bootstrap_servers': 'kafka_first:9091',  # Update with your Kafka broker address
    'group_id': 'second_consumer_group',
    'auto_offset_reset': 'earliest' 
}

# PostgreSQL connection parameters
pg_conn_params = {
    'dbname': 'advertise',
    'user': 'test',
    'password': 'test',
    'host': 'postgres_store',
    'port': 5432
}

# Function to insert data into PostgreSQL
def insert_to_postgres(data):
    try:
        conn = psycopg2.connect(**pg_conn_params)
        cursor = conn.cursor()
        # Assuming your table structure and data format
        cursor.execute("INSERT INTO ad_interaction (id, ad_id, created_at, session_id, type) VALUES (%s, %s, %s, %s, %s)", 
                       (data['id'], data['ad_id'], data['created_at'], data['session_id'], data['type']))
        conn.commit()
        logger.info("Data inserted into PostgreSQL")
    except psycopg2.Error as e:
        logger.error(f"Error inserting data into PostgreSQL: {e}")
    finally:
        if conn:
            conn.close()

def consume_from_kafka():
    consumer = KafkaConsumer(**consumer_conf, enable_auto_commit=True)
    consumer.subscribe(['ad_impression'])
    records = consumer.poll(60 * 1000) 
    for tp, consumer_records in records.items():
        for consumer_record in consumer_records:
            data = json.loads(consumer_record.value.decode('utf-8'))
            data['id'] = str(uuid.uuid4())
            print(data)
            # data['created_at'] = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            insert_to_postgres(data)
    consumer.commit()

with DAG(
        'view_automation', 
        default_args=default_args, 
        schedule_interval='@hourly', 
        catchup=False
    ) as dag:
    generate_view_task = PythonOperator(
        task_id='insert_view_to_postgres',
        python_callable=consume_from_kafka
    )