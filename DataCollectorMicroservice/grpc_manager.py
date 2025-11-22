from opensky_api import OpenSkyApi
import time
import grpc
import testCred
import DatabaseManager as db
from concurrent import futures
import service_pb2
import service_pb2_grpc

def get_stub():
    channel = grpc.insecure_channel('server:50051')
    stub = service_pb2_grpc.UserServiceStub(channel)
    return stub

class Servicer(service_pb2_grpc.UserServiceServicer):
    def __init__(self):
        print("Ci siamo")

    def sendInterests(self, request, context):
        email = request.email
        airport_code = request.airport_code
        mode = request.mode
        request = db.insertInterests(email, airport_code, mode)
        if request == 1:
            return service_pb2.UserResponse(
                status=0,
                message="Inserimento dell interesse eseguito egregiamente"
            )
        else:
            return service_pb2.UserResponse(
                status=1,
                message="Inserimento dell interesse fallito malamente"
                )


