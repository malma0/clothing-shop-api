import grpc
from concurrent import futures
import time
import uuid
from datetime import datetime, timedelta
import jwt
from passlib.hash import pbkdf2_sha256  # ИЗМЕНИЛ НА pbkdf2_sha256
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import auth_pb2
import auth_pb2_grpc
from auth.db_sqlite import SessionLocal, User

SECRET_KEY = "your-secret-key-for-jwt-tokens-12345"

class AuthServicer(auth_pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        db = SessionLocal()
        try:
            existing = db.query(User).filter(User.email == request.email).first()
            if existing:
                return auth_pb2.AuthResponse(
                    success=False, 
                    message="User with this email already exists"
                )
            
            # pbkdf2_sha256 не имеет ограничения 72 байта
            password_hash = pbkdf2_sha256.hash(request.password)
            
            user = User(
                id=str(uuid.uuid4()),
                email=request.email,
                first_name=request.first_name,
                last_name=request.last_name,
                phone=request.phone,
                password_hash=password_hash
            )
            
            db.add(user)
            db.commit()
            
            token = jwt.encode({
                "sub": user.id,
                "email": user.email,
                "exp": datetime.utcnow() + timedelta(days=1)
            }, SECRET_KEY, algorithm="HS256")
            
            return auth_pb2.AuthResponse(
                success=True,
                token=token,
                message="Registration successful",
                user_id=user.id
            )
        except Exception as e:
            db.rollback()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return auth_pb2.AuthResponse()
        finally:
            db.close()
    
    def Login(self, request, context):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == request.email).first()
            if not user:
                return auth_pb2.AuthResponse(
                    success=False,
                    message="Invalid email or password"
                )
            
            if not pbkdf2_sha256.verify(request.password, user.password_hash):
                return auth_pb2.AuthResponse(
                    success=False,
                    message="Invalid email or password"
                )
            
            token = jwt.encode({
                "sub": user.id,
                "email": user.email,
                "exp": datetime.utcnow() + timedelta(days=1)
            }, SECRET_KEY, algorithm="HS256")
            
            return auth_pb2.AuthResponse(
                success=True,
                token=token,
                message="Login successful",
                user_id=user.id
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return auth_pb2.AuthResponse()
        finally:
            db.close()
    
    def ValidateToken(self, request, context):
        try:
            payload = jwt.decode(
                request.token, 
                SECRET_KEY, 
                algorithms=["HS256"]
            )
            return auth_pb2.ValidationResponse(
                valid=True,
                user_id=payload["sub"],
                email=payload["email"]
            )
        except jwt.ExpiredSignatureError:
            return auth_pb2.ValidationResponse(valid=False)
        except jwt.InvalidTokenError:
            return auth_pb2.ValidationResponse(valid=False)
    
    def ChangePassword(self, request, context):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == request.email).first()
            if not user:
                return auth_pb2.ChangePasswordResponse(
                    success=False,
                    message="User not found"
                )
            
            if not pbkdf2_sha256.verify(request.old_password, user.password_hash):
                return auth_pb2.ChangePasswordResponse(
                    success=False,
                    message="Incorrect old password"
                )
            
            user.password_hash = pbkdf2_sha256.hash(request.new_password)
            db.commit()
            
            return auth_pb2.ChangePasswordResponse(
                success=True,
                message="Password changed successfully"
            )
        finally:
            db.close()
    
    def ResetPassword(self, request, context):
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == request.email).first()
            if not user:
                return auth_pb2.ResetPasswordResponse(
                    success=False,
                    message="User not found"
                )
            
            import random
            import string
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            
            user.password_hash = pbkdf2_sha256.hash(new_password)
            db.commit()
            
            print(f"\nPassword reset for {request.email}")
            print(f"New password: {new_password}")
            print("(In production, this would be sent via email)\n")
            
            return auth_pb2.ResetPasswordResponse(
                success=True,
                message="New password generated. Check server console.",
                new_password=new_password
            )
        finally:
            db.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Auth SQLite gRPC server started on port 50051")
    print("Database: auth.db")
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        print("Server stopped")

if __name__ == '__main__':
    serve()
