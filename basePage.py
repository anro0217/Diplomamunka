from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt

class FramelessPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, 500, 800)
        self.setStyleSheet("background-color: #ffffff; color: #000000;")

    def center_window(self):
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
