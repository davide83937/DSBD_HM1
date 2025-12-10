from confluent_kafka import Producer, Consumer, KafkaException
from datetime import datetime
import json

topic1 = 'TOPIC1'
timestamp = ""

producer_config = {
    'bootstrap.servers': 'localhost:29092',
    'acks': 'all',  # Maximum durability - waits for all in-sync replicas
    'batch.size': 500,  #just an example, use default (16KB) which is more efficient
    'max.in.flight.requests.per.connection': 1,  # Only one in-flight request,default (5) is balanced
    'retries': 3,  # Retry on transient errors
    'linger.ms': 10,  # Wait 10ms to batch messages (reduces overhead)
}

consumer_config = {
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'group2',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False,  # Manual commit for batch control
    'max.poll.interval.ms': 300000,  # 5 minutes timeout (important for batch processing)
}

def create_producer():
    producer = Producer(producer_config)
    return producer

def create_consumer():
    consumer = Consumer(consumer_config)
    return consumer

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def delivery_messagge(producer):
    value = "Aggiornamento dei voli effettuato"
    message = {'timestamp': datetime.now().isoformat(), 'value': value}
    producer.produce(
        topic1,
        json.dumps(message).encode('utf-8'),  # Explicit encoding
        callback=delivery_report
    )

def check_message_kafka(consumer):

    while True:
       msg = consumer.poll(1.0)

       if msg is None:
          continue

       if msg.error():
          if msg.error().code() == KafkaException._PARTITION_EOF:
            print(f"End of partition {msg.partition()}")
          else:
            print(f"Consumer error: {msg.error()}")
          continue

       try:
          data = json.loads(msg.value().decode('utf-8'))
          timestamp = data['timestamp']

          consumer.commit(asynchronous=False)
          print(f"Committed offset: {msg.offset()}\n")


       except (json.JSONDecodeError, KeyError) as e:
          print(f"Malformed message at offset {msg.offset()}: {e}")
          consumer.commit(msg)
          continue