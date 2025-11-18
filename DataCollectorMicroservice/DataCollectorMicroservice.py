from opensky_api import OpenSkyApi
import time
import grpc
import testCred

api = OpenSkyApi()
lista = []
lista.append(testCred.getDepartures(api))
print(lista[0])


