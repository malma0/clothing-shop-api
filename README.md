# Магазин одежды — REST API + gRPC-сервис авторизации

Учебный backend интернет-магазина одежды. Каталог товаров, клиенты и поставщики доступны через REST API на FastAPI. Регистрация и вход вынесены в отдельный микросервис авторизации, с которым API общается по gRPC.

> **EN:** Clothing store backend: REST API on FastAPI with a separate gRPC authentication microservice (JWT, pbkdf2 password hashing), SQLAlchemy models for products, suppliers and clients.

## Архитектура

```
 клиент ──HTTP──▶  Shop API (FastAPI, :5000)  ──gRPC──▶  Auth Service (:50051)
                         │                                     │
                      shop.db (SQLite)                    SQLite (пользователи)
```

- **Shop API** (`main.py`): товары, клиенты, регистрация и вход. Зависимости подключаются через простой DI-контейнер (`ServiceContainer`).
- **Auth Service** (`auth_service/`): gRPC-сервер с методами `Register`, `Login`, `ValidateToken`, `ChangePassword`, `ResetPassword`. Выдаёт JWT, пароли хранит в виде хеша (pbkdf2_sha256).
- **Контракт** описан в `auth_service/proto/auth.proto`.

## Модель данных

`Address`, `Supplier`, `Product` (категория, цена, остаток, поставщик, изображение), `Image`, `Client`. Описание в `models.py`, CRUD-операции в `crud.py`.

## Стек

Python, FastAPI, SQLAlchemy, SQLite, gRPC (grpcio, protobuf), JWT (PyJWT), passlib.

## Запуск

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt pyjwt grpcio
pip install -r auth_service/requirements.txt

# 1. сервис авторизации (gRPC, порт 50051)
cd auth_service
python run_auth.py

# 2. в другом терминале: основное API (порт 5000)
python main.py
```

Swagger: http://localhost:5000/api/v1/docs

`simple_main.py` — минимальная версия API без базы данных, для проверки окружения.

Если нужно открывать API по адресу `shop.local`, добавь строку из `hosts_entry.txt` в системный файл `hosts`.

## Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/api/v1/` | проверка работы |
| POST | `/api/v1/register` | регистрация |
| POST | `/api/v1/auth` | вход, возвращает JWT |
| GET | `/api/v1/clients` | список клиентов |
| GET | `/api/v1/products` | каталог товаров |
