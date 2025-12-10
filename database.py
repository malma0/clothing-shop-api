import sqlite3


def create_database():
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()

    # Создание таблицы address
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS address (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT NOT NULL,
        city TEXT NOT NULL,
        street TEXT NOT NULL
    )
    ''')

    # Создание таблицы images
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id TEXT PRIMARY KEY,
        image BLOB NOT NULL
    )
    ''')

    # Создание таблицы supplier
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS supplier (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address_id INTEGER NOT NULL,
        phone_number TEXT NOT NULL,
        FOREIGN KEY (address_id) REFERENCES address(id)
    )
    ''')

    # Создание таблицы product
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        available_stock INTEGER NOT NULL,
        last_update_date DATE NOT NULL,
        supplier_id INTEGER NOT NULL,
        image_id TEXT,
        FOREIGN KEY (supplier_id) REFERENCES supplier(id),
        FOREIGN KEY (image_id) REFERENCES images(id)
    )
    ''')

    # Создание таблицы client
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS client (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        client_surname TEXT NOT NULL,
        birthday DATE,
        gender TEXT,
        registration_date DATE NOT NULL,
        address_id INTEGER NOT NULL,
        FOREIGN KEY (address_id) REFERENCES address(id)
    )
    ''')

    # Вставка тестовых данных

    # Адреса
    cursor.executemany('''
    INSERT INTO address (country, city, street) VALUES (?, ?, ?)
    ''', [
        ('Россия', 'Москва', 'ул. Тверская, д. 1'),
        ('Россия', 'Санкт-Петербург', 'Невский пр-т, д. 25'),
        ('Россия', 'Новосибирск', 'ул. Ленина, д. 10'),
        ('Россия', 'Екатеринбург', 'ул. Мира, д. 15'),
        ('Россия', 'Казань', 'ул. Баумана, д. 5')
    ])

    # Поставщики
    cursor.executemany('''
    INSERT INTO supplier (name, address_id, phone_number) VALUES (?, ?, ?)
    ''', [
        ('ООО "Модная одежда"', 1, '+7 (495) 111-11-11'),
        ('ИП Иванов', 2, '+7 (812) 222-22-22'),
        ('ООО "Стиль и комфорт"', 3, '+7 (383) 333-33-33'),
        ('АО "ТекстильПро"', 4, '+7 (343) 444-44-44'),
        ('ИП Петрова', 5, '+7 (843) 555-55-55')
    ])

    # Изображения
    image_data = b'\xFF\xD8\xFF\xE0'
    cursor.executemany('''
    INSERT INTO images (id, image) VALUES (?, ?)
    ''', [
        ('550e8400-e29b-41d4-a716-446655440000', image_data),
        ('550e8400-e29b-41d4-a716-446655440001', image_data),
        ('550e8400-e29b-41d4-a716-446655440002', image_data),
        ('550e8400-e29b-41d4-a716-446655440003', image_data),
        ('550e8400-e29b-41d4-a716-446655440004', image_data),
        ('550e8400-e29b-41d4-a716-446655440005', image_data),
        ('550e8400-e29b-41d4-a716-446655440006', image_data)
    ])

    # Товары (одежда)
    cursor.executemany('''
    INSERT INTO product (name, category, price, available_stock, last_update_date, supplier_id, image_id) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', [
        ('Джинсы классические', 'Брюки', 2999.99, 50, '2024-01-15', 1, '550e8400-e29b-41d4-a716-446655440000'),
        ('Футболка хлопковая', 'Футболки', 899.99, 100, '2024-01-10', 2, '550e8400-e29b-41d4-a716-446655440001'),
        ('Куртка зимняя', 'Верхняя одежда', 7999.99, 25, '2024-01-12', 3, '550e8400-e29b-41d4-a716-446655440002'),
        ('Платье вечернее', 'Платья', 4599.99, 30, '2024-01-08', 4, '550e8400-e29b-41d4-a716-446655440003'),
        ('Рубашка офисная', 'Рубашки', 1999.99, 75, '2024-01-14', 5, '550e8400-e29b-41d4-a716-446655440004'),
        ('Свитер шерстяной', 'Свитеры', 3499.99, 40, '2024-01-11', 1, '550e8400-e29b-41d4-a716-446655440005'),
        ('Юбка миди', 'Юбки', 2299.99, 60, '2024-01-09', 2, '550e8400-e29b-41d4-a716-446655440006')
    ])

    # Клиенты
    cursor.executemany('''
    INSERT INTO client (client_name, client_surname, birthday, gender, registration_date, address_id) 
    VALUES (?, ?, ?, ?, ?, ?)
    ''', [
        ('Михаил', 'Ивасенко', '1990-05-15', 'М', '2023-12-01', 1),
        ('Надира', 'Кондыкерова', '1995-08-22', 'Ж', '2023-12-05', 2),
        ('Максим', 'Жоглов', '1988-03-10', 'М', '2023-11-20', 3),
        ('Максим', 'Тиханович', '1992-11-30', 'М', '2023-12-10', 4),
        ('Ярослав', 'Дементьев', '1985-07-18', 'М', '2023-11-15', 5)
    ])

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()