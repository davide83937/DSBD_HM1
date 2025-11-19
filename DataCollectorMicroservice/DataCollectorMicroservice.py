from opensky_api import OpenSkyApi
import time
import grpc
import testCred
import DatabaseManager


api = OpenSkyApi()
db = DatabaseManager.dataManager()
#lista_arrivi = []
#lista_arrivi.extend(testCred.getArrives(api))
#print("LISTA ARRIVI --------------------------------------------------------------------------------")
#print(lista_arrivi[0])
#print("--------------------------------------------------------------------------------------------")

#Al momento abbiamo i dati nel DB
#lista_partenze = []
#lista_partenze.extend(testCred.getDepartures(api))
#db.insertOnDatabase(lista_partenze)



