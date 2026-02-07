import hashlib
import grpc
from flask import request
from flask import Blueprint
import DbManager as db
import grpc_methods
import service_pb2
import redis_script as rs
import metrics
import time


app = Blueprint('app', __name__)

def sha512_hash(s: str) -> str:
    return hashlib.sha512(s.encode()).hexdigest()

def sha256_hash(s: str) -> str:
    return hashlib.sha3_256(s.encode()).hexdigest()


@app.route("/", methods=["GET"])
def health_check():
    return {"status": "OK"}, 200

@app.route("/login", methods=["POST"])
def login():
    success = False
    fail_reason = "unknown_error"
    try:
        start_chiamata = time.perf_counter()
        valore = 0
        data = request.json
        email = data["email"]
        password = data["password"]
        password = sha512_hash(password)
        response = db.check_user(email)
        if response == 1:
            response = db.login(email, password, True)
            if response == 0:
                valore = time.perf_counter() - start_chiamata
                metrics.LOGIN_LATENCY.labels(
                    service='usermanager',
                    node=metrics.NODE_NAME,
                    resource='login_latency'
                ).set(valore)
                success = True
                return {"message": "Login effettuato con successo"}, 200
            elif response == 2:
                fail_reason = "already_logged"
                return {"message": "Utente gia loggato"}, 407
            elif response == -1:
                fail_reason = "db_internal_error"
                return {"message": "Qualcosa è andato storto"}, 404
            elif response == 1:
                fail_reason = "wrong_credentials"
                return {"message": "Qualcosa è andato storto"}, 409
        else:
            fail_reason = "user_not_found"
            return {"message": "L'utente non esiste"}, 408
    except grpc.RpcError as e:
       fail_reason = "grpc_error"
       e = e.code()
       if e == grpc.StatusCode.UNAVAILABLE:
         return {"message": f"Il canale grpc è spento o irraggiungibile: {e}"}, 503
    except KeyError as e:
        fail_reason = "missing_input"
        campo_mancante = e.args[0]
        return {"error": f"Manca il campo obbligatorio: {campo_mancante}"}, 400
    finally:
        if not success:
            metrics.LOGIN_COUNTER.labels(
                service='usermanager',
                node=metrics.NODE_NAME,
                resource=fail_reason  #
            ).inc(1)

@app.route("/registrazione", methods=["POST"])
def registrazione():
    try:
        data = request.json
        email = data["email"]
        username = data["username"]
        password = data["password"]
        password = sha512_hash(password)
        hash_mail = sha256_hash(email)
        response = rs.check_request(hash_mail)
        if response == 0:
            return {"message": "Registrazione andata a buon fine"}, 200
        response = db.check_user(email)
        if response == 0:
            response = db.registrazione(email, username, password)
            if response == 0:
                rs.insert_request(hash_mail, username)
                return {"message": "Registrazione andata a buon fine"}, 200
            else:
                return {"message": "Qualcosa è andato storto"}, 404
        else:
            return {"message": "Utente già registrato"}, 409
    except grpc.RpcError as e:
       e = e.code()
       if e == grpc.StatusCode.UNAVAILABLE:
         return {"message": f"Il canale grpc è spento o irraggiungibile: {e}"}, 503
    except KeyError as e:
        campo_mancante = e.args[0]
        return {"error": f"Manca il campo obbligatorio: {campo_mancante}"}, 400


@app.route("/cancellazione", methods=["POST"])
def cancellazione():
    try:
        data = request.json
        email = data["email"]
        password = data["password"]
        password = sha512_hash(password)
        response = db.check_user(email)
        if response == 1:
            response = db.login(email, password, False)
            if response == 0:
               response = db.cancellazione(email)
               if response == 0:
                   db.cancellazione_sessione(email)
                   stub = grpc_methods.get_stub()
                   stub.delete_interestes_by_email(service_pb2.UserCheckMessage(email=email))
                   return {"message": "cancellazione andata a buon fine"}, 200
               else:
                   return {"message": "qualcosa è andato storto"}, 404
            else:
                return {"message": "password errata"}, 405
        else:
            return {"message": "utente non esistente"}, 409
    except grpc.RpcError as e:
       e = e.code()
       if e == grpc.StatusCode.UNAVAILABLE:
         return {"message": f"Il canale grpc è spento o irraggiungibile: {e}"}, 503
    except KeyError as e:
        campo_mancante = e.args[0]
        return {"error": f"Manca il campo obbligatorio: {campo_mancante}"}, 400



