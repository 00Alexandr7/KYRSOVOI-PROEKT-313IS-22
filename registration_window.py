from PyQt6.QtWidgets import QDialog, QLineEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox
import sqlite3
import hashlib
import re  # Для регулярных выражений

class RegistrationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setGeometry(100, 100, 400, 300)

        # Поля для ввода данных
        self.label_full_name = QLabel("ФИО:")
        self.input_full_name = QLineEdit()
        self.label_email = QLabel("Почта:")
        self.input_email = QLineEdit()
        self.label_phone = QLabel("Телефон:")
        self.input_phone = QLineEdit()
        self.label_username = QLabel("Логин:")
        self.input_username = QLineEdit()
        self.label_password = QLabel("Пароль:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.button_register = QPushButton("Зарегистрироваться")

        # Компоновка
        layout = QVBoxLayout()
        layout.addWidget(self.label_full_name)
        layout.addWidget(self.input_full_name)
        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)
        layout.addWidget(self.label_phone)
        layout.addWidget(self.input_phone)
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.button_register)
        self.setLayout(layout)

        # Подключение кнопки
        self.button_register.clicked.connect(self.register_user)

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

        self.button_register.setStyleSheet(button_style)

    def hash_password(self, password):
        """Хэширует пароль с помощью SHA256."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def validate_full_name(self, full_name):
        """Проверка ФИО: только русские буквы, минимум 3 символа."""
        if len(full_name.split()) < 3:
            return False, "Введите полное ФИО (имя и фамилию)."
        if not re.match(r'^[А-Яа-яЁё\s]+$', full_name):
            return False, "ФИО должно содержать только русские буквы."
        if len(full_name) < 3:
            return False, "ФИО должно содержать хотя бы 3 символа."
        return True, ""

    def validate_username(self, username):
        """Проверка логина: минимум 8 символов, только латинские буквы и цифры."""
        if len(username) < 8:
            return False, "Логин должен содержать минимум 8 символов."
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            return False, "Логин должен содержать только латинские буквы и цифры."
        return True, ""

    def validate_password(self, password):
        """Проверка пароля: минимум 8 символов, только латинские буквы и цифры."""
        if len(password) < 8:
            return False, "Пароль должен содержать минимум 8 символов."
        if not re.match(r'^[a-zA-Z0-9]+$', password):
            return False, "Пароль должен содержать только латинские буквы и цифры."
        return True, ""

    def register_user(self):
        """Регистрация пользователя в системе."""
        # Получение данных из полей
        full_name = self.input_full_name.text().strip()
        email = self.input_email.text().strip()
        phone = self.input_phone.text().strip()
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        # Проверка обязательных полей
        if not full_name or not email or not username or not password:
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля!")
            return

        # Валидация ФИО
        is_valid, message = self.validate_full_name(full_name)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", message)
            return

        # Валидация логина
        is_valid, message = self.validate_username(username)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", message)
            return

        # Валидация пароля
        is_valid, message = self.validate_password(password)
        if not is_valid:
            QMessageBox.warning(self, "Ошибка", message)
            return

        # Валидация email
        if "@" not in email or "." not in email:
            QMessageBox.warning(self, "Ошибка", "Введите правильный адрес электронной почты!")
            return

        # Валидация номера телефона
        if not phone.isdigit() or len(phone) < 10:
            QMessageBox.warning(self, "Ошибка", "Введите правильный номер телефона!")
            return

        # Проверка уникальности логина и почты
        try:
            conn = sqlite3.connect("bookstore.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
            existing_user = cursor.fetchone()
            if existing_user:
                QMessageBox.warning(self, "Ошибка", "Логин или почта уже зарегистрированы!")
                conn.close()
                return
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Ошибка подключения к базе данных: {e}")
            return

        # Хэшируем пароль перед сохранением в базе данных
        hashed_password = self.hash_password(password)

        # Добавление нового пользователя
        try:
            cursor.execute("""
                INSERT INTO users (full_name, email, phone, username, password)
                VALUES (?, ?, ?, ?, ?)
            """, (full_name, email, phone, username, hashed_password))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Успех", "Регистрация прошла успешно! Теперь вы можете войти.")
            self.close()  # Закрытие окна регистрации
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось зарегистрировать пользователя: {e}")
