from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
from registration_window import RegistrationWindow
from admin_window import AdminWindow
from mainwindow import MainWindow
import sqlite3
import hashlib


class LoginWindow(QMainWindow):
    def __init__(self, open_main_window):
        super().__init__()
        self.setWindowTitle("Вход в систему")
        self.setGeometry(100, 100, 400, 300)
        self.open_main_window = open_main_window  # Функция для открытия главного окна

        # Поля для ввода логина и пароля
        self.label_username = QLabel("Логин:")
        self.input_username = QLineEdit()
        self.label_password = QLabel("Пароль:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.button_login = QPushButton("Войти")
        self.button_register = QPushButton("Регистрация")
         
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
            }"""

        self.button_login.setStyleSheet(button_style)
        self.button_register.setStyleSheet(button_style)#("padding: 4px 8px; font-size: 12px; border-radius: 100px; border: 1px solid #247dd6; color: #247dd6;")
        self.button_register.setStyleSheet#("padding: 4px 8px; font-size: 12px; border-radius: 100px; border: 1px solid #247dd6; color: #247dd6;")

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_register)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Подключение кнопок
        self.button_login.clicked.connect(self.login)
        self.button_register.clicked.connect(self.open_registration_window)

    def login(self):
        """Проверка логина и пароля."""
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        try:
            conn = sqlite3.connect("bookstore.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, is_admin FROM users WHERE username = ? AND password = ?", (username, hash_password))
            user = cursor.fetchone()
            conn.close()

            if user:
                user_id, is_admin = user
                if is_admin:
                    self.admin_window = AdminWindow(admin_id=user_id, back_to_login=self.show)
                    self.admin_window.show()
                else:
                    self.main_window = MainWindow(user_id=user_id)
                    self.main_window.show()
                self.close()
            else:
                QMessageBox.warning(self, "Ошибка", "Неправильный логин или пароль.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось выполнить вход: {e}")

    def open_registration_window(self):
        """Открытие окна регистрации."""
        self.registration_window = RegistrationWindow()
        self.registration_window.exec()
