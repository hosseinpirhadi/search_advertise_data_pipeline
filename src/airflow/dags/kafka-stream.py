from confluent_kafka import Producer
import json
from  datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests


default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2024, 1, 1, 00, 00),
}

def poling_api():
    API_URL = "https://bama.ir/cad/api/search?pageIndex=1"
    HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }   
    response = requests.get(API_URL, headers=HEADERS)
    response.raise_for_status() 
    return response.json()


def format_data(data):
    items = []
    for item in data['data']['ads']:
        if item.get('detail'):
            formatted_item = {
                'code' : item['detail'].get('code'),
                'title': item['detail'].get('title'),
                'year' : item['detail'].get('year'),
                'miles': item['detail'].get('mileage'),
                'date' : item['detail'].get('modified_date'),
                'price': item['price'].get('price')
            }
            
            items.append(formatted_item)
    return items


def stream_data():
    producer = Producer({'bootstrap.servers': 'kafka_first:9091',
                        'enable.idempotence': True})
    data = poling_api()
    formatted_data = format_data(data)
    for message in formatted_data:
        producer.produce('ads_fetched', key=str(message["code"]), value=json.dumps(message, ensure_ascii=False))
        producer.flush() 

with DAG('producer_automation', default_args=default_args, schedule_interval='@hourly', catchup=False) as dag:
    stream_task = PythonOperator(
        task_id='stream_data_from_bama',
        python_callable=stream_data
    )
