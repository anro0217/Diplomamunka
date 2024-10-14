from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication
from PyQt5.QtGui import QPixmap
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

        # Nyíl a robothoz
        self.robot_arrow_label = QLabel()
        robot_arrow_pixmap = QPixmap("robot_arrow.png")  # Robothoz mutató nyíl képe
        self.robot_arrow_label.setPixmap(robot_arrow_pixmap)
        self.robot_arrow_label.setAlignment(Qt.AlignLeft)  # Balra igazítás

        # Nyíl a bal felső menühöz
        self.menu_arrow_label = QLabel()
        menu_arrow_pixmap = QPixmap("menu_arrow.png")  # Bal felső menühöz mutató nyíl
        self.menu_arrow_label.setPixmap(menu_arrow_pixmap)
        self.menu_arrow_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Nyíl a jobb felső beállításokhoz
        self.settings_arrow_label = QLabel()
        settings_arrow_pixmap = QPixmap("settings_arrow.png")  # Jobb felső beállításokhoz nyíl
        self.settings_arrow_label.setPixmap(settings_arrow_pixmap)
        self.settings_arrow_label.setAlignment(Qt.AlignTop | Qt.AlignRight)

        # Widget elemek hozzáadása a layouthoz
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.description_label)
        layout.addWidget(self.robot_arrow_label)
        layout.addWidget(self.menu_arrow_label)
        layout.addWidget(self.settings_arrow_label)

        self.setLayout(layout)
