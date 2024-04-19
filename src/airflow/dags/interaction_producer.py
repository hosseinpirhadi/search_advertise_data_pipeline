import random
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select, func, text
from sqlalchemy.dialects.postgresql import UUID

# Define your database connection string
DB_CONNECTION_STRING = "postgresql://test:test@localhost:5433/advertise"

# Initialize SQLAlchemy engine
engine = create_engine(DB_CONNECTION_STRING)

def get_random_ad_id():
    # Fetch a random ad_id from the car_ad table
    with engine.connect() as conn:
        # stmt = select('*').select_from("car_ad").order_by("random").limit(1)
        stmt = select('*').select_from(text('car_ad')).order_by(func.random()).limit(1)
        result = conn.execute(stmt)
        row = result.fetchone()
        if row:
            return row
            return row[0]
        else:
            raise ValueError("No ad IDs found in the database")

def generate_ad_interaction_record():
    # Generate a random ad_id
    ad_id = get_random_ad_id()

    # Generate a random timestamp within the last 30 days
    timestamp = datetime.now(datetime.UTC) - timedelta(minutes=random.randint(0, 30*24*60))

    # Generate a random session_id
    session_id = uuid.uuid4()

    # Randomly select interaction type (True for click, False for view)
    interaction_type = random.choice([True, False])

    return {
        "id": uuid.uuid4(),
        "ad_id": ad_id,
        "type": interaction_type,
        "created_at": timestamp,
        "session_id": session_id
    }

def insert_ad_interaction_record(record):
    # Insert the record into the database
    with engine.connect() as conn:
        stmt = "INSERT INTO ad_interaction (id, ad_id, type, created_at, session_id) VALUES (%s, %s, %s, %s, %s)"
        conn.execute(stmt, (record["id"], record["ad_id"], record["type"], record["created_at"], record["session_id"]))

def generate_and_insert_ad_interactions(num_records):
    for _ in range(num_records):
        record = generate_ad_interaction_record()
        insert_ad_interaction_record(record)
