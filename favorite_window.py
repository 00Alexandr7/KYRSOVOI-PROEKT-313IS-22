from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QMessageBox
import sqlite3

class FavoritesWindow(QMainWindow):
    def __init__(self, user_id, back_to_main):
        super().__init__()
        self.setWindowTitle("Избранное")
        self.setGeometry(100, 100, 600, 400)

        self.user_id = user_id
        self.back_to_main = back_to_main

        # Создание виджетов
        self.favorites_table = QTableWidget()
        self.button_move_to_cart = QPushButton("Переместить в корзину")
        self.button_remove = QPushButton("Удалить из избранного")
        self.button_back = QPushButton("Назад")

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
            QPushButton#back {
                border-color: #ff0000;
                color: #ff0000;
            }
            QPushButton#back:hover {
                background-color: #d10000;
                color: white;
            }
            QPushButton#back:pressed {
                background-color: #a10000;
                border-color: #a10000;
            }
        """
        
        # Применение стилей
        self.button_move_to_cart.setStyleSheet(button_style)
        self.button_remove.setStyleSheet(button_style)
        self.button_back.setStyleSheet(button_style)
        self.button_back.setObjectName("back")  # Установка ID для кнопки "Назад"

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.favorites_table)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_move_to_cart)
        button_layout.addWidget(self.button_remove)
        button_layout.addWidget(self.button_back)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Загрузка данных избранного
        self.load_favorites()

        # Подключение кнопок
        self.button_move_to_cart.clicked.connect(self.move_to_cart)
        self.button_remove.clicked.connect(self.remove_from_favorites)
        self.button_back.clicked.connect(self.go_back)

    def get_db_connection(self):
        """Устанавливает соединение с базой данных."""
        return sqlite3.connect("bookstore.db")

    def load_favorites(self):
        """Загружает избранные книги пользователя и отображает их в таблице."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT books.id, books.title, books.price
                FROM favorites
                JOIN books ON favorites.book_id = books.id
                WHERE favorites.user_id = ?
            """, (self.user_id,))
            favorites = cursor.fetchall()
            conn.close()

            # Настроим таблицу
            self.favorites_table.setRowCount(len(favorites))
            self.favorites_table.setColumnCount(2)
            self.favorites_table.setHorizontalHeaderLabels(["Книга", "Цена"])

            if not favorites:
                QMessageBox.information(self, "Избранное пусто", "У вас нет избранных книг.")
                return

            # Заполнение таблицы данными
            self.book_ids = []  # Список ID книг для операций
            for row, (book_id, title, price) in enumerate(favorites):
                self.book_ids.append(book_id)

                # Устанавливаем данные в таблицу
                self.favorites_table.setItem(row, 0, QTableWidgetItem(title))
                self.favorites_table.setItem(row, 1, QTableWidgetItem(f"{price} руб."))

            # Автоматическая настройка ширины столбцов
            self.favorites_table.resizeColumnsToContents()
            self.favorites_table.resizeRowsToContents()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось загрузить избранное: {e}")

    def move_to_cart(self, row):
        """Перемещает выбранную книгу из избранного в корзину."""
        book_id = self.book_ids[row]
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()

            # Проверяем, есть ли книга уже в корзине
            cursor.execute("""
                SELECT quantity FROM cart WHERE user_id = ? AND book_id = ?
            """, (self.user_id, book_id))
            cart_item = cursor.fetchone()

            if cart_item:
                # Увеличиваем количество
                cursor.execute("""
                    UPDATE cart SET quantity = quantity + 1 WHERE user_id = ? AND book_id = ?
                """, (self.user_id, book_id))
            else:
                # Добавляем книгу в корзину
                cursor.execute("""
                    INSERT INTO cart (user_id, book_id, quantity) VALUES (?, ?, 1)
                """, (self.user_id, book_id))

            # Удаляем книгу из избранного
            cursor.execute("""
                DELETE FROM favorites WHERE user_id = ? AND book_id = ?
            """, (self.user_id, book_id))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Книга перемещена в корзину!")
            self.load_favorites()  # Обновление списка избранного
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось переместить книгу в корзину: {e}")

    def remove_from_favorites(self):
        """Удаляет выбранную книгу из избранного."""
        selected_row = self.favorites_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу для удаления из избранного!")
            return

        book_id = self.book_ids[selected_row]
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM favorites WHERE user_id = ? AND book_id = ?
            """, (self.user_id, book_id))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Книга удалена из избранного!")
            self.load_favorites()  # Обновление списка избранного
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось удалить книгу из избранного: {e}")

    def go_back(self):
         """Возвращает в главное окно."""
         from mainwindow import MainWindow
         self.close()  # Закрываем текущее окно
         self.main_window = MainWindow(self.user_id)  # Создаём новое окно
         self.main_window.show()  # Показываем его
