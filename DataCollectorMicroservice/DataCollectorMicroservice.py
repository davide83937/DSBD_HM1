import DatabaseManager as db
import service_pb2
from flask import request, jsonify
from flask import Blueprint
import grpc_manager
import testCred


app = Blueprint('app', __name__)

CLIENT_ID = "davidepanto@gmail.com-api-client"
CLIENT_SECRET = "ewpHTQ27KoTGv4vMoCyLT8QrIt4sLr3z"
AIRPORT = "LIRF"
ARRIVAL = "arrival"
DEPARTURE = "departure"

@app.route("/send_interest", methods=["POST"])
def sendInterest():
    data = request.json
    email = data["email"]
    stub = grpc_manager.get_stub()
    response = stub.checkUser(service_pb2.UserCheckMessage(email=email))
    if response.status == 0:
        airport = data["airport_code"]
        mode = data["mode"]
        response = db.insertInterests(email, airport, mode)
        if response == 0:
            return {"message": "Inserimento inserito"}
        else:
            return {"message": "Inserimento non inserito"}
    else:
        return {"message": "Utente non loggato"}


@app.route("/delete_interest", methods=["POST"])
def delete_interest():
    data = request.json
    email = data["email"]
    stub = grpc_manager.get_stub()
    response = stub.checkUser(service_pb2.UserCheckMessage(email=email))
    if response.status == 0:
        airport = data["airport_code"]
        mode = data["mode"]
        response = db.deleteInterest(email, airport, mode)
        if response == 0:
            return {"message": "Eliminazione riuscita"}, 200
        else:
            return {"message": "Eliminazione non riuscita"}, 404
    else:
        return {"message": "Utente non loggato"}, 409

@app.route("/get_info", methods=["POST"])
def get_info():
    data = request.json
    email = data["email"]
    stub = grpc_manager.get_stub()
    response = stub.checkUser(service_pb2.UserCheckMessage(email=email))
    if response.status == 0:
        airport = data["airport_code"]
        mode = data["mode"]
        response = db.get_flight_by_airport(airport, mode)
        lista_voli_json = []
        for riga in response:
            lista_voli_json.append({
                "partenza": riga[0],
                "ora_arrivo": riga[1],
                "ora_partenza": riga[2],
                "arrivo": str(riga[3]),
                "codice": str(riga[4])
            })

        # 2. Restituiamo il JSON con status 200 (OK)
        return {
            "count": len(lista_voli_json),
            "voli": lista_voli_json
        }, 200

    else:
        # Se l'utente non è loggato
        return {"message": "Utente non autorizzato o non loggato"}, 401


@app.route("/get_last", methods=["POST"])
def get_last_one():
    data = request.json
    email = data["email"]
    stub = grpc_manager.get_stub()
    response = stub.checkUser(service_pb2.UserCheckMessage(email=email))
    if response.status == 0:
        airport = data["airport_code"]
        last_arrival, last_departure = db.get_last_one(airport)
        response = [last_arrival, last_departure]
        lista_voli_json = []
        for riga in response:
            if riga is None:
                continue
            lista_voli_json.append({
                "partenza": riga[0],  # Assumo indice 0 = Airport
                "ora_arrivo": riga[1],  # Assumo indice 1 = Flight_code
                "ora_partenza": riga[2],  # Assumo indice 2 = Final_Airport
                "arrivo": str(riga[3]),  # Convertiamo datetime in stringa
                "codice": str(riga[4])
            })

        # 2. Restituiamo il JSON con status 200 (OK)
        return {
            "count": len(lista_voli_json),
            "voli": lista_voli_json
        }, 200

    else:
        # Se l'utente non è loggato
        return {"message": "Utente non autorizzato o non loggato"}, 401

@app.route("/get_avgs", methods=["POST"])
def get_avgs():
    data = request.json
    email = data["email"]
    stub = grpc_manager.get_stub()
    response = stub.checkUser(service_pb2.UserCheckMessage(email=email))
    if response.status == 0:
        airport = data["airport_code"]
        n_days = data["n_days"]
        arrival_avg, departure_avg = db.get_average_flights(airport, n_days)
        return {
            "media arrivi": arrival_avg,
            "media partenze": departure_avg
        }, 200

    else:
        # Se l'utente non è loggato
        return {"message": "Utente non autorizzato o non loggato"}, 401

#api = OpenSkyApi()

"""token = testCred.get_token(CLIENT_ID, CLIENT_SECRET)

lista_arrivi = []
start_time, end_time = testCred.get_data("2025-11-21 18:00:00".strip())
lista_arrivi.extend(testCred.get_info_flight(token, AIRPORT, start_time, end_time, ARRIVAL))
print("LISTA ARRIVI --------------------------------------------------------------------------------")
print(lista_arrivi)
print("--------------------------------------------------------------------------------------------")"""

#db.insertOnDatabase(lista_arrivi, "Flight_Data_Arrives")
"""
lista_partenze = []
start_time, end_time = testCred.get_data("2025-11-21 12:00:00".strip())
lista_partenze.extend(testCred.get_info_flight(token, AIRPORT, start_time, end_time, DEPARTURE))
print("LISTA PARTENZE --------------------------------------------------------------------------------")
print(lista_partenze)
print("--------------------------------------------------------------------------------------------")


#db.insertOnDatabase(lista_partenze, "Flight_Data_Departures")
"""



