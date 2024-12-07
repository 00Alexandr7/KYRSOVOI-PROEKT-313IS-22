import sys
from PyQt6.QtWidgets import QApplication
from cart_window import CartWindow
from favorite_window import FavoritesWindow
from book_details_window import BookDetailsWindow


class ApplicationManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.user_id = None  
        self.login_window = None
        self.main_window = None
        self.profile_window = None
        self.cart_window = None
        self.favorites_window = None
        self.book_details_window = None

    def show_login_window(self):
        """Открывает окно входа."""
        from login_window import LoginWindow
        if not self.login_window:
            self.login_window = LoginWindow(open_main_window=self.show_main_window)
        self.login_window.show()

    def show_main_window(self, user_id):
        """Открывает главное окно."""
        from mainwindow import MainWindow
        self.user_id = user_id
        if not self.main_window:
            self.main_window = MainWindow(
                user_id=self.user_id
            )
        self.main_window.show()

    def show_profile_window(self):
        """Открывает окно профиля."""
        from profile_window import ProfileWindow
        if not self.profile_window:
            self.profile_window = ProfileWindow(user_id=self.user_id, back_to_main=self.show_main_window)
        self.profile_window.show()

    def show_cart_window(self):
        """Открывает окно корзины."""
        if not self.cart_window:
            self.cart_window = CartWindow(user_id=self.user_id, back_to_main=self.show_main_window)
        self.cart_window.show()

    def show_favorites_window(self):
        """Открывает окно избранного."""
        if not self.favorites_window:
            self.favorites_window = FavoritesWindow(user_id=self.user_id, back_to_main=self.show_main_window)
        self.favorites_window.show()

    def show_book_details_window(self, book_id):
        """Открывает окно деталей книги."""
        if not self.book_details_window:
            self.book_details_window = BookDetailsWindow(
                book_id=book_id,
                user_id=self.user_id,
                back_to_main=self.show_main_window
            )
        self.book_details_window.show()


if __name__ == "__main__":
    manager = ApplicationManager()
    manager.show_login_window()
    sys.exit(manager.app.exec())
