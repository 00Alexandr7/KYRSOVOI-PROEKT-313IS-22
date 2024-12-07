import sqlite3

# Создание базы данных и подключение
conn = sqlite3.connect("bookstore.db")
cursor = conn.cursor()

# Таблица пользователей
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT 0  -- Флаг, указывающий, является ли пользователь администратором
)
""")

# Таблица книг
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    description TEXT,
    image_path TEXT
)
""")

# Таблица корзины
cursor.execute("""
CREATE TABLE IF NOT EXISTS cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (book_id) REFERENCES books (id),
    UNIQUE (user_id, book_id)
)
""")

# Таблица избранного
cursor.execute("""
CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (book_id) REFERENCES books (id)
)
""")

# Таблица отзывов
cursor.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")

# Добавление тестовых данных
# cursor.execute("INSERT OR IGNORE INTO users (full_name, email, phone, username, password, is_admin) VALUES (?, ?, ?, ?, ?, ?)",
#                ("Admin User", "admin@bookstore.com", "1234567890", "admin", "admin123", True))
# cursor.execute("INSERT OR IGNORE INTO users (full_name, email, phone, username, password) VALUES (?, ?, ?, ?, ?)",
#                ("John Doe", "john.doe@example.com", "1231231234", "john_doe", "password123"))
# cursor.execute("INSERT OR IGNORE INTO users (full_name, email, phone, username, password) VALUES (?, ?, ?, ?, ?)",
#                ("Jane Smith", "jane.smith@example.com", "9876543210", "jane_smith", "password456"))


# cursor.execute("UPDATE users SET is_admin = 1 WHERE id = 1")
# cursor.execute("UPDATE users SET password = '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9' WHERE id = 1")

# # Добавление тестовых книг
# cursor.execute("INSERT OR IGNORE INTO books (title, author, genre, price, stock, description, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                ("1984", "George Orwell", "Дистопия", 19.99, 5, "Книга о тоталитарном будущем", None))
# cursor.execute("INSERT OR IGNORE INTO books (title, author, genre, price, stock, description, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                ("Brave New World", "Aldous Huxley", "Фантастика", 15.99, 8, "Будущее общество", None))
# cursor.execute("""
#     INSERT INTO books (title, author, genre, price, stock, description, image_path)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("Преступление и наказание", "Федор Достоевский", "Роман", 12.99, 15, "Роман о нравственных и социальных вопросах", None))
# cursor.execute("""
#     INSERT INTO books (title, author, genre, price, stock, description, image_path)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("Война и мир", "Лев Толстой", "Роман", 19.99, 10, "Эпопея о войне 1812 года и жизни русской аристократии", None))
# cursor.execute("""
#     INSERT INTO books (title, author, genre, price, stock, description, image_path)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("Мастер и Маргарита", "Михаил Булгаков", "Роман", 16.99, 20, "Философский роман о дьяволе, любви и Москве", None))
# cursor.execute("""
#     INSERT INTO books (title, author, genre, price, stock, description, image_path)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("Анна Каренина", "Лев Толстой", "Роман", 14.99, 8, "Роман о любви, изменах и социальной несправедливости", None))
# cursor.execute("""
#     INSERT INTO books (title, author, genre, price, stock, description, image_path)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("Тихий Дон", "Михаил Шолохов", "Роман", 17.99, 12, "Роман о судьбе казачьего народа во времена Первой мировой войны", None))
# cursor.execute("""
#     INSERT INTO books (title, author, genre, price, stock, description, image_path)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("Доктор Живаго", "Борис Пастернак", "Роман", 18.99, 10, "Роман о любви и революции в России", None))
# cursor.execute("""
#     INSERT INTO books (title, author, genre, price, stock, description, image_path)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("Молодая гвардия", "Александр Фадеев", "Роман", 13.99, 6, "Роман о героизме советских людей во времена войны", None))
# cursor.execute("""
#     INSERT INTO books (title, author, genre, price, stock, description, image_path)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("Собачье сердце", "Михаил Булгаков", "Роман", 15.49, 18, "Роман о превращении пса в человека", None))
# cursor.execute("""
#     INSERT INTO books (title, author, genre, price, stock, description, image_path)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("To Kill a Mockingbird", "Harper Lee", "Драма", 18.99, 12, "Классика американской литературы", None))
# cursor.execute("""
#     INSERT INTO books (title, author, genre, price, stock, description, image_path)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ("The Great Gatsby", "F. Scott Fitzgerald", "Роман", 14.99, 5, "Роман о богатстве и утрате", None))

# conn.commit()
# conn.close()
