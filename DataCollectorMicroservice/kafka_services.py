from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from datetime import datetime
import json
import os

topic1 = 'to-alert-system'
topic2 = 'to-notifier'
timestamp = ""

value = "Aggiornamento dei voli effettuato"
message = {'timestamp': datetime.now().isoformat(), 'value': value}
def return_message(utente, airport, condition):
    return {'utente': utente, 'airport': airport, 'condition': condition }

# NOTA: Se sei dentro Docker, questo DEVE essere 'kafka_examples:9092'
# Se sei sul PC e lanci questo script fuori da Docker, usa 'localhost:29092'
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka_examples:9092')

producer_config = {
    'bootstrap.servers': bootstrap_servers,
    'acks': 'all',
    # 'batch.size': 500,  <-- RIMOSSO: troppo piccolo, rallenta tutto. Usa il default.
    'retries': 3,
    'linger.ms': 10,
}



def create_producer():
    return Producer(producer_config)


def create_consumer(group_id):
    consumer_config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': False,  # Commit manuale (ok, ma ricordati di farlo!)
        'max.poll.interval.ms': 300000,
    }
    return Consumer(consumer_config)


def delivery_report(err, msg):
    """ Callback chiamata per confermare l'invio """
    if err:
        print(f"Delivery failed: {err}", flush=True)
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}", flush=True)


def delivery_messagge(producer, topic, message):
    # 1. Serializzazione corretta in bytes
    payload = json.dumps(message).encode('utf-8')
    producer.produce(
        topic,
        payload,
        callback=delivery_report
    )
    # 2. IMPORTANTE: poll() serve a gestire le callback di conferma
    producer.poll(0)
    # 3. CRUCIALE: Forza l'invio immediato dei dati nel buffer
    producer.flush()
    print("Messaggio inviato (Flush completato)", flush=True)

def decode_timestamp(consumer, msg):
    global timestamp
    data = json.loads(msg.value().decode('utf-8'))
    received_timestamp = data.get('timestamp')
    timestamp = received_timestamp
    print(f"Ricevuto timestamp: {received_timestamp}", flush=True)
    # Commit manuale (perché hai enable.auto.commit = False)
    consumer.commit(asynchronous=False)
    print(f"Committed offset: {msg.offset()}\n", flush=True)
    return True

def decode_message(consumer, msg):
    data = json.loads(msg.value().decode('utf-8'))
    utente = data.get('utente')
    airport = data.get('airport')
    condition = data.get('condition')
    consumer.commit(asynchronous=False)
    return utente, airport, condition

def check_message_kafka(consumer, name):
    # 4. IMPORTANTE: Devi iscriverti al topic prima di fare poll!
    global timestamp
    #print(f"Consumer in ascolto su {topic1}...", flush=True)
    try:
            msg = consumer.poll(1.0)  # Attende 1 secondo
            if msg is None:
                return False

            if msg.error():
                # Usa KafkaError, non KafkaException per i codici
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # Non è un vero errore, solo fine dei dati vecchi
                    return False

                else:
                    print(f"Consumer error: {msg.error()}", flush=True)
                    return False

            try:
                # Decodifica
                #data = json.loads(msg.value().decode('utf-8'))
                #received_timestamp = data.get('timestamp')
                #timestamp = received_timestamp
                #print(f"Ricevuto timestamp: {received_timestamp}", flush=True)
                # Commit manuale (perché hai enable.auto.commit = False)
                #consumer.commit(asynchronous=False)
                #print(f"Committed offset: {msg.offset()}\n", flush=True)
                if name == 1:
                    return decode_timestamp(consumer, msg)
                else:
                    return decode_message(consumer, msg)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Malformed message at offset {msg.offset()}: {e}", flush=True)
                # Committiamo comunque per non bloccarci su un messaggio rotto all'infinito
                consumer.commit(asynchronous=False)
                return False
    except KeyboardInterrupt:
        print("Stop consumer...", flush=True)
        return False


def send_to_notifier(producer):
    print("")
