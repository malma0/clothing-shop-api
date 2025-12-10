import grpc
import sys
import os

sys.path.append('/home/malyugin-m-e/auth_service')

import auth_pb2
import auth_pb2_grpc

class AuthClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)
    
    def validate_token(self, token):
        try:
            response = self.stub.ValidateToken(
                auth_pb2.TokenRequest(token=token)
            )
            return response.valid, response.user_id, response.email
        except grpc.RpcError as e:
            print(f"gRPC error: {e}")
            return False, None, None
    
    def register(self, email, password, first_name="", last_name="", phone=""):
        try:
            response = self.stub.Register(
                auth_pb2.RegisterRequest(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone
                )
            )
            return response.success, response.token, response.message, response.user_id
        except grpc.RpcError as e:
            print(f"gRPC error: {e}")
            return False, None, str(e), None
    
    def login(self, email, password):
        try:
            response = self.stub.Login(
                auth_pb2.LoginRequest(
                    email=email,
                    password=password
                )
            )
            return response.success, response.token, response.message, response.user_id
        except grpc.RpcError as e:
            print(f"gRPC error: {e}")
            return False, None, str(e), None
    
    def change_password(self, email, old_password, new_password):
        try:
            response = self.stub.ChangePassword(
                auth_pb2.ChangePasswordRequest(
                    email=email,
                    old_password=old_password,
                    new_password=new_password
                )
            )
            return response.success, response.message
        except grpc.RpcError as e:
            print(f"gRPC error: {e}")
            return False, str(e)
    
    def reset_password(self, email):
        try:
            response = self.stub.ResetPassword(
                auth_pb2.ResetPasswordRequest(email=email)
            )
            return response.success, response.message, response.new_password
        except grpc.RpcError as e:
            print(f"gRPC error: {e}")
            return False, str(e), None
