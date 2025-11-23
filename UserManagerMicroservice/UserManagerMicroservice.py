import hashlib
from flask import request
from flask import Blueprint
import DbManager as db

app = Blueprint('app', __name__)

def sha512_hash(s: str) -> str:
    return hashlib.sha512(s.encode()).hexdigest()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]
    response = db.check_user(email)
    if response == 1:
        response = db.login(email, password, True)
        if response == 0:
            return {"message": "Login effettuato con successo"}, 200
        elif response == 2:
            return {"message": "Utente gia loggato"}, 407
        elif response == -1:
            return {"message": "Qualcosa è andato storto"}, 404
        elif response == 1:
            return {"message": "Qualcosa è andato storto"}, 409
    else:
        return {"message": "L'utente non esiste"}, 408




@app.route("/registrazione", methods=["POST"])
def registrazione():
    data = request.json
    email = data["email"]
    username = data["username"]
    password = data["password"]
    response = db.check_user(email)
    if response == 0:
        response = db.registrazione(email, username, password)
        if response == 0:
            return {"message": "Registrazione andata a buon fine"}, 200
        else:
            return {"message": "Qualcosa è andato storto"}, 404
    else:
        return {"message": "Utente già registrato"}, 409


@app.route("/cancellazione", methods=["POST"])
def cancellazione():
    data = request.json
    email = data["email"]
    password = data["password"]
    response = db.check_user(email)
    if response == 1:
        response = db.login(email, password, False)
        if response == 0:
           response = db.cancellazione(email)
           if response == 0:
               db.cancellazione_sessione(email)
               return {"message": "cancellazione andata a buon fine"}, 200
           else:
               return {"message": "qualcosa è andato storto"}, 404
        else:
            return {"message": "password errata"}, 405
    else:
        return {"message": "utente non esistente"}, 409




