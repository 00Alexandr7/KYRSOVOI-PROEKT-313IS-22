from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QMessageBox
import sqlite3
import openpyxl
from datetime import datetime

class CartWindow(QMainWindow):
    def __init__(self, user_id, back_to_main):
        super().__init__()
        self.setWindowTitle("Корзина")
        self.setGeometry(100, 100, 600, 400)

        self.user_id = user_id
        self.back_to_main = back_to_main

        # Создаем виджеты
        self.label_heading = QLabel("Ваша корзина")
        
        # Заменили QListWidget на QTableWidget для отображения товаров
        self.cart_table = QTableWidget()
        
        self.label_total = QLabel("Итоговая сумма: 0 руб.")
        self.button_checkout = QPushButton("Оформить заказ")
        self.button_remove_item = QPushButton("Удалить выбранный товар")
        self.button_back = QPushButton("Назад")

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.label_heading)
        layout.addWidget(self.cart_table)
        layout.addWidget(self.label_total)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_checkout)
        button_layout.addWidget(self.button_remove_item)
        button_layout.addWidget(self.button_back)
        layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Загрузка данных корзины
        self.load_cart()

        # Подключение кнопок
        self.button_checkout.clicked.connect(self.checkout)
        self.button_remove_item.clicked.connect(self.remove_item)
        self.button_back.clicked.connect(self.go_back)

        # Стилизация кнопок
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
            QPushButton#logout {
                border-color: #ff0000;
                color: #ff0000;
            }
            QPushButton#logout:hover {
                background-color: #ff0000;
                color: white;
            }
        """

        # Применение стилей ко всем кнопкам
        self.button_checkout.setStyleSheet(button_style)
        self.button_remove_item.setStyleSheet(button_style)
        self.button_back.setObjectName("logout")
        self.button_back.setStyleSheet(button_style)

    def get_db_connection(self):
        """Устанавливает соединение с базой данных."""
        return sqlite3.connect("bookstore.db")

    def load_cart(self):
        """Загружает данные корзины пользователя и отображает их в таблице."""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""SELECT books.id, books.title, books.price, cart.quantity
                              FROM cart
                              JOIN books ON cart.book_id = books.id
                              WHERE cart.user_id = ?""", (self.user_id,))
            cart_items = cursor.fetchall()
            conn.close()

            # Настроим таблицу
            self.cart_table.setRowCount(len(cart_items))
            self.cart_table.setColumnCount(4)
            self.cart_table.setHorizontalHeaderLabels(["Книга", "Цена", "Количество", "Итог"])

            total = 0
            self.book_ids = []

            # Заполнение таблицы данными
            for row, (book_id, title, price, quantity) in enumerate(cart_items):
                total_price = price * quantity
                total += total_price
                self.book_ids.append(book_id)

                self.cart_table.setItem(row, 0, QTableWidgetItem(title))
                self.cart_table.setItem(row, 1, QTableWidgetItem(f"{price:.2f} руб."))
                self.cart_table.setItem(row, 2, QTableWidgetItem(str(quantity)))
                self.cart_table.setItem(row, 3, QTableWidgetItem(f"{total_price:.2f} руб."))

            self.cart_table.resizeColumnsToContents()
            self.cart_table.resizeRowsToContents()

            self.label_total.setText(f"Итоговая сумма: {total:.2f} руб.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось загрузить корзину: {e}")

    def checkout(self):
        """Оформляет заказ и сохраняет информацию в Excel файл."""
        if self.cart_table.rowCount() == 0:
            QMessageBox.warning(self, "Ошибка", "Ваша корзина пуста!")
            return

        order_data = []
        total = 0
        for row in range(self.cart_table.rowCount()):
            title = self.cart_table.item(row, 0).text()
            price = float(self.cart_table.item(row, 1).text().replace(" руб.", ""))
            quantity = int(self.cart_table.item(row, 2).text())
            total_price = price * quantity
            order_data.append([title, price, quantity, total_price])
            total += total_price

        # Сохранение данных в Excel
        today = datetime.today().strftime('%Y-%m-%d')
        filename = f"Чек_{today}.xlsx"
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Чек"
        
        ws.append(["Книга", "Цена", "Количество", "Итог"])

        for item in order_data:
            ws.append(item)

        ws.append(["", "", "Итоговая сумма", f"{total:.2f} руб."])

        wb.save(filename)

        # Очистка корзины после оформления заказа
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cart WHERE user_id = ?", (self.user_id,))  # Очистка корзины
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Заказ оформлен", f"Ваш заказ оформлен! Чек сохранен как {filename}.")
            self.load_cart()  # Обновление корзины
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось оформить заказ: {e}")

    def remove_item(self):
        """Удаляет выбранный товар из корзины."""
        selected_row = self.cart_table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для удаления!")
            return

        book_id = self.book_ids[selected_row]
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM cart WHERE user_id = ? AND book_id = ?""", (self.user_id, book_id))
            cursor.execute("""UPDATE books SET stock = stock + 1 WHERE id = ?""", (book_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Товар удалён из корзины.")
            self.load_cart()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось удалить товар: {e}")

    def go_back(self):
        """Возвращает в главное окно."""
        from mainwindow import MainWindow
        self.hide()
        self.window = MainWindow(self.user_id)
        self.window.show()
