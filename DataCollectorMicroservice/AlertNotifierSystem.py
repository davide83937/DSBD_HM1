import time
import kafka_services as k
import email_manager as mail

NAME = 2

consumer = k.create_consumer("notifier-group", k.topic2)
consumer.subscribe([k.topic2])

def watch_kafka():
  try:
    while True:
        result = k.check_message_kafka(consumer, NAME)
        if result is not False:
            utente, airport, condition = result
            corpo = mail.make_corpo(utente, airport, condition)
            mail.send_email(utente, corpo)
        time.sleep(1)
  except KeyboardInterrupt:
    print("Interruzione manuale ricevuta. Chiusura in corso...")
  except Exception as e:
    print(f"Errore critico nel loop: {e}")
  finally:
    consumer.close()


if __name__ == "__main__":
    watch_kafka()

