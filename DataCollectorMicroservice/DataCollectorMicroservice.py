from opensky_api import OpenSkyApi
import time
import grpc
import testCred
import DatabaseManager

CLIENT_ID = "davidepanto@gmail.com-api-client"
CLIENT_SECRET = "ewpHTQ27KoTGv4vMoCyLT8QrIt4sLr3z"
AIRPORT = "LIRF"
ARRIVAL = "arrival"
DEPARTURE = "departure"


#api = OpenSkyApi()
db = DatabaseManager.dataManager()
token = testCred.get_token(CLIENT_ID, CLIENT_SECRET)

lista_arrivi = []
start_time, end_time = testCred.get_data("2025-11-19 18:00:00".strip())
lista_arrivi.extend(testCred.get_info_flight(token, AIRPORT, start_time, end_time, ARRIVAL))
#print("LISTA ARRIVI --------------------------------------------------------------------------------")
#print(lista_arrivi)
#print("--------------------------------------------------------------------------------------------")

db.insertOnDatabase(lista_arrivi,"Flight_Data_Arrives")

lista_partenze = []
start_time, end_time = testCred.get_data("2025-11-19 12:00:00".strip())
lista_partenze.extend(testCred.get_info_flight(token, AIRPORT, start_time, end_time, DEPARTURE))
#print("LISTA PARTENZE --------------------------------------------------------------------------------")
#print(lista_partenze)
#print("--------------------------------------------------------------------------------------------")


db.insertOnDatabase(lista_partenze, "Flight_Data_Departures")



