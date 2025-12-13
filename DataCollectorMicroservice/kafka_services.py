from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from datetime import datetime
import json
import os

topic1 = 'to-alert-system'
topic2 = 'to-notifier'
timestamp = ""

value = "Aggiornamento dei voli effettuato"
message = {'timestamp': datetime.now().isoformat(), 'value': value}

bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka_examples:9092')

producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'acks': 'all',
    'retries': 3,
    'linger.ms': 10,
}

def return_message(utente, airport, condition):
    return {'utente': utente, 'airport': airport, 'condition': condition }

def create_producer():
    return Producer(producer_config)

def create_consumer(group_id):
    consumer_config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,
        'max.poll.interval.ms': 300000,
    }
    return Consumer(consumer_config)


def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}", flush=True)
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}", flush=True)


def delivery_messagge(producer, topic, message):
    payload = json.dumps(message).encode('utf-8')
    producer.produce(
        topic,
        payload,
        callback=delivery_report
    )
    producer.poll(0)
    producer.flush()

def decode_timestamp(consumer, msg):
    global timestamp
    data = json.loads(msg.value().decode('utf-8'))
    received_timestamp = data.get('timestamp')
    timestamp = received_timestamp
    consumer.commit(asynchronous=False)
    return True

def decode_message(consumer, msg):
    data = json.loads(msg.value().decode('utf-8'))
    utente = data.get('utente')
    airport = data.get('airport')
    condition = data.get('condition')
    consumer.commit(asynchronous=False)
    return utente, airport, condition

def check_message_kafka(consumer, name):
    global timestamp
    try:
            msg = consumer.poll(1.0)
            if msg is None:
                return False
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    return False
                else:
                    return False
            try:
                if name == 1:
                    return decode_timestamp(consumer, msg)
                else:
                    return decode_message(consumer, msg)
            except (json.JSONDecodeError, KeyError) as e:
                consumer.commit(asynchronous=False)
                return False
    except KeyboardInterrupt:
        return False


