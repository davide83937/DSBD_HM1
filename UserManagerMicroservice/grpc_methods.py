from http.client import responses
from concurrent import futures

import grpc
import service_pb2
import service_pb2_grpc
import DbManager as db

def get_stub():
    channel = grpc.insecure_channel('server:50051')
    stub = service_pb2_grpc.UserServiceStub(channel)
    return stub


class Servicer(service_pb2_grpc.UserServiceServicer):
    def __init__(self):
        print("Ci siamo")

    def checkUser(self, request, context):
        email = request.email
        response = db.check_logging(email)
        if response == 0:
            return service_pb2.UserResponse(
                status=0,
                message="L'utente è loggato"
            )
        else:
            return service_pb2.UserResponse(
                status=1,
                message="Non so chi sia costui"
            )


def serve():
    """
    Start the gRPC server and listen for incoming requests.
    Server runs on port 50051.
    """
    # Create a gRPC server with thread pool
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register our service implementation
    service_pb2_grpc.add_UserServiceServicer_to_server(
        Servicer(), server
    )

    # Listen on port 50051
    port = "50051"
    server.add_insecure_port(f"[::]:{port}")

    # Start the server
    server.start()
    print(f"Server started on port {port}")
    print("Waiting for client requests...")
    print("")

    # Keep server running
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
