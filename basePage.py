from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QSize

from database.database import DatabaseManager
from gui.settingsPage import SettingsWindow


class FramelessPage(QWidget):
    def __init__(self, darkModeEnabled=False):
        super().__init__()
        self.db_manager = DatabaseManager('database/application.db')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 500, 800)
        self.setStyleSheet("background-color: #ffffff; color: #000000;")

        # Settings gomb ikonra cserélése
        self.settings_button = QPushButton(self)
        self.settings_button.setIconSize(QSize(40, 40))  # Állítsd be az ikon méretét
        self.settings_button.setGeometry(462, 738, 50, 50)  # Jobb alsó sarok
        self.settings_button.clicked.connect(self.toggle_settings)

        self.setTheme(darkModeEnabled)

        # Beállítások ablak
        self.settings_window = SettingsWindow(self)
        self.settings_window.hide()

    def toggle_settings(self):
        mainWindowGeometry = self.geometry()
        self.settings_window.toggleVisibility(mainWindowGeometry)

    def setTheme(self, darkModeEnabled):
        if darkModeEnabled:
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
            self.settings_button.setIcon(QIcon("resources/images/settings_light_icon.png"))
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")
            self.settings_button.setIcon(QIcon("resources/images/settings_dark_icon.png"))

    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
