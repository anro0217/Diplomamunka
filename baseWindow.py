from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QPushButton
from PyQt5.QtCore import Qt, QTimer, QEvent, QSize

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

        self.settings_window = SettingsWindow(self)
        self.settings_window.resize(250, 400)
        self.settings_window.hide()

        # Felhasználói menü/profile gomb
        self.user_menu_button = QPushButton()
        self.profile_icon = QIcon('resources/images/blank_profile.png')
        self.user_menu_button.setIcon(self.profile_icon)
        self.user_menu_button.setIconSize(QSize(40, 40))  # Az ikon méretének beállítása
        self.user_menu_button.setFlat(True)
        self.user_menu_button.setFixedSize(40, 40)  # A gomb méretének beállítása
        self.user_menu_button.setStyleSheet(
            "QPushButton {"
            "border: none;"  # Eltávolítjuk a gomb keretét
            "border-radius: 20px;"  # Kör alakúra állítjuk
            "}"
            "QPushButton:pressed {"
            "border: 1px solid #8f8f91;"  # Megnyomáskor keretet adunk hozzá
            "}"
        )

        self.user_menu = QMenu()
        self.user_menu_button.setMenu(self.user_menu)
        self.settings_action = QAction("Settings", self)
        self.settings_action.triggered.connect(self.open_settings_window)
        self.sign_out_action = QAction("Sign Out", self)
        self.sign_out_action.triggered.connect(self.sign_out)
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(QApplication.instance().quit)

        self.user_menu.addActions([self.settings_action, self.sign_out_action, self.exit_action])

        self.user_menu_button.installEventFilter(self)

    def open_settings_window(self):
        x = (self.x() + self.width()) - self.settings_window.width()
        y = (self.y())
        self.settings_window.move(x, y)
        self.settings_window.show()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)  # Először hívjuk meg a szülő osztály mousePressEvent-jét

        # Ellenőrizzük, hogy a settings ablak nyitva van-e
        if self.settings_window.isVisible():
            # Ellenőrizzük, hogy a kattintás a settings ablakon kívül történt-e
            if not self.settings_window.geometry().contains(self.mapFromGlobal(event.globalPos())):
                self.settings_window.hide()  # Zárjuk be az ablakot

    def toggle_lessons_dropdown(self):
        self.lessons_list_widget.setVisible(not self.lessons_list_widget.isVisible())
        self.statistics_button.setVisible(not self.statistics_button.isVisible())
        self.robot_label.setVisible(not self.robot_label.isVisible())

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
        self.settings_window.hide()

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
