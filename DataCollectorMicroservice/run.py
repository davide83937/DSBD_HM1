import time

from flask import Flask
from DataCollectorMicroservice import app
import threading
import DatabaseManager as db

CLIENT_ID = "davidepanto@gmail.com-api-client"
CLIENT_SECRET = "ewpHTQ27KoTGv4vMoCyLT8QrIt4sLr3z"

def background_cancelling_flights():
    while True:
        db.delete_old_flights()
        time.sleep(43200)

def backgroung_downloading_flights():
    while True:
        db.download_flights(CLIENT_ID, CLIENT_SECRET)
        time.sleep(43200)

def start_downloading_flights():
    # Crea il thread puntando alla funzione definita sopra
    worker = threading.Thread(target=backgroung_downloading_flights)
    # daemon=True significa che il thread muore quando spegni il server Flask
    worker.daemon = True
    worker.start()



def start_cancelling_task():
    # Crea il thread puntando alla funzione definita sopra
    worker = threading.Thread(target=background_cancelling_flights)
    #daemon=True significa che il thread muore quando spegni il server Flask
    worker.daemon = True
    worker.start()


appl = Flask(__name__)
appl.register_blueprint(app)

if __name__ == "__main__":
    # Avvia il worker
    start_cancelling_task()
    start_downloading_flights()
    # Avvia Flask (il server web)
    # Nota: use_reloader=False è importante se usi i thread in debug mode,
    # altrimenti Flask ne avvia due copie!
    appl.run(port=5005, debug=True, use_reloader=False)
