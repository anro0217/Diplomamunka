from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class WelcomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout beállítása
        layout = QVBoxLayout()

        # Üdvözlő üzenet
        self.welcome_label = QLabel("Welcome to the Programming Language Learning Assistant!")
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.welcome_label.setAlignment(Qt.AlignCenter)

        # Leírás
        self.description_label = QLabel(
            "This application helps you learn programming languages.\n"
            "Explore different languages, complete practical tasks,\n"
            "and track your progress!\n\n"
            "Click the robot to reach the task description.\n"
            "Use the top-left menu to access the lesson list.\n"
            "On the top-right menu you can find settings, log out, and exit."
        )
        self.description_label.setStyleSheet("font-size: 16px;")
        self.description_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.welcome_label)
        layout.addWidget(self.description_label)

        self.setLayout(layout)
