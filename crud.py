from sqlalchemy.orm import Session
from models import Client, Product, Supplier, Image, Address
# УБРАЛ import schemas - он не нужен здесь

# CLIENT OPERATIONS
def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Client).offset(skip).limit(limit).all()

def get_clients_by_name(db: Session, name: str, surname: str):
    return db.query(Client).filter(
        Client.client_name == name, 
        Client.client_surname == surname
    ).all()

def create_client(db: Session, client_data: dict):  # ИЗМЕНИЛ ТИП
    db_client = Client(**client_data)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
    return client

def update_client_address(db: Session, client_id: int, address_id: int):
    client = db.query(Client).filter(Client.id == client_id).first()
    if client:
        client.address_id = address_id
        db.commit()
        db.refresh(client)
    return client

# PRODUCT OPERATIONS
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product_data: dict):  # ИЗМЕНИЛ ТИП
    db_product = Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product

def decrease_product_stock(db: Session, product_id: int, decrease_by: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.available_stock -= decrease_by
        db.commit()
        db.refresh(product)
    return product

# SUPPLIER OPERATIONS
def get_supplier(db: Session, supplier_id: int):
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def get_suppliers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Supplier).offset(skip).limit(limit).all()

def create_supplier(db: Session, supplier_data: dict):  # ИЗМЕНИЛ ТИП
    db_supplier = Supplier(**supplier_data)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def delete_supplier(db: Session, supplier_id: int):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if supplier:
        db.delete(supplier)
        db.commit()
    return supplier

def update_supplier_address(db: Session, supplier_id: int, address_id: int):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if supplier:
        supplier.address_id = address_id
        db.commit()
        db.refresh(supplier)
    return supplier

# IMAGE OPERATIONS
def get_image(db: Session, image_id: str):
    return db.query(Image).filter(Image.id == image_id).first()

def get_image_by_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product and product.image_id:
        return db.query(Image).filter(Image.id == product.image_id).first()
    return None

def create_image(db: Session, image_id: str, image_data: bytes):
    db_image = Image(id=image_id, image=image_data)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def update_image(db: Session, image_id: str, new_image_data: bytes):
    image = db.query(Image).filter(Image.id == image_id).first()
    if image:
        image.image = new_image_data
        db.commit()
        db.refresh(image)
    return image

def delete_image(db: Session, image_id: str):
    image = db.query(Image).filter(Image.id == image_id).first()
    if image:
        db.delete(image)
        db.commit()
    return image