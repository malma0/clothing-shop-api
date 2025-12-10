from pydantic import BaseModel
from typing import Optional
from datetime import date


# Базовые схемы
class AddressBase(BaseModel):
    country: str
    city: str
    street: str


class ClientBase(BaseModel):
    client_name: str
    client_surname: str
    birthday: Optional[date] = None
    gender: Optional[str] = None
    registration_date: date


# Схемы для создания (CREATE)
class ClientCreate(ClientBase):
    address: AddressBase


class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    available_stock: int
    supplier_id: int
    image_id: str


# Схемы для ответа (RESPONSE)
class ClientResponse(ClientBase):
    id: int
    address: AddressBase

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    available_stock: int
    last_update_date: date

    class Config:
        from_attributes = True
class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_info: Optional[str] = None
    
    class Config:
        from_attributes = True
class SupplierResponse(BaseModel):
    id: int
    name: str
    contact_info: Optional[str] = None
    
    class Config:
        from_attributes = True
