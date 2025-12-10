import kafka_services as k
import threading
import time
import DatabaseManager as db
from DataCollectorMicroservice.kafka_services import message

consumer = k.create_consumer()
consumer.subscribe([k.topic1])

producer = k.create_producer()

def background_update_timestamp_update():
    while True:
        result = k.check_message_kafka(consumer)
        if result:
            alert = []
            alert = db.check_flight_conditions()
            for a in alert:
                message = k.return_message(a['email'], a['airport'], a['condition'])
                k.delivery_messagge(producer, k.topic2, message)
        time.sleep(5)

def start_update_timestamp():
    worker = threading.Thread(target=background_update_timestamp_update)
    worker.daemon = True
    worker.start()