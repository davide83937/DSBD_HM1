from flask import Flask, request
import DbManager as db

app = Flask(__name__)

"""@app.route("/ciao", methods=["GET"])
def hello():
    return {"msg": "ciao dal server"}
"""

@app.route("/registrazione", methods=["POST"])
def registrazione():
    data = request.json
    email = data["email"]
    username = data["username"]
    password = data["password"]
    response = db.check_user(email)
    if response == 0:
        #print("Possiamo procedere con la registrazione")
        response = db.registrazione(email, username, password)
        if response == 0:
            return {"message": "Registrazione andata a buon fine"}, 200
        else:
            return {"message": "Qualcosa è andato storto"}, 404
    else:
        return {"message": "utente già registrato"}, 409


@app.route("/cancellazione", methods=["POST"])
def cancellazione():
    data = request.json
    email = data["email"]
    password = data["password"]
    response = db.check_user(email)
    if response == 1:
        #print("Possiamo procedere con la cancellazione")
        response = db.login(email, password)
        if response == 0:
           response = db.cancellazione(email)
           if response == 0:
               return {"message": "cancellazione andata a buon fine"}, 200
           else:
               return {"message": "qualcosa è andato storto"}, 404
        else:
            return {"message": "password errata"}, 405
    else:
        return {"message": "utente non esistente"}, 409




app.run(port=5000)