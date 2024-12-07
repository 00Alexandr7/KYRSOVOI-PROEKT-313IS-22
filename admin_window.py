from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QInputDialog
import sqlite3

class AdminWindow(QMainWindow):
    def __init__(self, admin_id, back_to_login):
        super().__init__()
        self.admin_id = admin_id
        self.back_to_login = back_to_login

        self.setWindowTitle("Администраторский интерфейс")
        self.setGeometry(100, 100, 800, 600)

        # Виджеты
        self.label_heading = QLabel("Административная панель")
        
        # Используем QTableWidget для отображения данных
        self.table_users = QTableWidget()
        self.table_comments = QTableWidget()
        self.table_books = QTableWidget()

        # Поля ввода для добавления книги
        self.input_book_title = QLineEdit()
        self.input_book_author = QLineEdit()
        self.input_book_genre = QLineEdit()
        self.input_book_price = QLineEdit()
        self.input_book_stock = QLineEdit()
        
        # Кнопки
        self.button_add_book = QPushButton("Добавить книгу")
        self.button_remove_user = QPushButton("Удалить пользователя")
        self.button_delete_comment = QPushButton("Удалить отзыв")
        self.button_edit_book_quantity = QPushButton("Изменить количество")
        self.button_edit_book_description = QPushButton("Изменить описание")
        self.button_logout = QPushButton("Выйти")

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.label_heading)
        
        # Настроим таблицы
        layout.addWidget(QLabel("Пользователи:"))
        layout.addWidget(self.table_users)
        layout.addWidget(self.button_remove_user)
        
        layout.addWidget(QLabel("Отзывы:"))
        layout.addWidget(self.table_comments)
        layout.addWidget(self.button_delete_comment)
        
        layout.addWidget(QLabel("Каталог книг:"))
        layout.addWidget(self.table_books)
        
        layout.addWidget(QLabel("Добавить книгу:"))
        layout.addWidget(QLabel("Название:"))
        layout.addWidget(self.input_book_title)
        layout.addWidget(QLabel("Автор:"))
        layout.addWidget(self.input_book_author)
        layout.addWidget(QLabel("Жанр:"))
        layout.addWidget(self.input_book_genre)
        layout.addWidget(QLabel("Цена:"))
        layout.addWidget(self.input_book_price)
        layout.addWidget(QLabel("Количество:"))
        layout.addWidget(self.input_book_stock)
        layout.addWidget(self.button_add_book)

        layout.addWidget(self.button_edit_book_quantity)
        layout.addWidget(self.button_edit_book_description)
        layout.addWidget(self.button_logout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Загрузка данных
        self.load_users()
        self.load_comments()
        self.load_books()

        # Подключение кнопок
        self.button_add_book.clicked.connect(self.add_book)
        self.button_delete_comment.clicked.connect(self.delete_comment)
        self.button_remove_user.clicked.connect(self.remove_user)
        self.button_edit_book_quantity.clicked.connect(self.edit_book_quantity)
        self.button_edit_book_description.clicked.connect(self.edit_book_description)
        self.button_logout.clicked.connect(self.logout)

        # Стилизация кнопок
        self.apply_button_styles()

    def apply_button_styles(self):
        """Применение стилей ко всем кнопкам"""
        button_style = """
            QPushButton {
                padding: 4px 8px;
                font-size: 12px;
                border-radius: 100px;
                border: 1px solid #247dd6;
                color: #247dd6;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #247dd6;
                color: white;
            }
            QPushButton:pressed {
                background-color: #1f5c92;
                border-color: #1f5c92;
            }
            QPushButton#button_add_book {
                border-color: #00a550;
                color: #00a550;
            }
            QPushButton#button_add_book:hover {
                background-color: #00a550;
                color: white;
            }
            QPushButton#logout {
                border-color: #ff0000;
                color: #ff0000;
            }
            QPushButton#logout:hover {
                background-color: #ff0000;
                color: white;
            }
        """

        self.button_add_book.setStyleSheet(button_style)
        self.button_add_book.setObjectName("button_add_book")
        self.button_remove_user.setStyleSheet(button_style)
        self.button_remove_user.setObjectName("logout")
        self.button_delete_comment.setStyleSheet(button_style)
        self.button_delete_comment.setObjectName("logout")
        self.button_edit_book_quantity.setStyleSheet(button_style)
        self.button_edit_book_description.setStyleSheet(button_style)
        self.button_logout.setStyleSheet(button_style)
        self.button_logout.setObjectName("logout")

    def load_users(self):
        """Загрузка пользователей из базы данных."""
        conn = sqlite3.connect("bookstore.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT id, full_name, email FROM users WHERE is_admin = 0""")
        users = cursor.fetchall()
        conn.close()

        self.table_users.setRowCount(len(users))
        self.table_users.setColumnCount(3)
        self.table_users.setHorizontalHeaderLabels(['ID', 'Имя', 'Email'])
        
        for row, (user_id, full_name, email) in enumerate(users):
            self.table_users.setItem(row, 0, QTableWidgetItem(str(user_id)))
            self.table_users.setItem(row, 1, QTableWidgetItem(full_name))
            self.table_users.setItem(row, 2, QTableWidgetItem(email))

    def load_comments(self):
        """Загрузка отзывов из базы данных."""
        conn = sqlite3.connect("bookstore.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT comments.id, users.full_name, comments.content
                          FROM comments
                          JOIN users ON comments.user_id = users.id""")
        comments = cursor.fetchall()
        conn.close()

        self.table_comments.setRowCount(len(comments))
        self.table_comments.setColumnCount(3)
        self.table_comments.setHorizontalHeaderLabels(['ID', 'Пользователь', 'Комментарий'])

        for row, (comment_id, user_name, content) in enumerate(comments):
            self.table_comments.setItem(row, 0, QTableWidgetItem(str(comment_id)))
            self.table_comments.setItem(row, 1, QTableWidgetItem(user_name))
            self.table_comments.setItem(row, 2, QTableWidgetItem(content))

    def load_books(self):
        """Загрузка книг из базы данных."""
        conn = sqlite3.connect("bookstore.db")
        cursor = conn.cursor()
        cursor.execute("""SELECT id, title, author, genre, price, stock FROM books""")
        books = cursor.fetchall()
        conn.close()

        self.table_books.setRowCount(len(books))
        self.table_books.setColumnCount(6)
        self.table_books.setHorizontalHeaderLabels(['ID', 'Название', 'Автор', 'Жанр', 'Цена', 'Количество'])

        for row, (book_id, title, author, genre, price, stock) in enumerate(books):
            self.table_books.setItem(row, 0, QTableWidgetItem(str(book_id)))
            self.table_books.setItem(row, 1, QTableWidgetItem(title))
            self.table_books.setItem(row, 2, QTableWidgetItem(author))
            self.table_books.setItem(row, 3, QTableWidgetItem(genre))
            self.table_books.setItem(row, 4, QTableWidgetItem(str(price)))
            self.table_books.setItem(row, 5, QTableWidgetItem(str(stock)))

    def add_book(self):
        """Добавление новой книги."""
        title = self.input_book_title.text().strip()
        author = self.input_book_author.text().strip()
        genre = self.input_book_genre.text().strip()
        try:
            price = float(self.input_book_price.text().strip())
            stock = int(self.input_book_stock.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Введите корректные значения для цены и количества.")
            return

        if not title or not author or not genre:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        conn = sqlite3.connect("bookstore.db")
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO books (title, author, genre, price, stock) 
                          VALUES (?, ?, ?, ?, ?)""", (title, author, genre, price, stock))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Успех", "Книга добавлена.")
        self.load_books()

    def edit_book_quantity(self):
        """Изменение количества книги."""
        selected_row = self.table_books.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу для изменения.")
            return

        book_id = int(self.table_books.item(selected_row, 0).text())
        new_quantity, ok = QInputDialog.getInt(self, "Изменить количество", "Введите новое количество:", 1)
        if ok:
            conn = sqlite3.connect("bookstore.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE books SET stock = ? WHERE id = ?", (new_quantity, book_id))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Количество книги обновлено.")
            self.load_books()

    def edit_book_description(self):
        """Изменение описания книги."""
        selected_row = self.table_books.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу для изменения.")
            return

        book_id = int(self.table_books.item(selected_row, 0).text())
        new_description, ok = QInputDialog.getText(self, "Изменить описание", "Введите новое описание:")
        if ok:
            conn = sqlite3.connect("bookstore.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE books SET description = ? WHERE id = ?", (new_description, book_id))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Описание книги обновлено.")
            self.load_books()

    def delete_comment(self):
        """Удаление отзыва."""
        selected_row = self.table_comments.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите отзыв для удаления.")
            return

        comment_id = int(self.table_comments.item(selected_row, 0).text())
        conn = sqlite3.connect("bookstore.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Успех", "Отзыв удалён.")
        self.load_comments()

    def remove_user(self):
        """Удаление пользователя."""
        selected_row = self.table_users.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для удаления.")
            return

        user_id = int(self.table_users.item(selected_row, 0).text())
        conn = sqlite3.connect("bookstore.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id =? AND is_admin=0", (user_id,))
        conn.commit()
        conn.close()

        self.load_users()
        QMessageBox.information(self, "Успех", "Пользователь удалён.")

    def logout(self):
        """Выход из административного интерфейса."""
        self.close()
        self.back_to_login()
