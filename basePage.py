from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt

from database.database import DatabaseManager


class FramelessPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager('database/application.db')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 500, 800)
        self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def setTheme(self, darkModeEnabled):
        if darkModeEnabled:
            self.setStyleSheet("background-color: #333333; color: #ffffff;")
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
