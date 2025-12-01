import redis
import os

redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

def insert_request(email_hash, username):
    try:
       r.set(email_hash, username, ex=60)
    except redis.ConnectionError:
        print("Errore: Impossibile connettersi a Redis. Assicurati che il server sia attivo!")

def check_request(email_hash):
    if r.exists(email_hash):
        return 0
    else:
        return 1