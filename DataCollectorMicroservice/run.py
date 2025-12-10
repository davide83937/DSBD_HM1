import time
import kafka_services as k
from flask import Flask
from DataCollectorMicroservice import app
import threading
import DatabaseManager as db

CLIENT_ID = "davidepanto@gmail.com-api-client"
CLIENT_SECRET = "ewpHTQ27KoTGv4vMoCyLT8QrIt4sLr3z"

consumer = k.create_consumer()
consumer.subscribe([k.topic1])

def background_cancelling_flights():
    while True:
        db.delete_old_flights()
        time.sleep(43200)

def backgroung_downloading_flights():
    while True:
        db.download_flights(CLIENT_ID, CLIENT_SECRET)
        time.sleep(30)

def start_downloading_flights():
    worker = threading.Thread(target=backgroung_downloading_flights)
    worker.daemon = True
    worker.start()



def start_cancelling_task():
    worker = threading.Thread(target=background_cancelling_flights)
    worker.daemon = True
    worker.start()

def background_update_timestamp_update():
    while True:
        k.check_message_kafka(consumer)
        time.sleep(60)

def start_update_timestamp():
    worker = threading.Thread(target=background_update_timestamp_update)
    worker.daemon = True
    worker.start()




appl = Flask(__name__)
appl.register_blueprint(app)

if __name__ == "__main__":
    start_cancelling_task()
    start_downloading_flights()
    start_update_timestamp()
    appl.run(host='0.0.0.0', port=5005, debug=True, use_reloader=False)
