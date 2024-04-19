import random
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select, func, text
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
import json
from confluent_kafka import Producer
# Define default arguments for the DAG
default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2024, 1, 1, 00, 00),
}

# Define your database connection string
DB_CONNECTION_STRING = "postgresql://test:test@postgres_store:5432/advertise"

# Initialize SQLAlchemy engine
engine = create_engine(DB_CONNECTION_STRING)

def get_random_ad_id():
    # Fetch a random ad_id from the car_ad table
    with engine.connect() as conn:
        stmt = select('*').select_from(text('car_ad')).order_by(func.random()).limit(1)
        result = conn.execute(stmt)
        row = result.fetchone()
        if row:
            return row[0]
        else:
            raise ValueError("No ad IDs found in the database")

def generate_ad_interaction_record():
    # Generate a random ad_id
    ad_id = str(get_random_ad_id())
    # Generate a random timestamp within the last 30 days
    timestamp = datetime.utcnow() - timedelta(minutes=random.randint(0, 30*24*60))
    timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    # Generate a random session_id
    session_id = str(uuid.uuid4())
    # Randomly select interaction type (True for click, False for view)
    interaction_type = random.choice([True, False])
    return {"id": str(uuid.uuid4()), "ad_id": ad_id, "type": interaction_type, "created_at": timestamp, "session_id": session_id}

def insert_ad_interaction_records(records):
    # Insert the records into the database
    with engine.connect() as conn:
        stmt = "INSERT INTO ad_interaction (id, ad_id, type, created_at, session_id) VALUES (%s, %s, %s, %s, %s)"
        conn.execute(stmt, [(record["id"], record["ad_id"], record["type"], record["created_at"], record["session_id"]) for record in records])

def generate_and_insert_ad_interactions():
    num_records = 10  # Example: Insert 10 records per hourly execution
    records = [generate_ad_interaction_record() for _ in range(num_records)]
    # insert_ad_interaction_records(records)
    producer = Producer(
                    {
                        'bootstrap.servers': 'kafka_first:9091',
                        'enable.idempotence': True
                    }
                )
    
    for message in records:
        topic = 'ad_impression' if message['type'] else 'ad_click'  # Determine topic based on type
        producer.produce(topic, key=message["id"], value=json.dumps(message, ensure_ascii=False))
        
    producer.flush() 

with DAG('interaction_automation', default_args=default_args, schedule_interval='@hourly', catchup=False) as dag:
    generation_task = PythonOperator(
        task_id='stream_ad_interaction',
        python_callable=generate_and_insert_ad_interactions
    )
