from confluent_kafka import Producer
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Kafka Producer Configuration
producer_config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': os.getenv('KAFKA_SASL_USERNAME'),
    'sasl.password': os.getenv('KAFKA_SASL_PASSWORD')
}
producer = Producer(**producer_config)

# Fetch stock data
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
SYMBOL = 'IBM'
URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={SYMBOL}&interval=5min&apikey={API_KEY}'
response = requests.get(URL)
data = response.json()

# Delivery report callback for produced messages
def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# Produce messages to the 'topic_0'
topic = 'topic_0'
message_count = 0
max_messages = 300 # Set the maximum number of messages to send

try:
    for timestamp, values in data['Time Series (5min)'].items():
        if message_count >= max_messages:
            print("Reached maximum number of messages. Stopping producer.")
            break
        
        record_key = timestamp
        record_value = json.dumps(values)
        producer.produce(topic, key=record_key, value=record_value, callback=delivery_report)
        producer.poll(1)
        message_count += 1

except Exception as e:
    print(f'Failed to produce message: {e}')

producer.flush()
