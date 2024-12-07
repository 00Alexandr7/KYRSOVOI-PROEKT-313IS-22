from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QTableWidget, QTableWidgetItem, QWidget, QMessageBox
import sqlite3


class BookDetailsWindow(QMainWindow):
    def __init__(self, book_id, user_id, back_to_main):
        super().__init__()
        self.setWindowTitle("Детали книги")
        self.setGeometry(100, 100, 600, 500)

        # Переданные параметры
        self.book_id = book_id
        self.user_id = user_id
        self.back_to_main = back_to_main

        # Создание виджетов
        self.label_title = QLabel("Наименование:")
        self.label_author = QLabel("Автор:")
        self.label_price = QLabel("Цена:")
        self.label_stock = QLabel("В наличии:")
        self.label_description = QLabel("Описание:")
        self.text_description = QLabel()
        
        # Заменили QListWidget на QTableWidget для отзывов
        self.comments_table = QTableWidget()
        self.text_comment = QTextEdit()
        
        self.button_add_to_cart = QPushButton("Добавить в корзину")
        self.button_add_to_favorites = QPushButton("Добавить в избранное")
        self.button_add_comment = QPushButton("Оставить отзыв")
        self.button_back = QPushButton("Назад")

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.label_title)
        layout.addWidget(self.label_author)
        layout.addWidget(self.label_price)
        layout.addWidget(self.label_stock)
        layout.addWidget(self.label_description)
        layout.addWidget(self.text_description)

        # Добавление таблицы для отзывов
        layout.addWidget(QLabel("Отзывы:"))
        layout.addWidget(self.comments_table)

        layout.addWidget(QLabel("Ваш отзыв:"))
        layout.addWidget(self.text_comment)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_add_to_cart)
        button_layout.addWidget(self.button_add_to_favorites)
        button_layout.addWidget(self.button_add_comment)
        button_layout.addWidget(self.button_back)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Загрузка данных книги и отзывов
        self.load_book_details()
        self.load_comments()

        # Подключение кнопок
        self.button_add_to_cart.clicked.connect(self.add_to_cart)
        self.button_add_to_favorites.clicked.connect(self.add_to_favorites)
        self.button_add_comment.clicked.connect(self.add_comment)
        self.button_back.clicked.connect(self.go_back)

        # Стиль для кнопок
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
            QPushButton#favorites {
                border-color: #ffd700;
                color: #ffd700;
            }
            QPushButton#favorites:hover {
                background-color: #ffd700;
                color: white;
            }
            QPushButton#cart {
                border-color: #00a550;
                color: #00a550;
            }
            QPushButton#cart:hover {
                background-color: #00a550;
                color: white;
            }
            QPushButton#back {
                border-color: #ff0000;
                color: #ff0000;
            }
            QPushButton#back:hover {
                background-color: #ff0000;
                color: white;
            }
        """

        self.button_add_to_cart.setStyleSheet(button_style)
        self.button_add_to_cart.setObjectName("buttom_add_to_cart")
        self.button_add_to_favorites.setStyleSheet(button_style)
        self.button_add_to_favorites.setObjectName("favorites")
        self.button_add_comment.setStyleSheet(button_style)
        self.button_back.setStyleSheet(button_style)
        self.button_back.setObjectName("back")

    def get_db_connection(self):
        """Устанавливает соединение с базой данных."""
        return sqlite3.connect("bookstore.db")

    def load_book_details(self):
        """Загружает информацию о книге из базы данных."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title, author, price, stock, description FROM books WHERE id = ?",
                (self.book_id,)
            )
            book = cursor.fetchone()
            conn.close()

            if book:
                title, author, price, stock, description = book
                self.label_title.setText(f"Наименование: {title}")
                self.label_author.setText(f"Автор: {author}")
                self.label_price.setText(f"Цена: {price} руб.")
                if stock == 0:
                    self.label_stock.setText("Нет в наличии")
                else:
                    self.label_stock.setText(f"В наличии: {stock}")
                self.text_description.setText(description)
            else:
                QMessageBox.warning(self, "Ошибка", "Книга не найдена!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось загрузить данные книги: {e}")

    def load_comments(self):
        """Загружает отзывы к книге и отображает их в таблице."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT users.full_name, comments.content, comments.created_at
                FROM comments
                JOIN users ON comments.user_id = users.id
                WHERE comments.book_id = ?
                ORDER BY comments.created_at DESC
            """, (self.book_id,))
            comments = cursor.fetchall()
            conn.close()

            # Настроим таблицу
            self.comments_table.setRowCount(len(comments))
            self.comments_table.setColumnCount(3)
            self.comments_table.setHorizontalHeaderLabels(["Имя", "Отзыв", "Дата"])

            # Заполнение таблицы данными
            for row, (full_name, content, created_at) in enumerate(comments):
                self.comments_table.setItem(row, 0, QTableWidgetItem(full_name))
                self.comments_table.setItem(row, 1, QTableWidgetItem(content))
                self.comments_table.setItem(row, 2, QTableWidgetItem(created_at))

            # Автоматическая настройка ширины столбцов
            self.comments_table.resizeColumnsToContents()
            self.comments_table.resizeRowsToContents()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось загрузить отзывы: {e}")

    def add_to_cart(self):
        """Добавляет книгу в корзину и уменьшает количество в базе данных."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT stock FROM books WHERE id = ?", (self.book_id,))
            stock = cursor.fetchone()[0]

            if stock > 0:
                cursor.execute("""SELECT quantity FROM cart WHERE user_id = ? AND book_id = ?""", (self.user_id, self.book_id))
                cart_item = cursor.fetchone()

                if cart_item:
                    cursor.execute("""UPDATE cart SET quantity = quantity + 1 WHERE user_id = ? AND book_id = ?""", (self.user_id, self.book_id))
                else:
                    cursor.execute("""INSERT INTO cart (user_id, book_id, quantity) VALUES (?, ?, 1)""", (self.user_id, self.book_id))

                cursor.execute("""UPDATE books SET stock = stock - 1 WHERE id = ?""", (self.book_id,))
                conn.commit()

                self.load_book_details()

                QMessageBox.information(self, "Успех", "Книга добавлена в корзину!")
            else:
                QMessageBox.warning(self, "Ошибка", "Товара нет в наличии!")

            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось добавить книгу в корзину: {e}")

    def add_to_favorites(self):
        """Добавляет книгу в избранное."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT id FROM favorites WHERE user_id = ? AND book_id = ?""", (self.user_id, self.book_id))
            favorite_item = cursor.fetchone()

            if favorite_item:
                QMessageBox.warning(self, "Уведомление", "Эта книга уже в избранном!")
            else:
                cursor.execute("""INSERT INTO favorites (user_id, book_id) VALUES (?, ?)""", (self.user_id, self.book_id))
                conn.commit()
                QMessageBox.information(self, "Успех", "Книга добавлена в избранное!")
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось добавить книгу в избранное: {e}")

    def add_comment(self):
        """Добавляет отзыв к книге."""
        comment = self.text_comment.toPlainText().strip()
        if not comment:
            QMessageBox.warning(self, "Ошибка", "Отзыв не может быть пустым!")
            return

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO comments (book_id, user_id, content) VALUES (?, ?, ?)""", (self.book_id, self.user_id, comment))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Ваш отзыв добавлен!")
            self.text_comment.clear()
            self.load_comments()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось добавить отзыв: {e}")

    def go_back(self):
        """Возвращает в главное окно."""
        from mainwindow import MainWindow
        self.hide()
        self.window = MainWindow(self.user_id)
        self.window.show()
