from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt

from database.database import DatabaseManager
from gui.settingsPage import SettingsWindow
from resources.utils import loginUtils


class FramelessWindow(QMainWindow):
    def __init__(self, login_window):
        super().__init__()
        self.db_manager = DatabaseManager('database/application.db')
        self.login_window = login_window
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 1600, 900)
        self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def toggle_lessons_dropdown(self):
        self.lessons_list_widget.setVisible(not self.lessons_list_widget.isVisible())
        self.robot_label.setVisible(not self.robot_label.isVisible())

    def open_settings_window(self):
        # Létrehozzuk a beállítások ablakot, ha még nem létezik
        if not hasattr(self, 'settings_window'):
            self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def sign_out(self):
        self.hide()
        self.open_login_window()
        try:
            with open('login_state.cfg', 'r', encoding='utf-8') as f:
                self.login_window.username_field.setText(f.read().strip().replace('\u200B', ''))
        except FileNotFoundError:
            pass
        self.login_window.checkBox.setChecked(False)
        self.login_window.password_field.setText('')
        self.login_window.password_field.setFocus()
        loginUtils.delete_login_state()
        self.user_label.setText("")

    def open_login_window(self, event=None):
        self.login_window.setWindowModality(Qt.ApplicationModal)
        self.login_window.show()

    def set_user_label(self, username_or_email):
        if loginUtils.is_email(username_or_email):
            self.user_label.setText(self.db_manager.get_username_by_email(username_or_email))
            self.user_label.setDisabled(True)
        else:
            self.user_label.setText(username_or_email)
            self.user_label.setDisabled(True)

    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
