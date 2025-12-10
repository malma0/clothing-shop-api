from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Создаем подключение к SQLite базе
SQLALCHEMY_DATABASE_URL = "sqlite:///./shop.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем таблицы если их нет
Base.metadata.create_all(bind=engine)
