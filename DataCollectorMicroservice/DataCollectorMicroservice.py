import DatabaseManager as db
import service_pb2
from flask import request
from flask import Blueprint
import grpc_manager

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



#api = OpenSkyApi()
"""
token = testCred.get_token(CLIENT_ID, CLIENT_SECRET)

lista_arrivi = []
start_time, end_time = testCred.get_data("2025-11-19 18:00:00".strip())
lista_arrivi.extend(testCred.get_info_flight(token, AIRPORT, start_time, end_time, ARRIVAL))"""
#print("LISTA ARRIVI --------------------------------------------------------------------------------")
#print(lista_arrivi)
#print("--------------------------------------------------------------------------------------------")

"""db.insertOnDatabase(lista_arrivi, "Flight_Data_Arrives")

lista_partenze = []
start_time, end_time = testCred.get_data("2025-11-19 12:00:00".strip())
lista_partenze.extend(testCred.get_info_flight(token, AIRPORT, start_time, end_time, DEPARTURE))"""
#print("LISTA PARTENZE --------------------------------------------------------------------------------")
#print(lista_partenze)
#print("--------------------------------------------------------------------------------------------")


#db.insertOnDatabase(lista_partenze, "Flight_Data_Departures")



