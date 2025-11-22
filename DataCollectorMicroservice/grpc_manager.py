import grpc
import service_pb2_grpc

def get_stub():
    channel = grpc.insecure_channel('server:50051')
    stub = service_pb2_grpc.UserServiceStub(channel)
    return stub






