from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView
import sqlite3
from cart_window import CartWindow
from favorite_window import FavoritesWindow
from book_details_window import BookDetailsWindow

class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.setWindowTitle("Каталог книг")
        self.setGeometry(100, 100, 800, 500)

        self.user_id = user_id

        # Виджеты
        self.table_books = QTableWidget()
        self.button_profile = QPushButton("Профиль")
        self.button_cart = QPushButton("Корзина")
        self.button_favorites = QPushButton("Избранное")
        self.button_logout = QPushButton("Выйти")

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.table_books)
        layout.addWidget(self.button_profile)
        layout.addWidget(self.button_cart)
        layout.addWidget(self.button_favorites)
        layout.addWidget(self.button_logout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Настройка таблицы
        self.table_books.setColumnCount(7)  # Мы добавляем 2 новых столбца
        self.table_books.setHorizontalHeaderLabels(["ID", "Название", "Автор", "Цена", "Осталось", "Добавить в корзину", "Добавить в избранное"])
        self.table_books.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Запрещаем редактировать ячейки
        self.table_books.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)  # Выделение строк
        self.table_books.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)  # Одновременный выбор одной строки
        self.table_books.horizontalHeader().setStretchLastSection(True)
        self.table_books.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Скрыть столбец ID
        self.table_books.setColumnHidden(0, True)

        # Загрузка книг
        self.load_books()

        # Подключение кнопок
        self.table_books.doubleClicked.connect(self.view_book_details)
        self.button_profile.clicked.connect(self.view_profile)
        self.button_cart.clicked.connect(self.view_cart)
        self.button_favorites.clicked.connect(self.view_favorites)
        self.button_logout.clicked.connect(self.logout)

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
        self.button_profile.setStyleSheet(button_style)
        self.button_cart.setStyleSheet(button_style)
        self.button_favorites.setObjectName("favorites")
        self.button_favorites.setStyleSheet(button_style)
        self.button_logout.setObjectName("logout")
        self.button_logout.setStyleSheet(button_style)

    def load_books(self):
        """Загружает книги из базы данных и отображает в таблице."""
        try:
            conn = sqlite3.connect("bookstore.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, author, price, stock FROM books")
            books = cursor.fetchall()
            conn.close()

            self.table_books.setRowCount(len(books)) 

            self.book_ids = []
            for row, (book_id, title, author, price, stock) in enumerate(books):
                self.book_ids.append(book_id)

                self.table_books.setItem(row, 1, QTableWidgetItem(title))  
                self.table_books.setItem(row, 2, QTableWidgetItem(author))  
                self.table_books.setItem(row, 3, QTableWidgetItem(f"{price} руб."))  

                # Проверяем количество на складе
                if stock == 0:
                    stock_display = "Нет в наличии"
                else:
                    stock_display = f"В наличии: {stock}"

                self.table_books.setItem(row, 4, QTableWidgetItem(stock_display))  
                
                add_to_cart_button = QPushButton("В корзину")
                add_to_favorites_button = QPushButton("В избранное")

                add_to_cart_button.setStyleSheet("""
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
                """)
                add_to_favorites_button.setStyleSheet("""
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
                """)

                # Привязываем действия к кнопкам
                add_to_cart_button.clicked.connect(lambda checked, book_id=book_id: self.add_to_cart(book_id))
                add_to_favorites_button.clicked.connect(lambda checked, book_id=book_id: self.add_to_favorites(book_id))

                # Добавляем кнопки в таблицу
                self.table_books.setCellWidget(row, 5, add_to_cart_button)
                self.table_books.setCellWidget(row, 6, add_to_favorites_button)

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось загрузить книги: {e}")

    def add_to_cart(self, book_id):
        """Добавляет книгу в корзину и уменьшает количество на складе."""
        try:
            conn = sqlite3.connect("bookstore.db")
            cursor = conn.cursor()

            cursor.execute("SELECT stock FROM books WHERE id = ?", (book_id,))
            stock = cursor.fetchone()[0]

            if stock <= 0:
                QMessageBox.warning(self, "Ошибка", "Книги нет в наличии!")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO cart (user_id, book_id, quantity) 
                VALUES (?, ?, 1)
                ON CONFLICT(user_id, book_id) 
                DO UPDATE SET quantity = quantity + 1
            """, (self.user_id, book_id))

            cursor.execute("""
                UPDATE books SET stock = stock - 1 WHERE id = ?
            """, (book_id,))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Книга добавлена в корзину!")
            self.load_books()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось добавить книгу в корзину: {e}")

    def add_to_favorites(self, book_id):
        """Добавляет книгу в избранное."""
        try:
            conn = sqlite3.connect("bookstore.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO favorites (user_id, book_id) 
                VALUES (?, ?)
            """, (self.user_id, book_id))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех", "Книга добавлена в избранное!")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось добавить книгу в избранное: {e}")

    def view_book_details(self):
        """Открывает окно с деталями книги.""" 
        selected_row = self.table_books.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите книгу для просмотра!")
            return

        book_id = self.book_ids[selected_row]
        self.close()
        self.book_details_window = BookDetailsWindow(book_id=book_id, user_id=self.user_id, back_to_main=MainWindow(self.user_id))
        self.book_details_window.show()

    def view_profile(self):
        """Открывает окно профиля.""" 
        from profile_window import ProfileWindow  
        self.close()
        self.profile_window = ProfileWindow(user_id=self.user_id, back_to_main=self.show)
        self.profile_window.show()

    def view_cart(self):
        """Открывает окно корзины.""" 
        self.close()
        self.cart_window = CartWindow(user_id=self.user_id, back_to_main=MainWindow(self.user_id))
        self.cart_window.show()

    def view_favorites(self):
        """Открывает окно избранного.""" 
        self.close()
        self.favorites_window = FavoritesWindow(user_id=self.user_id, back_to_main=MainWindow(self.user_id))
        self.favorites_window.show()

    def logout(self):
        """Выход из системы.""" 
        QMessageBox.information(self, "Выход", "Вы вышли из системы.")
        self.close()
