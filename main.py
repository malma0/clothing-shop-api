from fastapi import FastAPI, Depends, HTTPException, Header, UploadFile, File
from typing import Optional, List
from sqlalchemy.orm import Session
import crud
from database_session import SessionLocal
import jwt
from datetime import datetime, timedelta
import uuid

# ==================== DEPENDENCY INJECTION CONTAINER ====================
class ServiceContainer:
    def __init__(self):
        self._auth_service = None
        self._db_session = None
    
    @property
    def auth_service(self):
        if self._auth_service is None:
            self._auth_service = AuthService()
        return self._auth_service
    
    @property
    def db_session(self):
        if self._db_session is None:
            self._db_session = SessionLocal()
        return self._db_session
    
    def get_db(self):
        db = self.db_session
        try:
            yield db
        finally:
            db.close()

# Заглушка AuthService (вместо gRPC)
class AuthService:
    def __init__(self):
        self.secret_key = "test-secret-key-12345"
    
    def register(self, email, password, first_name=None, last_name=None, phone=None):
        user_id = str(uuid.uuid4())
        token = jwt.encode({
            "sub": user_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(days=1)
        }, self.secret_key, algorithm="HS256")
        
        return True, token, "Registration successful", user_id
    
    def login(self, email, password):
        user_id = str(uuid.uuid4())
        token = jwt.encode({
            "sub": user_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(days=1)
        }, self.secret_key, algorithm="HS256")
        
        return True, token, "Login successful", user_id
    
    def validate_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return True, payload["sub"], payload["email"]
        except:
            return False, None, None

# Создаем контейнер
container = ServiceContainer()

# ==================== FASTAPI APP ====================
app = FastAPI(
    title="Shop API",
    description="Магазин одежды с аутентификацией",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

# ==================== DEPENDENCIES ====================
def get_auth_service() -> AuthService:
    """Dependency для auth service"""
    return container.auth_service

def get_db() -> Session:
    """Dependency для базы данных"""
    db = container.db_session
    try:
        yield db
    finally:
        db.close()

async def verify_token(
    authorization: str = Header(None),
    auth_service: AuthService = Depends(get_auth_service)
) -> str:
    """Dependency для проверки токена"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token missing")
    
    token = authorization.split(" ")[1]
    valid, user_id, email = auth_service.validate_token(token)
    
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user_id

# ==================== PUBLIC ENDPOINTS ====================
@app.get("/api/v1/")
def api_v1():
    return {"API": "v1", "status": "working"}

@app.post("/api/v1/register")
async def register(
    email: str,
    password: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    phone: Optional[str] = None,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Регистрация пользователя"""
    success, token, message, user_id = auth_service.register(
        email, password, first_name, last_name, phone
    )
    
    return {
        "success": success,
        "token": token,
        "user_id": user_id,
        "message": message
    }

@app.post("/api/v1/auth")
async def login(
    email: str,
    password: str,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Авторизация пользователя"""
    success, token, message, user_id = auth_service.login(email, password)
    
    return {
        "success": success,
        "token": token,
        "user_id": user_id,
        "message": message
    }

# ==================== PROTECTED ENDPOINTS ====================
@app.get("/api/v1/test/{id}")
async def test(
    id: str,
    user_id: str = Depends(verify_token),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Тестовый защищенный эндпоинт"""
    return {
        "id": id,
        "test": "ok",
        "authenticated_user": user_id,
        "service_injected": str(auth_service)
    }

@app.get("/api/v1/clients")
async def read_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user_id: str = Depends(verify_token)
):
    """Получить всех клиентов"""
    clients = crud.get_clients(db, skip=skip, limit=limit)
    return {"clients": clients, "count": len(clients)}

@app.get("/api/v1/products")
async def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user_id: str = Depends(verify_token)
):
    """Получить все продукты"""
    products = crud.get_products(db, skip=skip, limit=limit)
    return {"products": products, "count": len(products)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
