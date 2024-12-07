from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sqlite3
import hashlib


class ProfileWindow(QMainWindow):
    def __init__(self, user_id, back_to_main):
        super().__init__()
        self.user_id = user_id
        self.back_to_main = back_to_main

        self.setWindowTitle("Профиль")
        self.setGeometry(100, 100, 400, 450)

        # Поля для редактирования
        self.input_name = QLineEdit()
        self.input_email = QLineEdit()
        self.input_phone = QLineEdit()
        self.input_password = QLineEdit()
        self.input_new_password = QLineEdit()
        self.input_confirm_password = QLineEdit()

        # Установка режима скрытого ввода для паролей
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_confirm_password.setEchoMode(QLineEdit.EchoMode.Password)

        # Кнопки
        self.button_save = QPushButton("Сохранить изменения")
        self.button_change_password = QPushButton("Изменить пароль")
        self.button_back = QPushButton("Назад")

        # Стиль кнопок и полей
        button_style = """
            QPushButton {
                padding: 4px 8px;
                font-size: 12px;
                border-radius: 100px;
                border: 1px solid #00a550;
                color: #00a550;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #00a550;
                color: white;
            }
            QPushButton:pressed {
                background-color: #1f5c92;
                border-color: #1f5c92;
            }
            QPushButton#change_password {
                border-color: #247dd6;
                color: #247dd6;
            }
            QPushButton#change_password:hover {
                background-color: #247dd6;
                color: white;

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
        input_style = "padding: 4px; font-size: 12px; border: 1px solid #ccc; border-radius: 20px;"

        # Применение стилей
        for widget in [self.input_name, self.input_email, self.input_phone, self.input_password, self.input_new_password, self.input_confirm_password]:
            widget.setStyleSheet(input_style)
            widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button_save.setStyleSheet(button_style)
        self.button_change_password.setStyleSheet(button_style)
        self.button_change_password.setObjectName("change_password")
        self.button_back.setStyleSheet(button_style)

        self.button_back.setObjectName("back")

        # Компоновка
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(QLabel("ФИО:"))
        layout.addWidget(self.input_name)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.input_email)
        layout.addWidget(QLabel("Телефон:"))
        layout.addWidget(self.input_phone)
        layout.addWidget(QLabel("Текущий пароль (для изменения данных):"))
        layout.addWidget(self.input_password)
        layout.addWidget(QLabel("Новый пароль:"))
        layout.addWidget(self.input_new_password)
        layout.addWidget(QLabel("Подтверждение нового пароля:"))
        layout.addWidget(self.input_confirm_password)
        layout.addWidget(self.button_save)
        layout.addWidget(self.button_change_password)
        layout.addWidget(self.button_back)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Загрузка данных профиля
        self.load_profile()

        # Подключение кнопок
        self.button_save.clicked.connect(self.save_changes)
        self.button_change_password.clicked.connect(self.change_password)
        self.button_back.clicked.connect(self.return_to_main)

    def load_profile(self):
        """Загрузка данных профиля из базы данных."""
        try:
            conn = sqlite3.connect("bookstore.db")
            cursor = conn.cursor()
            cursor.execute("SELECT full_name, email, phone FROM users WHERE id = ?", (self.user_id,))
            user = cursor.fetchone()
            conn.close()

            if user:
                self.input_name.setText(user[0])
                self.input_email.setText(user[1])
                self.input_phone.setText(user[2])
            else:
                QMessageBox.warning(self, "Ошибка", "Пользователь не найден.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось загрузить профиль: {e}")

    def save_changes(self):
        """Сохранение изменений профиля (логин, email, телефон)."""
        new_name = self.input_name.text().strip()
        new_email = self.input_email.text().strip()
        new_phone = self.input_phone.text().strip()
        current_password = self.input_password.text().strip()

        if not current_password:
            QMessageBox.warning(self, "Ошибка", "Для изменения данных требуется ввести текущий пароль.")
            return

        hashed_password = hashlib.sha256(current_password.encode('utf-8')).hexdigest()

        try:
            conn = sqlite3.connect("bookstore.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE id = ?", (self.user_id,))
            user = cursor.fetchone()

            if user and user[0] == hashed_password:
                cursor.execute("UPDATE users SET full_name = ?, email = ?, phone = ? WHERE id = ?",
                               (new_name, new_email, new_phone, self.user_id))
                conn.commit()
                QMessageBox.information(self, "Успех", "Профиль успешно обновлён!")
            else:
                QMessageBox.warning(self, "Ошибка", "Неправильный текущий пароль.")
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось сохранить изменения: {e}")

    def change_password(self):
        """Изменение пароля."""
        current_password = self.input_password.text().strip()
        new_password = self.input_new_password.text().strip()
        confirm_password = self.input_confirm_password.text().strip()

        if not current_password or not new_password or not confirm_password:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        if new_password != confirm_password:
            QMessageBox.warning(self, "Ошибка", "Новый пароль и подтверждение пароля не совпадают!")
            return

        hashed_current_password = hashlib.sha256(current_password.encode('utf-8')).hexdigest()
        hashed_new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

        try:
            conn = sqlite3.connect("bookstore.db")
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE id = ?", (self.user_id,))
            user = cursor.fetchone()

            if user and user[0] == hashed_current_password:
                if user[0] == hashed_new_password:
                    QMessageBox.warning(self, "Ошибка", "Новый пароль не может совпадать с текущим!")
                    return
                cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_new_password, self.user_id))
                conn.commit()
                QMessageBox.information(self, "Успех", "Пароль успешно изменён!")
            else:
                QMessageBox.warning(self, "Ошибка", "Неправильный текущий пароль.")
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", f"Не удалось изменить пароль: {e}")

    def return_to_main(self):
        """Возврат в главное окно."""
        self.close()
        self.back_to_main()
