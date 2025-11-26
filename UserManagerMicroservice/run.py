import time
import threading

from flask import Flask
from UserManagerMicroservice import app
import DbManager as db


def background_cancelling_request():
    while True:
        db.delete_old_request()
        time.sleep(70)

def start_cancelling_request():
    print("Sto cancellando")
    worker = threading.Thread(target=background_cancelling_request)
    worker.daemon = True
    worker.start()

appl = Flask(__name__)
appl.register_blueprint(app)

if __name__ == "__main__":
    #appl.run(host='0.0.0.0', port=5000)
    start_cancelling_request()
    appl.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

