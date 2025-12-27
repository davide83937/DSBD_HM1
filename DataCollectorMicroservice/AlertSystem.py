import kafka_services as k
import threading
import time
import DatabaseManager as db

NAME = 1

consumer = k.create_consumer("alert-group-v5", k.topic1)
consumer.subscribe([k.topic1])

producer = k.create_producer()

def background_timestamp_update():
  try:
    while True:
        print("DEBUG: Alert System in attesa di messaggi...", flush=True)  # AGGIUNGI QUESTA
        result = k.check_message_kafka(consumer, NAME)
        if result:
            print(f"Messaggio ricevuto! Controllo voli per l'aeroporto...", flush=True)
            alert = []
            alert = db.check_flight_conditions()
            for a in alert:
                message = k.return_message(a['email'], a['airport'], a['condition'])
                k.delivery_messagge(producer, k.topic2, message)
        time.sleep(5)
  except KeyboardInterrupt:
      print("Interruzione manuale ricevuta. Chiusura in corso...")
  except Exception as e:
      print(f"Errore critico nel loop: {e}")
  finally:
      consumer.close()

if __name__ == "__main__":
    background_timestamp_update()
