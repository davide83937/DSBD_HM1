import time
import kafka_services as k
from flask import Flask
from DataCollectorMicroservice import app
import threading
import DatabaseManager as db
from circuit_breaker import CircuitBreakerOpenException

CLIENT_ID = "davidepanto@gmail.com-api-client"
CLIENT_SECRET = "ewpHTQ27KoTGv4vMoCyLT8QrIt4sLr3z"
NAME = 1

consumer = k.create_consumer("group1")
consumer.subscribe([k.topic1])

polling_config = {"interval": 43200}
MODE_MAIN = "MAIN"
MODE_FALLBACK = "FALLBACK"
api_mode = MODE_MAIN


def set_polling_interval(seconds):
    global polling_config
    if polling_config["interval"] != seconds:
        print(f"Cambio intervallo polling: {polling_config['interval']}s -> {seconds}s.", flush=True)
        polling_config["interval"] = seconds



def background_cancelling_flights():
    while True:
        db.delete_old_flights()
        time.sleep(43200)

def backgroung_downloading_flights():
    global api_mode
    while True:
        try:
            if api_mode == MODE_MAIN:
                print("Modalità MAIN: Tentativo di download completo.", flush=True)
                db.download_flights(CLIENT_ID, CLIENT_SECRET)
                set_polling_interval(43200)
            elif api_mode == MODE_FALLBACK:
                print("Modalità FALLBACK: Tentativo di check veloce (polling 60s).", flush=True)
                success = db.check_fallback_api(CLIENT_ID, CLIENT_SECRET)
                if success:
                    print("Fallback API SUCCESS. Ritorno alla modalità MAIN.", flush=True)
                    api_mode = MODE_MAIN
                    set_polling_interval(43200)
                else:
                    set_polling_interval(60)
        except CircuitBreakerOpenException:
           print("Circuit Breaker OPEN. Passaggio immediato alla modalità FALLBACK.", flush=True)
           api_mode = MODE_FALLBACK
           set_polling_interval(60)
        except Exception as e:
           print(f"Errore generale nel loop: {e}", flush=True)
           set_polling_interval(60)
        time.sleep(polling_config["interval"])

def start_downloading_flights():
    worker = threading.Thread(target=backgroung_downloading_flights)
    worker.daemon = True
    worker.start()


def start_cancelling_task():
    worker = threading.Thread(target=background_cancelling_flights)
    worker.daemon = True
    worker.start()

def background_update_timestamp_update():
    try:
        while True:
            k.check_message_kafka(consumer, NAME)
            time.sleep(5)
    except KeyboardInterrupt:
        print("Interruzione manuale ricevuta. Chiusura in corso...")
    except Exception as e:
        print(f"Errore critico nel loop: {e}")
    finally:
        consumer.close()



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
