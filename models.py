from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, Text, ForeignKey, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)


class Image(Base):
    __tablename__ = 'images'
    id = Column(String, primary_key=True, index=True)
    image = Column(BLOB, nullable=False)


class Supplier(Base):
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))
    phone_number = Column(String, nullable=False)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    available_stock = Column(Integer, nullable=False)
    last_update_date = Column(Date, nullable=False)
    supplier_id = Column(Integer, ForeignKey('supplier.id'))
    image_id = Column(String, ForeignKey('images.id'))


class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    client_surname = Column(String, nullable=False)
    birthday = Column(Date)
    gender = Column(String)
    registration_date = Column(Date, nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))